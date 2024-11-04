Feature: Todo API

  # As a user, I want to create todo items so that I can add them to my todo list.

  Scenario: Adding a new todo item Success
    When I create a todo item with {"title": "TestTitle1"}
    Then the todo item should be created
    And the todo item should contain TestTitle1

  Scenario: Adding a new todo item Alternate
    When I create a todo item with {"title": "TestTitle1", "description" : "JC description test"}
    Then the todo item should be created
    And the todo item should contain TestTitle1
    And the todo item should contain JC description test

  Scenario: Adding a new todo item Error
    When I create a todo item with {}
    Then the todo item should not be created

  # As a user, I want to search for specific todo items so that I can retrieve them from my todo list.

  Scenario: Search for a todo Success
    Given I have a todo item with {"title": "TestTitle1"}
    When I search for that todo item
    Then the todo item is found and sent to me
    And the search should contain TestTitle1

  Scenario: Search for a todo Alternate
    Given I have a todo item with {"title": "TestTitle1","doneStatus": False}
    When I search for that todo item
    Then the todo item is found and sent to me
    And the search should contain false

  Scenario: Search for a todo Error
    Given I have no todo item
    When I search for a todo item with a bad id
    Then the todo item should not be found

  # As a user, I want to edit todo items from my list so that I may update their title, status or description.

  Scenario: Edit a todo item Success
    Given I have a todo item with {"title": "TestTitle1"}
    When I update that todo item with {"title": "TestTitleUpdate"}
    Then the todo item should be updated
    And the todo item should contain TestTitleUpdate

  Scenario: Edit a todo item Alternate
    Given I have a todo item with {"title": "TestTitle1", "doneStatus" : False}
    When I update that todo item with {"title": "TestTitle1", "doneStatus" : True}
    Then the todo item should be updated
    And the todo item should contain true

  Scenario: Edit a todo item Error
    Given I have no todo item
    When I update a non-existing todo item with {"title": "TestTitle1"}
    Then the todo item should not be found


  # As a user, I want to delete todo items from my list so that I may clean up my todo list.

  Scenario: Deleting a todo item Success
    Given I have a todo item with {"title": "TestTitle1"}
    When I try to delete that todo item
    Then the todo item should be deleted
    And that todo item should no longer exist

  Scenario: Deleting a todo item Alternate
    Given I have todo items
    When I try to delete all the todo items
    Then the todo items should be deleted
    And the todo item list should be empty

  Scenario: Deleting a todo item Error
    Given I have no todo item
    When I try to delete a non-existing todo item
    Then the todo item should not be found

  # As a user, I want to add categories to my todo items so that I may separate my todo items by category.

  Scenario: Adding a category to todo item Success
    Given I have a todo item with {"title": "TestTitle1"}
    When I add a category to the todo item with {"title": "TestTitle1"}
    Then the category should be created and added to the todo item
    And the category should contain TestTitle1

  Scenario: Adding a category to todo item Alternate
    Given I have a todo item with {"title": "TestTitle1"}
    When I add a category to the todo item with {"title": "TestTitle1", "description" : "JC description test"}
    Then the category should be created and added to the todo item
    And the category should contain TestTitle1
    And the category should contain JC description test

  Scenario: Adding a category to todo item Error
    Given I have no todo item
    When I add a category to a non-exsiting todo item with {"title": "TestTitle1"}
    Then the todo item should not be found
