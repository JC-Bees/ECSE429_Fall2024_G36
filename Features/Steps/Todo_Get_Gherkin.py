import requests
from behave import given, when, then

BASE_URL = 'http://localhost:4567/todos'

TODO_ID_URL = 'http://localhost:4567/todos/{id}'

CATEGORY_URL = 'http://localhost:4567/todos/{id}/categories'

# Step definitions for 'GIVEN' steps

@given(u'I have a todo item with {content}')
def Todo_step_existing_todo_item(context, content):
    #Create the todo item
    response = requests.post(BASE_URL, json=eval(content))
    assert response.status_code == 201
    #saving the id of the todo for testing
    context.todoID = response.json()['id']

@given(u'I have todo items')
def Todo_step_existing_todo_items(context):
    # Create multiple todo items for testing
    response = requests.post(BASE_URL, json={"title": "TestTitle1"})
    assert response.status_code == 201
    response = requests.post(BASE_URL, json={"title": "TestTitle2"})
    assert response.status_code == 201
    response = requests.post(BASE_URL, json={"title": "TestTitle3"})
    assert response.status_code == 201
    response = requests.post(BASE_URL, json={"title": "TestTitle4"})
    assert response.status_code == 201
    response = requests.post(BASE_URL, json={"title": "TestTitle5"})
    assert response.status_code == 201

@given(u'I have no todo item')
def Todo_step_no_existing_todo_item(context):
    # Get any existing todos
    response = requests.get(BASE_URL)
    todoList = response.json()['todos']
    # If any exist, then delete them by id
    if (len(todoList) > 0):
        for todo in todoList:
            response = requests.delete(TODO_ID_URL.format(id =todo['id']))
            assert response.status_code == 200
    # Check to see that they were properly deleted
    response = requests.get(BASE_URL)
    todoList = response.json()['todos']
    assert len(todoList) == 0

# Step definitions for 'WHEN' steps

@when(u'I create a todo item with {content}')
def Todo_step_create_todo_item(context, content):
    # Create a todo
    response = requests.post(BASE_URL, json=eval(content))
    context.response = response

@when(u'I search for that todo item')
def Todo_step_search_todo_item(context):
    # Get a todo item
    response = requests.get(TODO_ID_URL.format(id = context.todoID))
    context.response = response

@when(u'I search for a todo item with a bad id')
def Todo_step_search_todo_item_badId(context):
    # Creating item using ID 123456789 as it will never exist in testing
    response = requests.get(TODO_ID_URL.format(id = 123456789))
    context.response = response

@when(u'I update a non-existing todo item with {content}')
def Todo_step_update_non_existing_todo_item(context,content):
    # Creating item using ID 123456789 as it will never exist in testing
    response = requests.put(TODO_ID_URL.format(id = 123456789), json=eval(content))
    context.response = response

@when(u'I update that todo item with {content}')
def Todo_step_update_todo_item(context, content):
    # Update a todo item
    response = requests.put(TODO_ID_URL.format(id = context.todoID), json=eval(content))
    context.response = response

@when(u'I try to delete that todo item')
def Todo_step_delete_todo_item(context):
    # Delete a todo item
    response = requests.delete(TODO_ID_URL.format(id = context.todoID))
    context.response = response

@when(u'I try to delete all the todo items')
def Todo_step_delete_all_todo_items(context):
    # Get any existing todos
    response = requests.get(BASE_URL)
    todoList = response.json()['todos']
    if (len(todoList) > 0):
        for todo in todoList:
            response = requests.delete(TODO_ID_URL.format(id =todo['id']))
            assert response.status_code == 200
            context.response = response
    # Check to see that they were properly deleted
    response = requests.get(BASE_URL)
    todoList = response.json()['todos']
    assert len(todoList) == 0

@when(u'I try to delete a non-existing todo item')
def Todo_step_delete_non_existing_todo_item(context):
    # Creating item using ID 123456789 as it will never exist in testing
    response = requests.delete(TODO_ID_URL.format(id = 123456789))
    context.response = response

@when(u'I add a category to a non-exsiting todo item with {content}')
def Todo_step_add_category_to_non_existing_todo_item(context,content):
    # Creating item using ID 123456789 as it will never exist in testing
    response = requests.post(CATEGORY_URL.format(id = 123456789), json=eval(content)) 
    context.response = response

@when(u'I add a category to the todo item with {content}')
def Todo_step_add_category(context, content):
    # Create a new category for a todo item
    response = requests.post(CATEGORY_URL.format(id = context.todoID), json=eval(content))
    context.response = response
    
# Step definitions for 'THEN' steps

@then(u'the todo item should be created')
def Todo_step_todo_item_created(context):
    # Make sure the todo item is created
    assert context.response.status_code == 201

@then(u'the todo item should contain {content}')
def Todo_step_todo_item_contains(context, content):
    # Make sure the content was properly inputed
    assert content in context.response.json().values()

@then(u'the todo item should not be created')
def Todo_step_todo_item_not_created(context):
    # Make sure the system rejected the request
    assert context.response.status_code == 400

@then(u'the todo item is found and sent to me')
def Todo_step_todo_item_found(context):
    # Make sure the system succesfully found the todo item
    assert context.response.status_code == 200

@then(u'the search should contain {content}')
def Todo_step_response_contains(context, content):
    # Check that the obtained results contain what was specified
    check = False
    for todos in context.response.json()['todos']:
        if content in todos.values():
            check = True
    assert check == True

@then(u'the todo item should not be found')
def Todo_step_todo_item_not_found(context):
    # Make sure the todo is not in the system
    assert context.response.status_code == 404

@then(u'the todo item should be updated')
def Todo_step_todo_item_updated(context):
    # Make sure the todo item was updated succesfully
    assert context.response.status_code == 200

@then(u'that todo item should no longer exist')
def Todo_step_todo_item_should_no_longer_exist(context):
    # Make sure the system can't find the todo
    response = requests.get(TODO_ID_URL.format(id = context.todoID))
    assert response.status_code == 404

@then(u'the todo item should be deleted')
def Todo_step_todo_item_deleted(context):
    # Make sure the todo was successfully deleted
    assert context.response.status_code == 200

@then(u'the todo items should be deleted')
def Todo_step_todo_items_deleted(context):
    # Make sure all the todos were deleted
    assert context.response.status_code == 200

@then(u'the todo item list should be empty')
def Todo_step_todo_item_list_empty(context):
    # Make sure all the todos were deleted, system should have no more todos
    response = requests.get(BASE_URL)
    todoList = response.json()['todos']
    assert len(todoList) == 0

@then(u'the category should be created and added to the todo item')
def Todo_step_category_created(context):
    # Make sure the category was created
    assert context.response.status_code == 201

@then(u'the category should contain {content}')
def Todo_step_category_contains_title(context, content):
    # Make sure the created category containes the specified content
    category_data = context.response.json().values()
    assert content in category_data

