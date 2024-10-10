import requests
import pytest
import pytest_randomly

# Run Tests using "pytest Categories_Module_Tests.py" In terminal

# Base URL for the API
BASE_URL = "http://localhost:4567/categories"

@pytest.fixture(autouse=True)
def tearDown():
    # This function will run before each test to reset all variables
    yield
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        # if there are categories in the system
        categories = response.json().get("categories", [])
        for category in categories:
            id = category["id"]
            requests.delete(f"{BASE_URL}/{id}") # deletes each category in system

# ACTUAL BEHAVIOUR WORKING

# First general test to make sure everything works
def test_get_GUI():
    url = "http://localhost:4567/gui/entities"  # Adjust the port if needed
    response = requests.get(url)

    # Check that the response status code is 200 OK
    assert response.status_code == 200

    # Check that the response content type is text/html
    assert response.headers["Content-Type"] == "text/html"


# Get the categories page contents
def test_get_data():
    url = "http://localhost:4567/categories"
    response = requests.get(url)

    # Check that the response status code is 200 OK
    assert response.status_code == 200

    # Check that the response content type is text/html
    assert response.headers["Content-Type"] == "application/json"

    # data = response.json()
    # assert 'id' in data
    # assert 'title' in data
    # assert 'description' in data


# Post to category page contents will all inputs
def test_post_data_Success():
    url = "http://localhost:4567/categories"

    data = {"title": "Groceries", "description": "grocery lists"}

    response = requests.post(url, json=data)

    assert response.status_code == 201

    data = response.json()

    assert data["id"]
    assert data["title"] == "Groceries"
    assert data["description"] == "grocery lists"


# Post to category page contents with id, fail
def test_post_data_FailID():
    url = "http://localhost:4567/categories"

    data = {"id": "4", "title": "Groceries", "description": "grocery lists"}

    response = requests.post(url, data)

    assert response.status_code == 415


# Get header information for categories
def test_head_category():
    url = "http://localhost:4567/categories"

    response = requests.head(url)

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"


# Test to get a category by id
def test_get_category_by_id():
    # create a test category
    data = {"title": "Soccer", "description": "to-do lists about soccer"}
    post_response = requests.post(BASE_URL, json=data)
    created_category = post_response.json()
    category_id = created_category["id"]

    response = requests.get(f"{BASE_URL}/{category_id}")

    assert response.status_code == 200
    data = response.json()

    assert data["categories"][0]["id"] == category_id
    assert data["categories"][0]["title"] == "Soccer"
    assert data["categories"][0]["description"] == "to-do lists about soccer"


# Test to get a category by invalid id, fail
def test_get_category_by_invalid_id():
    response = requests.get(f"{BASE_URL}/100000000000000")
    assert response.status_code == 404


# Test to update a category by id
def test_put_category_by_id():
    data = {"title": "Soccer", "description": "to-do lists about soccer"}
    post_response = requests.post(BASE_URL, json=data)
    created_category = post_response.json()
    category_id = created_category["id"]

    updated_category_data = {
        "title": "Soccer!!",
        "description": "to-do lists about soccer stuff",
    }

    response = requests.put(f"{BASE_URL}/{category_id}", json=updated_category_data)

    assert response.status_code == 200
    updated_category = response.json()
    assert updated_category["title"] == "Soccer!!"
    assert updated_category["description"] == "to-do lists about soccer stuff"


# Test to update a category by id
def test_post_category_by_id():
    data = {"title": "Soccer", "description": "to-do lists about soccer"}
    post_response = requests.post(BASE_URL, json=data)
    created_category = post_response.json()
    category_id = created_category["id"]

    updated_category_data = {
        "title": "Soccer!!",
        "description": "to-do lists about soccer stuff",
    }

    response = requests.post(f"{BASE_URL}/{category_id}", json=updated_category_data)

    assert response.status_code == 200
    updated_category = response.json()
    assert updated_category["title"] == "Soccer!!"
    assert updated_category["description"] == "to-do lists about soccer stuff"


# Test to delete a category by ID
def test_delete_category_by_id():
    data = {"title": "Soccer", "description": "to-do lists about soccer"}
    post_response = requests.post(BASE_URL, json=data)
    created_category = post_response.json()
    category_id = created_category["id"]

    response = requests.delete(f"{BASE_URL}/{category_id}")

    # try to get the deleted category and make sure does not exist
    response = requests.get(f"{BASE_URL}/{category_id}")
    assert response.status_code == 404


# Get header information for a specific category
def test_head_category_by_id():
    data = {"title": "Soccer", "description": "to-do lists about soccer"}

    post_response = requests.post(BASE_URL, json=data)
    created_category = post_response.json()
    category_id = created_category["id"]

    response = requests.head(f"{BASE_URL}/{category_id}")

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"


# Test get categories for a specific category
def test_get_todos_by_category_id():
    data = {"title": "Groceries", "description": "grocery lists"}
    post_response = requests.post(BASE_URL, json=data)
    created_category = post_response.json()
    category_id = created_category["id"]

    response = requests.get(f"{BASE_URL}/{category_id}/todos")

    assert response.status_code == 200
    assert isinstance(response.json()["todos"], list)


# Test create categories for a specific category
def test_post_todos_by_category_id():
    data = {"title": "Groceries", "description": "grocery lists"}
    post_response = requests.post(BASE_URL, json=data)
    created_category = post_response.json()
    category_id = created_category["id"]

    todo_data = {"title": "Apples", "description": "2 gala, 1 delicious"}

    response = requests.post(f"{BASE_URL}/{category_id}/todos", json=todo_data)

    assert response.status_code == 201

    data = response.json()
    assert "id" in data
    assert data["title"] == "Apples"
    assert data["description"] == "2 gala, 1 delicious"


# Get header information for todos
def test_head_todos_by_category():
    data = {"title": "Groceries", "description": "grocery lists"}
    post_response = requests.post(BASE_URL, json=data)
    created_category = post_response.json()
    category_id = created_category["id"]

    response = requests.head(f"{BASE_URL}/{category_id}/todos")

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"


# Test delete category by id for a specific category
def test_delete_todo_by_id_from_category():
    data = {"title": "Groceries", "description": "grocery lists"}
    post_response = requests.post(BASE_URL, json=data)
    created_category = post_response.json()
    category_id = created_category["id"]

    todo_data = {"title": "Apples", "description": "2 gala, 1 delicious"}

    todo_response = requests.post(f"{BASE_URL}/{category_id}/todos", json=todo_data)
    todo = todo_response.json()
    todo_id = todo["id"]

    response = requests.delete(f"{BASE_URL}/{category_id}/todos/{todo_id}")
    assert response.status_code == 200

    # Try to get todo and make sure it is not there
    response = requests.get(f"{BASE_URL}/{category_id}/todos/{todo_id}")
    assert response.status_code == 404


# Test get projects for a specific category
def test_get_projects_by_category_id():
    data = {"title": "Groceries", "description": "grocery lists"}
    post_response = requests.post(BASE_URL, json=data)
    created_category = post_response.json()
    category_id = created_category["id"]

    response = requests.get(f"{BASE_URL}/{category_id}/projects")

    assert response.status_code == 200
    assert isinstance(response.json()["projects"], list)


# Test create projects for a specific category
def test_post_projects_by_category_id():
    data = {"title": "Groceries", "description": "grocery lists"}
    post_response = requests.post(BASE_URL, json=data)
    created_category = post_response.json()
    category_id = created_category["id"]

    project_data = {
        "title": "Project 1",
    }

    response = requests.post(f"{BASE_URL}/{category_id}/projects", json=project_data)

    assert response.status_code == 201

    data = response.json()
    assert "id" in data
    assert data["title"] == "Project 1"


# Get header information for projects
def test_head_projects_by_category():
    data = {"title": "Groceries", "description": "grocery lists"}
    post_response = requests.post(BASE_URL, json=data)
    created_category = post_response.json()
    category_id = created_category["id"]

    response = requests.head(f"{BASE_URL}/{category_id}/projects")

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"


# Test delete project by id for a specific category
def test_delete_project_by_id_from_category():
    data = {"title": "Groceries", "description": "grocery lists"}
    post_response = requests.post(BASE_URL, json=data)
    created_category = post_response.json()
    category_id = created_category["id"]

    project_data = {
        "title": "Project 1",
    }

    project_response = requests.post(
        f"{BASE_URL}/{category_id}/projects", json=project_data
    )
    project = project_response.json()
    project_id = project["id"]

    response = requests.delete(f"{BASE_URL}/{category_id}/projects/{project_id}")
    assert response.status_code == 200

    # Try to get project and make sure it is not there
    response = requests.get(f"{BASE_URL}/{category_id}/projects/{project_id}")
    assert response.status_code == 404


def test_options_categories():
    options_response = requests.options(f"{BASE_URL}/categories")
    assert options_response.status_code == 200


def test_options_category_by_id():
    data = {"title": "Groceries", "description": "grocery lists"}
    post_response = requests.post(BASE_URL, json=data)
    created_category = post_response.json()
    category_id = created_category["id"]

    options_response = requests.options(f"{BASE_URL}/categories/{category_id}")
    assert options_response.status_code == 200


def test_options_todos_by_category():
    data = {"title": "Groceries", "description": "grocery lists"}
    post_response = requests.post(BASE_URL, json=data)
    created_category = post_response.json()
    category_id = created_category["id"]

    options_response = requests.options(f"{BASE_URL}/categories/{category_id}/todos")
    assert options_response.status_code == 200


def test_options_todo_by_id_by_category():
    data = {"title": "Groceries", "description": "grocery lists"}
    post_response = requests.post(BASE_URL, json=data)
    created_category = post_response.json()
    category_id = created_category["id"]

    todo_data = {"title": "Apples", "description": "2 gala, 1 delicious"}

    todo_response = requests.post(f"{BASE_URL}/{category_id}/todos", json=todo_data)
    todo = todo_response.json()
    todo_id = todo["id"]

    options_response = requests.options(
        f"{BASE_URL}/categories/{category_id}/todos/{todo_id}"
    )
    assert options_response.status_code == 200


def test_options_projects_by_category():
    data = {"title": "Groceries", "description": "grocery lists"}
    post_response = requests.post(BASE_URL, json=data)
    created_category = post_response.json()
    category_id = created_category["id"]

    options_response = requests.options(f"{BASE_URL}/categories/{category_id}/projects")
    assert options_response.status_code == 200


def test_options_project_by_id_by_category():
    data = {"title": "Groceries", "description": "grocery lists"}
    post_response = requests.post(BASE_URL, json=data)
    created_category = post_response.json()
    category_id = created_category["id"]

    project_data = {
        "title": "Project 1",
    }

    project_response = requests.post(
        f"{BASE_URL}/{category_id}/projects", json=project_data
    )
    project = project_response.json()
    project_id = project["id"]

    options_response = requests.options(
        f"{BASE_URL}/categories/{category_id}/projects/{project_id}"
    )
    assert options_response.status_code == 200


# WHEN EXPECTED BEHAVIOUR FAILS


# Test to update a category by id when requesting to update id
def test_put_category_by_id_UNEXPECTED():
    data = {"title": "Soccer", "description": "to-do lists about soccer"}
    post_response = requests.post(BASE_URL, json=data)
    created_category = post_response.json()
    category_id = created_category["id"]

    updated_category_data = {"id": 100, "title": "Soccer 1"}

    response = requests.put(f"{BASE_URL}/{category_id}", json=updated_category_data)

    updated_category = response.json()
    assert updated_category["id"] == category_id  # make sure that id doesn't change
    assert response.status_code == 400


# Test to update a category by id when requesting to update id
def test_post_category_by_id_UNEXPECTED():
    data = {"title": "Soccer", "description": "to-do lists about soccer"}
    post_response = requests.post(BASE_URL, json=data)
    created_category = post_response.json()
    category_id = created_category["id"]

    updated_category_data = {"id": 100, "title": "Soccer 1"}

    response = requests.post(f"{BASE_URL}/{category_id}", json=updated_category_data)

    updated_category = response.json()
    assert updated_category["id"] == category_id  # make sure that id doesn't change
    assert response.status_code == 400


# Get header information for specific project
def test_head_project_by_id_by_category_UNEXPECTED():
    data = {"title": "Groceries", "description": "grocery lists"}
    post_response = requests.post(BASE_URL, json=data)
    created_category = post_response.json()
    category_id = created_category["id"]

    project_data = {"title": "Apples", "description": "2 gala, 1 delicious"}

    project_post_response = requests.post(
        f"{BASE_URL}/{category_id}/projects", json=project_data
    )
    created_project = project_post_response.json()
    project_id = created_project["id"]

    response = requests.head(f"{BASE_URL}/{category_id}/projects/{project_id}")

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"


# Get header information for specific todo
def test_head_todos_by_id_by_category_UNEXPECTED():
    data = {"title": "Groceries", "description": "grocery lists"}
    post_response = requests.post(BASE_URL, json=data)
    created_category = post_response.json()
    category_id = created_category["id"]

    todo_data = {"title": "Apples", "description": "2 gala, 1 delicious"}

    todo_post_response = requests.post(
        f"{BASE_URL}/{category_id}/todos", json=todo_data
    )
    created_todo = todo_post_response.json()
    todo_id = created_todo["id"]

    response = requests.head(f"{BASE_URL}/{category_id}/todos/{todo_id}")

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"


# Test get specific todo by id
def test_get_todo_by_id_by_category_UNEXPECTED():
    data = {"title": "Groceries", "description": "grocery lists"}
    post_response = requests.post(BASE_URL, json=data)
    created_category = post_response.json()
    category_id = created_category["id"]

    todo_data = {"title": "Apples", "description": "2 gala, 1 delicious"}

    todo_post_response = requests.post(
        f"{BASE_URL}/{category_id}/todos", json=todo_data
    )
    created_todo = todo_post_response.json()
    todo_id = created_todo["id"]

    response = requests.get(f"{BASE_URL}/{category_id}/todos/{todo_id}")

    assert response.status_code == 200
    todo = response.json()
    assert todo["id"] == todo_id
    assert todo["title"] == "Apples"
    assert todo["description"] == "2 gala, 1 delicious"


# Test update specific todo by id
def test_put_todo_by_id_by_category_UNEXPECTED():
    data = {"title": "Groceries", "description": "grocery lists"}
    post_response = requests.post(BASE_URL, json=data)
    created_category = post_response.json()
    category_id = created_category["id"]

    todo_data = {"title": "Apples", "description": "2 gala, 1 delicious"}

    todo_post_response = requests.post(
        f"{BASE_URL}/{category_id}/todos", json=todo_data
    )
    created_todo = todo_post_response.json()
    todo_id = created_todo["id"]

    updated_todo_data = {"title": "Apples!", "description": "2 gala, 2 delicious"}

    response = requests.get(f"{BASE_URL}/{category_id}/todos/{todo_id}")

    assert response.status_code == 200
    todo = response.json()
    assert todo["title"] == "Apples!"
    assert todo["description"] == "2 gala, 2 delicious"


# Test get specific project by id
def test_get_project_by_id_by_category_UNEXPECTED():
    data = {"title": "Groceries", "description": "grocery lists"}
    post_response = requests.post(BASE_URL, json=data)
    created_category = post_response.json()
    category_id = created_category["id"]

    project_data = {"title": "Project 1"}

    project_post_response = requests.post(
        f"{BASE_URL}/{category_id}/projects", json=project_data
    )
    created_project = project_post_response.json()
    project_id = created_project["id"]

    response = requests.get(f"{BASE_URL}/{category_id}/projects/{project_id}")

    assert response.status_code == 200
    project = response.json()
    assert project["id"] == project_id
    assert project["title"] == "Project 1"


# Test update specific project by id
def test_put_project_by_id_by_category_UNEXPECTED():
    data = {"title": "Groceries", "description": "grocery lists"}
    post_response = requests.post(BASE_URL, json=data)
    created_category = post_response.json()
    category_id = created_category["id"]

    project_data = {"title": "Project 1"}

    project_post_response = requests.post(
        f"{BASE_URL}/{category_id}/projects", json=project_data
    )
    created_project = project_post_response.json()
    project_id = created_project["id"]

    updated_project_data = {"title": "Project 2"}

    response = requests.get(f"{BASE_URL}/{category_id}/projects/{project_id}")

    assert response.status_code == 200
    project = response.json()
    assert project["title"] == "Project 2"


# Test when you give a non string value for title or description to create a category, should return and not create category
def test_get_post_categories_UNEXPECTED():
    data = {"title": 1.0, "description": False}

    response = requests.post(BASE_URL, json=data)

    assert response.status_code == 400


# Test when you give a non string value for title or description to update a category, should return and error and not update title/description
def test_get_post_categories_by_id_UNEXPECTED():
    data = {"title": "Groceries", "description": "grocery lists"}
    post_response = requests.post(BASE_URL, json=data)
    created_category = post_response.json()
    category_id = created_category["id"]

    updated_data = {"title": 1.0, "description": False}

    response = requests.post(f"{BASE_URL}/{category_id}", json=updated_data)

    assert response.status_code == 400


# Test create a project with existing id
def test_post_project_with_existing_id_UNEXPECTED():
    data = {"title": "Groceries", "description": "grocery lists"}
    post_response = requests.post(BASE_URL, json=data)
    created_category = post_response.json()
    category_id = created_category["id"]

    project_data = {"title": "Project 1"}

    project_post_response = requests.post(
        f"{BASE_URL}/{category_id}/projects", json=project_data
    )
    created_project = project_post_response.json()
    project_id = created_project["id"]

    new_project_data = {"id": project_id, "title": "Project 2"}
    response = requests.post(
        f"{BASE_URL}/{category_id}/projects", json=new_project_data
    )

    assert response.status_code == 400


# Test create a project with valid id
def test_post_project_with_valid_id_parameter_UNEXPECTED():
    data = {"title": "Groceries", "description": "grocery lists"}
    post_response = requests.post(BASE_URL, json=data)
    created_category = post_response.json()
    category_id = created_category["id"]

    project_data = {"title": "Project 1"}

    project_post_response = requests.post(
        f"{BASE_URL}/{category_id}/projects", json=project_data
    )
    created_project = project_post_response.json()
    project_id = created_project["id"]

    new_project_data = {"id": 10000, "title": "Project 2"}
    response = requests.post(
        f"{BASE_URL}/{category_id}/projects", json=new_project_data
    )

    assert response.status_code == 400


