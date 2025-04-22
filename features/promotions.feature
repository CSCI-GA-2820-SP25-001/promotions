Feature: Promotions Management UI
  As a member of the Promotions Squad
  I want to manage promotions via the Admin UI
  So that I can control lifecycle of promotions effectively

  Background:
    Given I am on the "Promotions Page"

  Scenario: Create a new promotion
    Given I am on the "Promotions Page"
    When I enter "Spring Sale" as the promotion name
    And I set the "Promotion ID" to "SPRING001-<timestamp>"
    And I set the "Status" to "Active"
    And I set the "Amount" to "10.5"
    And I set the "Start Date" to "2025-04-23"
    And I set the "End Date" to "2025-04-30"
    And I click the "Create" button
    Then I should see a confirmation message "Promotion created successfully"
    # And I store the internal promotion ID
    When I click the "Search" button
    Then I should see "Spring Sale" in the promotion list

  
  Scenario: Retrieve a promotion by ID
    When I enter the stored internal ID
    And I click the "Retrieve" button
    Then I should see the promotion name field containing "Spring Sale"

  Scenario: Update a promotion
    When I enter the stored internal ID
    And I click the "Retrieve" button
    And I enter "Spring Sale Updated" as the promotion name
    And I click the "Update" button
    Then I should see a confirmation message "Promotion updated successfully"

  Scenario: Delete a promotion
    When I enter the stored internal ID
    And I click the "Delete" button
    Then I should see a confirmation message "Promotion has been Deleted!"

  Scenario: Search for a promotion by name
    When I enter "Spring Sale Updated" as the promotion name
    And I click the "Search" button
    Then I should see "Spring Sale Updated" in the promotion list



