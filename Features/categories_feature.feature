Feature: category API

  # As a user, I want to create a category so that I can group todos and projects into broader themes.

  Scenario: Create a new category Normal Flow
    When the user creates a category with {"title": "TestTitle1"}
    Then the category with {"title": "TestTitle1"} shall exist in the system

  Scenario: Create a new category Alternate Flow
    When the user creates a category with {"title": "TestTitle2", "description": "test description"}
    Then the category with {"title": "TestTitle2", "description": "test description 2"} shall exist in the system

  Scenario: Create a new category Error Flow
    When the user creates a category with {}
    Then the category shall not exist in the system 

  # As a user, I want to retrieve a specific category so that I can access its information.

  Scenario: Get a specific category Normal Flow
    Given a category with {"title": "TestTitle3"} exists in the system
    When I search for that category
    Then the category with {"title": "TestTitle3"} is found

  Scenario: Get a specific category Alternate Flow
    Given a category with {"title": "TestTitle4", "description": "test description"} exists in the system
    When I search for that category
    Then the category with {"title": "TestTitle4", "description": "test description"} is found

  Scenario: Get a specific category Error Flow
    When I search for a category with an id that does not exist
    Then no category is found

  # As a user, I want to delete a specific category so that I can get rid of categories that I don’t use anymore.

  Scenario: Delete a specific category Normal Flow 
    Given a category with {"title": "TestTitle5"} exists in the system
    When I delete that category
    Then the category gets deleted from the system

  Scenario: Delete a specific category Alternate Flow 
    Given a category with {"title": "TestTitle6", "description": "test description"} exists in the system
    When I delete that category
    Then the category gets deleted from the system

  Scenario: Delete a specific category Error Flow 
    When I attempt to delete a category with an id that does not exist
    Then the category does not get deleted

  # As a user, I want to create a todo item within a specific category so that I can organize my todo lists into broader themes.

  Scenario: Create a todo for a specific category Normal Flow
    Given a category with {"title": "TestTitle7"} exists in the system
    When I create a todo item with {"title": "TodoTitle"} for the specific category
    Then the todo item with {"title": "TodoTitle"} shall exist in the system

  Scenario: Create a todo for a specific category Alternate Flow
    Given a category with {"title": "TestTitle8"} exists in the system
    When I create a todo item with {"title": "TodoTitle2", "description": "test description"} for the specific category
    Then the todo item with {"title": "TodoTitle2", "description": "test description"} shall exist in the system

  Scenario: Create a todo for a specific category Error Flow
    When I create a todo item with {"title": "TodoTitle3"} for a specific category that does not exist
    Then the todo item with {"title": "TodoTitle3"} shall not exist in the system

  # As a user, I want to create a project within a specific category so that I can organize my projects into broader themes.

  Scenario: Create a project for a specific category Normal Flow
    Given a category with {"title": "TestTitle9"} exists in the system
    When I create a project for the specific category
    Then the project shall exist in the system

  Scenario: Create a project for a specific category Alternate Flow
    Given a category with {"title": "TestTitle10"} exists in the system
    When I create a project with {"title": "ProjTitle", "description": "test description"} for the specific category
    Then the project with {"title": "ProjTitle", "description": "test description"} shall exist in the system

  Scenario: Create a project for a specific category Error Flow
    When I create a project for a specific category that does not exist
    Then the project shall not exist in the system
