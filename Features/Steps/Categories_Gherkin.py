import requests
import json
from behave import given, when, then

# Base URL for the API
BASE_URL = "http://localhost:4567"

# User story 1: As a user, I want to create a category so that I can group todos and projects into broader themes.
# Scenario: Create a new category (Normal Flow)

@when(u'the user creates a category with {content}')
def step_when_create_category(context, content):
    # Create the category
    response = requests.post(f"{BASE_URL}/categories", json = eval(content)) 
    context.response = response

@then(u'the category with {content} shall exist in the system')
def step_then_create_category(context, content):
    # Make sure category was created successfully
    assert context.response.status_code == 201
    # And category exists in system
    response = requests.get(f"{BASE_URL}/categories")
    categories = response.json().get("categories", [])
    titles = [cat["title"] for cat in categories]
    assert json.loads(content)['title'] in titles 
    

# Scenario: Create a new category (Alternate Flow)

# Scenario: Create a new category (Error Flow)
@then(u'the category shall not exist in the system')
def step_then_create_category_error(context):
    # Make sure the system did not create the category
    assert context.response.status_code == 400

# Scenario: Get a specific category (Normal Flow)
@ given(u'a category with {content} exists in the system')
def step_given_get_category(context, content):
    # Create the category and store information
    response = requests.post(f"{BASE_URL}/categories", json = eval(content)) 
    context.response = response
    context.category_id = response.json()['id']
    context.category_title = response.json()['title']

@ when(u'I search for that category')
def step_when_get_category(context):
    # Get the category by its id
    id = context.category_id
    response = requests.get(f"{BASE_URL}/categories/{id}")
    context.response = response 

@ then(u'the category with {content} is found')
def step_then_get_category(context, content):
    # Make sure the system succesfully found the category item
    assert context.response.status_code == 200
    # And its title is correct
    cat = context.response.json()['categories'][0]
    assert cat['title'] == json.loads(content)['title']

# Scenario: Get a specific category (Alternate Flow)

# Scenario: Get a specific category (Error Flow)
@ when(u'I search for a category with an id that does not exist')
def step_when_get_category_error(context):
    # Get category with an id that does not exist
    id = 1000000000000000000
    response = requests.get(f"{BASE_URL}/categories/{id}")
    context.response = response

@ then(u'no category is found')
def step_then_get_category_error(context):
    # Make sure the system was not able to find category
    assert context.response.status_code == 404

# Scenario: Delete a specific category (Normal Flow) 
@ when(u'I delete that category')
def step_when_delete_category(context):
    # Delete the category by its id
    id = context.category_id
    response = requests.delete(f"{BASE_URL}/categories/{id}")
    context.response = response

@ then(u'the category gets deleted from the system')
def step_then_delete_category(context):
    # Make sure the category was deleted from the system
    assert context.response.status_code == 200

# Scenario: Delete a specific category (Alternate Flow) 

# Scenario: Delete a specific category (Error Flow) 
@ when(u'I attempt to delete a category with an id that does not exist')
def step_when_delete_category_error(context):
    # Delete a category by an id that does not exist
    id = 100000000000000000000
    response = requests.delete(f"{BASE_URL}/categories/{id}")
    context.response = response

@ then(u'the category does not get deleted')
def step_then_delete_category_error(context):
    # Make sure the category was not found in system
    assert context.response.status_code == 404

# Scenario: Create a todo for a specific category (Normal Flow)
@ when(u'I create a todo item with {content} for the specific category')
def step_when_create_todo_for_category(context, content):
    # Create todo for specific category
    id = context.category_id
    response = requests.post(f"{BASE_URL}/categories/{id}/todos", json = eval(content))
    context.response = response

@ then(u'the todo item with {content} shall exist in the system')
def step_then_creat_todo_for_category(context, content):
    # Make sure the todo was created
    assert context.response.status_code == 201

    # And todo exists in system
    id = context.category_id
    response = requests.get(f"{BASE_URL}/categories/{id}/todos")
    todos = response.json().get("todos", [])
    titles = [todo["title"] for todo in todos]
    assert json.loads(content)['title'] in titles

# Scenario: Create a todo for a specific category (Alternate Flow)

# Scenario: Create a todo for a specific category (Error Flow)
@ when(u'I create a todo item with {content} for a specific category that does not exist')
def step_when_create_todo_for_category_error(context, content):
    # Create todo for category with an id that does not exist
    id = 10000000000000000000
    response = requests.post(f"{BASE_URL}/categories/{id}/todos", json = eval(content))
    context.response = response

@ then(u'the todo item with {content} shall not exist in the system')
def step_then_creat_todo_for_category_error(context, content):
    # Make sure the todo was not created
    assert context.response.status_code == 404

# Scenario: Create a project for a specific category (Normal Flow)
@ when(u'I create a project for the specific category')
def step_when_create_proj_for_category(context):
    # Create project for specific category
    id = context.category_id
    response = requests.post(f"{BASE_URL}/categories/{id}/projects")
    context.response = response

@ then(u'the project shall exist in the system')
def step_then_create_proj_for_category(context):
    # Make sure the project was created
    assert context.response.status_code == 201

# Scenario: Create a project for a specific category (Alternate Flow)
@ when(u'I create a project with {content} for the specific category')
def step_when_create_proj_for_category_alt(context, content):
    # Create project for specific category
    id = context.category_id
    response = requests.post(f"{BASE_URL}/categories/{id}/projects", json = eval(content))
    context.response = response

@ then(u'the project with {content} shall exist in the system')
def step_then_creat_proj_for_category_alt(context, content):
    # Make sure the project was created
    assert context.response.status_code == 201

    # And project exists in system
    id = context.category_id
    response = requests.get(f"{BASE_URL}/categories/{id}/projects")
    projects = response.json().get("projects", [])
    titles = [proj["title"] for proj in projects]
    assert json.loads(content)['title'] in titles

# Scenario: Create a project for a specific category (Error Flow)
@ when(u'I create a project for a specific category that does not exist')
def step_when_create_proj_for_category_error(context):
    # Create project for category with an id that does not exist
    id = 10000000000000000000
    response = requests.post(f"{BASE_URL}/categories/{id}/projects")
    context.response = response

@ then(u'the project shall not exist in the system')
def step_then_creat_proj_for_category_error(context):
    # Make sure the project was not created
    assert context.response.status_code == 404

