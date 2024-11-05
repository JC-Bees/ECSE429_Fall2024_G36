Feature: Projects API 

#As a user, I want to retrieve a specific project so that I can access its information

Scenario: Retrieving a project with ID
    Given I have a project item with {"title": "projectTitle"}
    When I search for that project
    Then the project is found and sent to me
    And the project search should contain projectTitle

Scenario: Retrieving a project with the get all method
    Given I have a project item with {"title": "projectTitle"}
    When I search for that project item with the get all projects method
    Then the projects should be sent to me
    And the projects should contain the project item title projectTitle

Scenario: Retrieving a project with no specified ID
    Given that I am searching for a project but without its ID {}
    When I search for that project without an ID
    Then I should get an error message telling me to specify the project ID

#As a user, I want to add a category to my project, so that I may differentiate my projects by category

Scenario: Adding a category to my project
    Given that I have a category item {"title": "categoryTitle"} that I want to relate to a project item {"title": "projectTitle"}
    When I add a relation between the category and project
    Then the project information should contain the category and its information {"title": "categoryTitle"}

Scenario: Adding multiple categories to my project
    Given that I have two category items {"title": "categoryTitle1"}, {"title": "categoryTitle2"} that I want to relate to a project item {"title": "projectTitle"}
    When I add a relation between the categories and project
    Then the project information should contain the category IDs

Scenario: Try realting a non existing category to a project
    Given that i have a project item {"title": "projectTitle"} and a category item that is invalid {}
    When I try to relate the category to the project 
    Then I should get an error message telling me Could not find thing matching value for id

#As a developper, I want to be able to retrieve the metadata of projects, so that I can ensure that the specific ressources are available

Scenario: Retrieving the header of a single project
    Given that I have a project item {"title": "projectTitle"} whos header I want to retrieve
    When I retrieve the metadata
    Then everything shoud look fine and the content should be of type application/json

Scenario: Retrieving the header of all available projects
    Given that I have a project item {"title": "projectTitle1"} and another project item of {"title": "projectTitle2"}
    When I retrieve the metadata for those specific projects 
    Then everything should be fine and the content should be of type application/json

Scenario: Retrieving the header with an invalid project ID
    Given that I have a project item {} whos project ID is invalid
    When I try to retrieve the metadata for the invalid project
    Then I should be notified that an error has occured by the status code 404

#As a user, I want to remove a specific category from a project so that I can better tailor the project to fit my needs.

Scenario: Removing a specific category from a project
    Given that I have a specific project item {"title": "projectTitle"} that is related to a specific category item {"title": "categoryTitle"}
    When I try to delete the relationship between the project and the category
    Then I should not see that category in the project information

Scenario: Removing all categories from a project
    Given that I have a specific project item {"title": "projectTitle"} that is related to multiple specific category items {"title": "categoryTitle1"}, {"title": "categoryTitle2"}
    When I try to delete the relationship between the project and the multiple categories 
    Then the category information should not be present in the project information

Scenario: Removing a category with an invalid Id from a project
    Given that i have a specific project item {"title": "projectTitle"} and an invalid category ID {}
    When I try to delete the relationship between the category and the project
    Then I should be notified that no category wa sable to be found

#As a user, I want to add specific tasks to my projects so that I can organize my work in a more efficient manner

Scenario: Adding a task to a project 
    Given a specific project item {"title": "projectTitle"} and a specific task item {"title": "taskTitle"}
    When I try to add the specific task to the project 
    Then the tasks information should not be present in the projects information

Scenario: Adding multiple tasks to a project
    Given a specific project item {"title": "projectTitle"} and multiple specific task items {"title": "taskTitle1"}, {"title": "taskTitle2"}
    When I try to add the specific task items to the project 
    Then the multiple task item information should not be present in the projects information

Scenario: Trying to add an invalid task to a project
    Given a specific project item {"title": "projectTitle"} and an invalid specific task item {}
    When I try to add the specific invalid task item to the project
    Then I should get an error saying no specific task item of such was found