from browser import alert, document, html
from browser.local_storage import storage
from datetime import datetime
import json, time

# date
today = datetime.now().strftime('%A, %b %d')
document["date"].text = today

# progress bar
progress = document["progress"]

# counts
todo_count = document["todo-count"]
todone_count = document["todone-count"]
tolater_count = document["tolater-count"]

# lists
todo = document["todo"]
todone = document["todone"]
tolater = document["tolater"]

def add_item(e):
    timestamp = datetime.now().timestamp()
    task = document["new-item"]
    delete_button = html.SPAN("&#10008;", Class="delete button", id=f"delete_{timestamp}")
    done_button = html.SPAN("&#10004;", Class="done button", id=f"done_{timestamp}")
    later_button = html.SPAN("||", Class="later button", id=f"later_{timestamp}")
    new_item = html.SPAN(task.value, Class="item", id=f"item_{timestamp}")
    item_div = html.DIV(new_item + done_button + later_button + delete_button, id=timestamp, Class="task")
    todo <= item_div
    storage[str(timestamp)] = json.dumps({'date': timestamp, 'status': 'todo', 'task': task.value, 'div': item_div.innerHTML})
    task.value = ""
    document[f"done_{timestamp}"].bind('click', mark_done)
    document[f"later_{timestamp}"].bind('click', do_later)
    document[f"delete_{timestamp}"].bind('click', remove_task)
    update_progress()
     
def mark_done(e):
    update_button(e, undo, mark_done, todone)
    update_progress()

def do_later(e):
    update_button(e, do_now, do_later, tolater)
    update_progress()

def undo(e):
    update_button(e, mark_done, undo, todo)
    update_progress()

def remove_task(e):
    update_button(e)
    update_progress()
    
def do_now(e):
    update_button(e, do_later, do_now, todo)
    update_progress()

def update_button(event, f_bind = '', f_unbind = '', section = ''):
    button_span = event.target
    button_class = button_span.class_name
    item = button_span.parentElement
    list = item.parentElement
    stored_item = json.loads(storage[str(item.id)])
    list.removeChild(item)
    if "later" in button_class:
        item.removeChild(button_span)
        stored_item['status'] = 'later'
        stored_item['div'] = item.innerHTML
        storage[str(item.id)] = json.dumps(stored_item)
    elif "done" in button_class:
        for child in item.children:
            if "button" in child.class_name:
                item.removeChild(child)
        stored_item['status'] = 'completed'
        stored_item['div'] = item.innerHTML
        storage[str(item.id)] = json.dumps(stored_item)
    elif "delete" in button_class:
        del storage[str(item.id)]
    if not "delete" in button_class:
        button_span.bind('click', f_bind)
        button_span.unbind('click', f_unbind)
        section <= item
    
def update_progress():
    remaining = todo.childElementCount
    todo_count.text = remaining
    completed = todone.childElementCount
    todone_count.text = completed
    paused = tolater.childElementCount
    tolater_count.text = paused
    progress.max = remaining + completed
    progress.value = completed
    if progress.value == progress.max:
        alert("YOU COMPLETED ALL YOUR TASKS! YOU. ARE. AWESOME!")

# storage
for item in storage:
    stored = json.loads(storage[item])
    print(stored['status'], ': ', stored['task'])
    inner = json.loads(storage[item])['div']
    if stored['status'] is 'todo':
        todo <= html.DIV(inner, id=item, Class='task')
        document[f"done_{item}"].bind('click', mark_done)
        document[f"later_{item}"].bind('click', do_later)
        document[f"delete_{item}"].bind('click', remove_task)
    elif stored['status'] is 'later':
        tolater <= html.DIV(inner, id=item, Class='task')
        document[f"done_{item}"].bind('click', mark_done)
        document[f"delete_{item}"].bind('click', remove_task)
    elif stored['status'] is 'completed':
        todone <= html.DIV(inner, id=item, Class='task')

document["submit-btn"].bind('click', add_item)