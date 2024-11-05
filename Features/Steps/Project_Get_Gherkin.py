import requests
from behave import given, when, then

BASE_URL = 'http://localhost:4567/projects'

Projects_ID_URL = 'http://localhost:4567/projects/{id}'

CATEGORY_URL = 'http://localhost:4567/categories'

Project_to_Category_Url = 'http://localhost:4567/projects/{id}/categories'

Task_Url = 'http://localhost:4567/todos'

Project_to_task_Url = 'http://localhost:4567/projects/{id}/tasks'

# Step definitions for 'GIVEN' steps

@given(u'I have a project item with {content}')
def project_step_given(context, content):
    #Create Project
    response = requests.post(BASE_URL, json=eval(content))
    assert response.status_code == 201
    context.projectID = response.json()['id']

@given(u'that I am searching for a project but without its ID {content}')
def project_step_given_no_id(context, content): 
    context.projectID = content

@given(u'that I have a category item {content1} that I want to relate to a project item {content2}')
def project_step_given_category_and_project(context, content1, content2):
    #creating the project
    response_project = requests.post(BASE_URL, json=eval(content2))
    assert response_project.status_code == 201
    context.projectID = response_project.json()['id']
    #creating the category
    response_category = requests.post(CATEGORY_URL, json=eval(content1))
    assert response_category.status_code == 201
    context.categoryID = response_category.json()['id']

@given(u'that I have two category items {content1}, {content2} that I want to relate to a project item {content3}')
def project_step_given_multiple_categories(context, content1, content2, content3):
    #creating the project
    response_project = requests.post(BASE_URL, json=eval(content3))
    assert response_project.status_code == 201
    context.projectID = response_project.json()['id']
    #creating the category1
    response_category1 = requests.post(CATEGORY_URL, json= eval(content1))
    assert response_category1.status_code == 201
    context.category1ID = response_category1.json()['id']
    #creating the category2
    response_category2 = requests.post(CATEGORY_URL, json=eval(content2))
    assert response_category2.status_code == 201
    context.category2ID = response_category2.json()['id']

@given(u'that i have a project item {content1} and a category item that is invalid {content2}')
def project_step_given_error_flow_category_no_id(context, content1, content2):
    #creating the project
    response_project = requests.post(BASE_URL, json=eval(content1))
    assert response_project.status_code == 201
    context.projectID = response_project.json()['id']
    #no need to create category
    context.categoryID = content2

@given(u'that I have a project item {content} whos header I want to retrieve')
def project_step_when_metadata_retrieval(context, content):
    #creating the project
    response_project = requests.post(BASE_URL, json=eval(content))
    assert response_project.status_code == 201
    context.projectID = response_project.json()['id']

@given(u'that I have a project item {content1} and another project item of {content2}')
def project_step_when_multiple_projects_head_method(context, content1, content2):
    #creating the project1
    response_project1 = requests.post(BASE_URL, json=eval(content1))
    assert response_project1.status_code == 201
    context.project1ID = response_project1.json()['id']
    #creating the project2
    response_project2 = requests.post(BASE_URL, json=eval(content2))
    assert response_project2.status_code == 201
    context.project2ID = response_project2.json()['id']

@given(u'that I have a project item {content} whos project ID is invalid')
def project_step_given_invalid_project_id_metadata_retrieval(context, content):
    context.projectID = content

@given(u'that I have a specific project item {content1} that is related to a specific category item {content2}')
def project_step_given_relating_category_to_project_then_deleting(context, content1, content2):
    #creating the project
    response_project = requests.post(BASE_URL, json=eval(content1))
    assert response_project.status_code == 201
    context.projectID = response_project.json()['id']
    #creating the category
    response_category = requests.post(CATEGORY_URL, json=eval(content2))
    assert response_category.status_code == 201
    context.categoryID = response_category.json()['id']
    #relating the category to the project
    data = {
        "id" : context.categoryID
    }
    response = requests.post(Project_to_Category_Url.format(id = context.projectID), json = data)
    assert response.status_code == 201

@given(u'that I have a specific project item {content1} that is related to multiple specific category items {content2}, {content3}')
def project_step_given_multiple_categories_to_project(context, content1, content2, content3):
    #creating the project
    response_project = requests.post(BASE_URL, json=eval(content1))
    assert response_project.status_code == 201
    context.projectID = response_project.json()['id']
    #creating the category1
    response_category1 = requests.post(CATEGORY_URL, json=eval(content2))
    assert response_category1.status_code == 201
    context.category1ID = response_category1.json()['id']
    #creating the category2
    response_category2 = requests.post(CATEGORY_URL, json=eval(content3))
    assert response_category2.status_code == 201
    context.category2ID = response_category2.json()['id']
    #relating the category1 to the project
    data1 = {
        "id" : context.category1ID
    }
    response_relation1 = requests.post(Project_to_Category_Url.format(id = context.projectID), json = data1)
    assert response_relation1.status_code == 201
    #relating the category2 to the project
    data2 = {
        "id" : context.category2ID
    }
    response_relation2 = requests.post(Project_to_Category_Url.format(id = context.projectID), json = data2)
    assert response_relation2.status_code == 201

@given(u'that i have a specific project item {content1} and an invalid category ID {content2}')
def project_step_given_relating_project_to_category_with_invalid_category_id(context, content1, content2):
    #creating the project
    response_project = requests.post(BASE_URL, json=eval(content1))
    assert response_project.status_code == 201
    context.projectID = response_project.json()['id']
    #categoryid
    context.categoryID = content2

@given(u'a specific project item {content1} and a specific task item {content2}')
def project_step_given_adding_task_to_project(context, content1, content2):
    #creating the project
    response_project = requests.post(BASE_URL, json=eval(content1))
    assert response_project.status_code == 201
    context.projectID = response_project.json()['id']
    #creating the task
    response_task = requests.post(Task_Url, json=eval(content2))
    assert response_task.status_code == 201
    context.taskID = response_task.json()['id']

@given(u'a specific project item {content1} and multiple specific task items {content2}, {content3}')
def project_step_given_multiple_tasks(context, content1, content2, content3):
    #creating the project
    response_project = requests.post(BASE_URL, json=eval(content1))
    assert response_project.status_code == 201
    context.projectID = response_project.json()['id']
    #creating the task1
    response_task1 = requests.post(Task_Url, json=eval(content2))
    assert response_task1.status_code == 201
    context.task1ID = response_task1.json()['id']
    #creating the task2
    response_task2 = requests.post(Task_Url, json=eval(content3))
    assert response_task2.status_code == 201
    context.task2ID = response_task2.json()['id']

@given(u'a specific project item {content1} and an invalid specific task item {content2}')
def project_step_given_invalid_task_relation(context, content1, content2):
    #creating the project
    response_project = requests.post(BASE_URL, json=eval(content1))
    assert response_project.status_code == 201
    context.projectID = response_project.json()['id']
    #creating the task
    response_task = requests.post(Task_Url, json=eval(content2))
    assert response_task.status_code == 400
    context.taskID = content2


#Step definitions for "When" steps 

@when(u'I search for that project')
def project_step_when(context):
    # Get a todo item
    response = requests.get(Projects_ID_URL.format(id = context.projectID))
    context.response = response

@when(u'I search for that project item with the get all projects method')
def project_step_when_get_all(context):
    #Get all projects
    response = requests.get(BASE_URL)
    context.response = response

@when(u'I search for that project without an ID')
def project_step_when_search_with_no_id(context):
    response = requests.get(Projects_ID_URL.format(id = context.projectID))
    context.response = response

@when(u'I add a relation between the category and project')
def project_step_when_add_category(context): 
    data = {
        "id" : context.categoryID
    }
    response = requests.post(Project_to_Category_Url.format(id = context.projectID), json = data)
    assert response.status_code == 201

@when(u'I add a relation between the categories and project')
def project_step_when_add_relation_multiple_categories(context):
    data1 = {
        "id" : context.category1ID
    }
    data2 = {
        "id" : context.category2ID
    }
    response1 = requests.post(Project_to_Category_Url.format(id = context.projectID), json = data1)
    response2 = requests.post(Project_to_Category_Url.format(id = context.projectID), json = data2)
    assert response1.status_code == 201
    assert response2.status_code == 201

@when(u'I try to relate the category to the project')
def project_step_when_relating_invalid_category_id(context):
    data = {
        "id" : context.categoryID
    }
    response = requests.post(Project_to_Category_Url.format(id = context.projectID), json = data)
    context.response = response

@when(u'I retrieve the metadata')
def project_step_when_retrieving_metadata(context):
    #getting the header information
    response = requests.head(Projects_ID_URL.format(id = context.projectID))
    context.response = response

@when(u'I retrieve the metadata for those specific projects')
def project_step_when_retrieve_all_metadata(context):
    #getting the header information
    response = requests.head(BASE_URL)
    context.response = response

@when(u'I try to retrieve the metadata for the invalid project')
def project_step_when_retrieve_invalid_project_metadata(context):
    response = requests.head(Projects_ID_URL.format(id = context.projectID))
    context.response = response

@when(u'I try to delete the relationship between the project and the category')
def project_step_when_delete_relationship_between_project_and_category(context):
    response = requests.delete('http://localhost:4567/projects/{id1}/categories/{id2}'.format(id1 = context.projectID, id2 = context.categoryID))
    assert response.status_code == 200

@when(u'I try to delete the relationship between the project and the multiple categories')
def project_step_when_deleting_multiple_relationships_from_project(context):
    response_deletion1 = requests.delete('http://localhost:4567/projects/{id1}/categories/{id2}'.format(id1 = context.projectID, id2 = context.category1ID))
    assert response_deletion1.status_code == 200
    response_deletion2 = requests.delete('http://localhost:4567/projects/{id1}/categories/{id2}'.format(id1 = context.projectID, id2 = context.category2ID))
    assert response_deletion2.status_code == 200

@when(u'I try to delete the relationship between the category and the project')
def project_step_when_deleting_invalid_category_id_from_project(context):
    response = requests.delete('http://localhost:4567/projects/{id1}/categories/{id2}'.format(id1 = context.projectID, id2 = context.categoryID))
    assert response.status_code == 404
    context.response = response

@when(u'I try to add the specific task to the project')
def project_step_when_adding_task_to_project(context):
    data = {
        "id" : context.taskID
    }
    response = requests.post(Project_to_task_Url.format(id= context.projectID), json = data)
    assert response.status_code == 201
    context.response = response

@when(u'I try to add the specific task items to the project')
def project_step_when_adding_multiple_taks_to_project(context):
    #adding task1
    data1 = {
        "id" : context.task1ID
    }
    response_task1 = requests.post(Project_to_task_Url.format(id= context.projectID), json = data1)
    assert response_task1.status_code == 201
    context.response_task1 = response_task1
    #adding task2
    data2 = {
        "id" : context.task2ID
    }
    response_task2 = requests.post(Project_to_task_Url.format(id= context.projectID), json = data2)
    assert response_task2.status_code == 201
    context.response_task2 = response_task2

@when(u'I try to add the specific invalid task item to the project')
def project_step_when_relating_invalid_task_to_a_project(context):
    #adding task
    data = {
        "id" : context.taskID
    }
    response_task = requests.post(Project_to_task_Url.format(id= context.projectID), json = data)
    assert response_task.status_code == 404
    context.response_task = response_task


#Step definitions for "Then" steps

@then(u'the project is found and sent to me')
def project_step_then(context):
    # Make sure the system succesfully found the todo item
    assert context.response.status_code == 200

@then(u'the project search should contain {content}')
def project_step_then_response_contains(context, content):
    # Check that the obtained results contain what was specified
    check = False
    for project in context.response.json()['projects']:
        if content in project.values():
            check = True
    assert check == True

@then(u'the projects should be sent to me')
def project_step_then_get_all(context):
    assert context.response.status_code == 200

@then(u'the projects should contain the project item title {content}')
def project_step_then_get_all_contain(context, content):

    check = False
    for project in context.response.json()['projects']:
        if content in project.values():
            check = True
    assert check == True

@then(u'I should get an error message telling me to specify the project ID')
def project_step_then_message_to_specify_id(context):
    assert context.response.status_code == 404 
    assert context.response.json()['errorMessages'][0] == 'Could not find an instance with projects/{}'

@then(u'the project information should contain the category and its information {content}')
def project_step_category_validation(context, content):
    #get the project 
    response = requests.get(Projects_ID_URL.format(id = context.projectID))
    assert context.categoryID in response.json()['projects'][0]['categories'][0]['id']

@then(u'the project information should contain the category IDs')
def project_step_then_multiple_category_validation(context):
    response = requests.get(Projects_ID_URL.format(id = context.projectID))
    list = [context.category2ID, context.category1ID]
    for category in response.json()['projects'][0]['categories']:
        if category['id'] in list:
            list.remove(category['id'])
    if not list: 
        assert True
    else: 
        assert False
    
@then(u'I should get an error message telling me {content}')
def project_step_then_relating_invalid_category_to_project(context, content):
    assert context.response.status_code == 404 
    assert context.response.json()['errorMessages'][0] == content

@then(u'everything shoud look fine and the content should be of type {content}')
def project_step_then_metadata_validation(context, content):
    assert context.response.status_code == 200
    print(content)
    assert context.response.headers['Content-Type'] == content

@then(u'everything should be fine and the content should be of type {content}')
def project_step_then_all_header_info_validation(context, content):
    assert context.response.status_code == 200
    assert context.response.headers['Content-Type'] == content

@then(u'I should be notified that an error has occured by the status code {content}')
def project_step_then_getting_invalid_project_id_metadata(context, content):
    assert context.response.status_code == int(content)

@then(u'I should not see that category in the project information')
def project_step_then_deleting_category_from_project_validation(context):
    #get the project again 
    response = requests.get(Projects_ID_URL.format(id = context.projectID))
    check = True
    categories = response.json()['projects'][0].get('categories')
    if categories:
        for category in categories:
            if category['id'] == context.categoryID:
                check = False
    if check: 
        assert True
    
@then(u'the category information should not be present in the project information')
def project_step_then_multiple_deletion_validation(context):
    response = requests.get(Projects_ID_URL.format(id = context.projectID))
    check1 = True
    check2 = True
    categories = response.json()['projects'][0].get('categories')
    if categories:
        for category in categories:
            if category['id'] == context.category1ID:
                check1 = False
            if category['id'] == context.category2ID:
                check2 = False
    if check1 and check2: 
        assert True
    
@then(u'I should be notified that no category wa sable to be found')
def project_step_then_invalid_category_id_deletion(context):
    assert context.response.json()['errorMessages'][0] == f'Could not find any instances with projects/{context.projectID}/categories/{context.categoryID}'

@then(u'the tasks information should not be present in the projects information')
def project_step_then_validating_single_task_info(context):
    response = requests.get(Projects_ID_URL.format(id = context.projectID))
    tasks = response.json()['projects'][0].get('tasks')
    if tasks:
        for task in tasks:
            if task['id'] == context.taskID:
                check = False
    if check: 
        assert True
    
@then(u'the multiple task item information should not be present in the projects information')
def project_step_then_multiple_tasks(context):
    response = requests.get(Projects_ID_URL.format(id = context.projectID))
    tasks = response.json()['projects'][0].get('tasks')
    list = [context.task1ID, context.task2ID]
    for task in tasks:
        if task['id'] in list:
            list.remove(task['id'])
    print(list)
    if not list: 
        assert True
    else: 
        assert False

@then(u'I should get an error saying no specific task item of such was found')
def project_step_then_relating_invalid_task_id_validation(context):
    assert context.response_task.status_code == 404


