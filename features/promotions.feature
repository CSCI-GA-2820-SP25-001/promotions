Feature: Promotions Management UI
  As a member of the Promotions Squad
  I want to manage promotions via the Admin UI
  So that I can control lifecycle of promotions effectively

Background:
    When I visit the "Promotions Page"

Scenario: Full Promotion Lifecycle
  When I visit the "Promotions Page"
  And I generate a unique Promotion ID with prefix "spring-sale"
  And I set the "Promotion Name" to "Spring Sale"
  And I set the "Promotion ID" to the generated ID
  And I select "Active" in the "State" dropdown
  And I set the "Amount" to "10.5"
  And I set the "Start Date" to "2025-04-23"
  And I set the "End Date" to "2025-04-30"
  And I set the "Description" to "Seasonal discount for all items"
  And I select "DISCOUNT" in the "Type" dropdown
  And I set the "Usage" to "100"
  And I press the "Create" button
  Then I should see the message "Promotion created successfully"

  When I copy the "ID" field
  And I press the "Clear" button
  Then the "ID" field should be empty
  And the "Promotion Name" field should be empty

  When I paste the "ID" field
  And I press the "Retrieve" button
  Then I should see the message "Promotion retrieved successfully"
  And I should see "Spring Sale" in the "Promotion Name" field

  When I change "Promotion Name" to "Spring Sale Updated"
  And I press the "Update" button
  Then I should see the message "Promotion updated successfully"

  When I press the "Search" button
  Then I should see the message "Promotion found"
  And I should see "Spring Sale Updated" in the results

  When I press the "Delete" button
  Then I should see the message "Promotion has been Deleted!"

