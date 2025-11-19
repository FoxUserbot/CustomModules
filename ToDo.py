# Ported With Wine Hikka
# Original Code By https://mods.xdesai.top/ToDo.py
import os
import json
import asyncio
from random import randint
from pyrogram import Client
from command import fox_command, fox_sudo, who_message, get_text, my_prefix

Module_Name = "ToDo"

LANGUAGES = {
    "en": {
        "task_removed": "<blockquote><b>✅ Task removed</b></blockquote>",
        "task_not_found": "<blockquote><b>🚫 Task not found</b></blockquote>",
        "new_task": "<b>Task </b><code>#{task_id}</code>:\n<blockquote>{task}</blockquote>\n{level}",
        "todo_list": "<blockquote><b>#ToDo</b></blockquote>",
        "importance_level": " -{{ {level} }}-",
        "task_item": "{task_id}: {task_text}",
        "no_tasks": "<blockquote><b>📭 No tasks</b></blockquote>",
        "usage": "📝 <b>Usage:</b> <code>{prefix}td [importance:0-4] [task]</code>",
        "utd_usage": "🗑️ <b>Usage:</b> <code>{prefix}utd [task_id]</code>",
    },
    "ru": {
        "task_removed": "<blockquote><b>✅ Задача удалена</b></blockquote>",
        "task_not_found": "<blockquote><b>🚫 Задача не найдена</b></blockquote>",
        "new_task": "<b>Задача </b><code>#{task_id}</code>:\n<blockquote>{task}</blockquote>\n{level}",
        "todo_list": "<blockquote><b>#ToDo</b></blockquote>",
        "importance_level": " -{{ {level} }}-",
        "task_item": "{task_id}: {task_text}",
        "no_tasks": "<blockquote><b>📭 Нет задач</b></blockquote>",
        "usage": "📝 <b>Использование:</b> <code>{prefix}td [важность:0-4] [задача]</code>",
        "utd_usage": "🗑️ <b>Использование:</b> <code>{prefix}utd [id_задачи]</code>",
    },
    "ua": {
        "task_removed": "<blockquote><b>✅ Завдання видалено</b></blockquote>",
        "task_not_found": "<blockquote><b>🚫 Завдання не знайдено</b></blockquote>",
        "new_task": "<b>Завдання </b><code>#{task_id}</code>:\n<blockquote>{task}</blockquote>\n{level}",
        "todo_list": "<blockquote><b>#ToDo</b></blockquote>",
        "importance_level": " -{{ {level} }}-",
        "task_item": "{task_id}: {task_text}",
        "no_tasks": "<blockquote><b>📭 Немає завдань</b></blockquote>",
        "usage": "📝 <b>Використання:</b> <code>{prefix}td [важливість:0-4] [завдання]</code>",
        "utd_usage": "🗑️ <b>Використання:</b> <code>{prefix}utd [id_завдання]</code>",
    }
}


def load_todos():
    try:
        with open("userdata/todo_list.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_todos(todos):
    with open("userdata/todo_list.json", "w", encoding="utf-8") as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)

@Client.on_message(fox_command("td", Module_Name, os.path.basename(__file__), "[importance:int] [task]") & fox_sudo())
async def td_handler(client, message):
    message = await who_message(client, message)
    args = message.text.split(maxsplit=1)
    args = args[1] if len(args) > 1 else ""
    

    todos = load_todos()
    

    imp_levels = [
        "🌌 Watchlist",
        "💻 Proging", 
        "⌚️ Work",
        "🎒 Family",
        "🚫 Private",
    ]
    
    importance = 0
    task = args
    
    if args:
        try:
            first_word = args.split()[0]
            if first_word.isdigit():
                importance = int(first_word)
                task = args.split(maxsplit=1)[1] if len(args.split()) > 1 else ""
        except (IndexError, ValueError):
            pass
    
    if not task and message.reply_to_message:
        task = message.reply_to_message.text
    
    if not task:
        prefix = my_prefix()
        text = get_text(Module_Name, "usage", LANGUAGES=LANGUAGES, prefix=prefix)
        await message.edit(text)
        return
    
    if importance >= len(imp_levels):
        importance = 0
    
    random_id = str(randint(10000, 99999))
    
    todos[random_id] = [task, importance]
    save_todos(todos)
    
    text = get_text(Module_Name, "new_task", LANGUAGES=LANGUAGES, 
                   task_id=random_id, task=task, level=imp_levels[importance])
    await message.edit(text)

@Client.on_message(fox_command("tdl", Module_Name, os.path.basename(__file__)) & fox_sudo())
async def tdl_handler(client, message):
    message = await who_message(client, message)
    todos = load_todos()
    if not todos:
        text = get_text(Module_Name, "no_tasks", LANGUAGES=LANGUAGES)
        await message.edit(text)
        return
    imp_levels = [
        "🌌 Watchlist",
        "💻 Proging", 
        "⌚️ Work",
        "🎒 Family",
        "🚫 Private",
    ]
    items = {len(imp_levels) - i - 1: [] for i in range(len(imp_levels))}
    for task_id, task_data in todos.items():
        task_text, importance = task_data
        prefix = my_prefix()
        task_link = f"<code>{prefix}utd {task_id}</code>: <code>{task_text}</code>"
        items[importance].append(task_link)
    result = get_text(Module_Name, "todo_list", LANGUAGES=LANGUAGES) + "\n"
    for importance in sorted(items.keys(), reverse=True):
        task_list = items[importance]
        if not task_list:
            continue
        level_text = imp_levels[importance]
        result += f"\n<blockquote>{get_text(Module_Name, 'importance_level', LANGUAGES=LANGUAGES, level=level_text)}\n"
        result += level_text[0] + ("\n" + level_text[0]).join(task_list) + "</blockquote>\n"
    
    await message.edit(result)

@Client.on_message(fox_command("utd", Module_Name, os.path.basename(__file__), "[task_id]") & fox_sudo())
async def utd_handler(client, message):
    message = await who_message(client, message)
    args = message.text.split()
    if len(args) < 2:
        prefix = my_prefix()
        text = get_text(Module_Name, "utd_usage", LANGUAGES=LANGUAGES, prefix=prefix)
        await message.edit(text)
        return
    task_id = args[1].lstrip("#")
    todos = load_todos()
    if task_id not in todos:
        text = get_text(Module_Name, "task_not_found", LANGUAGES=LANGUAGES)
        await message.edit(text)
        return
    del todos[task_id]
    save_todos(todos)
    text = get_text(Module_Name, "task_removed", LANGUAGES=LANGUAGES)
    await message.edit(text)
