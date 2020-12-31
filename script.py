from browser import alert, document, html
from browser.local_storage import storage
from datetime import datetime
import json

# date
today = datetime.now().strftime('%A, %b %d')

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
    if task.value:
        delete_button = html.SPAN("&#10008;", Class="delete button", id=f"delete_{timestamp}")
        done_button = html.SPAN("&#10004;", Class="todone button", id=f"done_{timestamp}")
        later_button = html.SPAN("||", Class="tolater button", id=f"later_{timestamp}")
        new_item = html.SPAN(task.value, Class="item", id=f"item_{timestamp}")
        item_div = html.DIV(new_item + done_button + later_button + delete_button, id=timestamp, Class="task")
        todo <= item_div
        storage[str(timestamp)] = json.dumps({'date': timestamp, 'status': 'todo', 'task': task.value, 'div': item_div.innerHTML})
        task.value = ""
        document[f"done_{timestamp}"].bind('click', update_button)
        document[f"later_{timestamp}"].bind('click', update_button)
        document[f"delete_{timestamp}"].bind('click', update_button)
        update_progress()

def update_button(event):
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
        tolater <= item
    elif "done" in button_class:
        for child in item.children:
            if "button" in child.class_name:
                item.removeChild(child)
        stored_item['status'] = 'completed'
        stored_item['div'] = item.innerHTML
        storage[str(item.id)] = json.dumps(stored_item)
        todone <= item
    elif "delete" in button_class:
        del storage[str(item.id)]
    update_progress()
    
def update_progress():
    remaining = todo.childElementCount
    todo_count.text = remaining
    completed = todone.childElementCount
    todone_count.text = completed
    if completed > 0 and len(document.select(".clear")) == 0:
        document["lists"] <= html.P("Clear completed", Class="clear center button", id="clear")
        document["clear"].bind('click', clear_completed)
    elif completed == 0 and len(document.select(".clear")) == 1:
        document["lists"].removeChild(document["clear"])
    
    paused = tolater.childElementCount
    tolater_count.text = paused
    progress.max = remaining + completed
    progress.value = completed
    if progress.value == progress.max:
        alert("YOU COMPLETED ALL YOUR TASKS! YOU. ARE. AWESOME!")

def enter_submits(e):
    if e.which is 13:
        document["submit-btn"].click()

def clear_completed(e):
    for stored_item in storage:
        item = json.loads(storage[stored_item])
        if item['status'] is 'completed':
            del storage[stored_item]
            todone.removeChild(document[stored_item])
    update_progress()

# storage
for item in storage:
    stored = json.loads(storage[item])
    inner = json.loads(storage[item])['div']
    if stored['status'] is 'todo':
        todo <= html.DIV(inner, id=item, Class='task')
        document[f"done_{item}"].bind('click', update_button)
        document[f"later_{item}"].bind('click', update_button)
        document[f"delete_{item}"].bind('click', update_button)
    elif stored['status'] is 'later':
        tolater <= html.DIV(inner, id=item, Class='task')
        document[f"done_{item}"].bind('click', update_button)
        document[f"delete_{item}"].bind('click', update_button)
    elif stored['status'] is 'completed':
        todone <= html.DIV(inner, id=item, Class='task')

update_progress()
document["new-item"].bind('keypress', enter_submits)
document["submit-btn"].bind('click', add_item)
document["date"].text = today