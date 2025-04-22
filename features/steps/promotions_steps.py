from behave import given, when, then
from selenium.webdriver.common.by import By
import time


@given('I am on the "Promotions Page"')
def step_impl(context):
    context.driver.get(context.base_url + "/")
    time.sleep(1)
    assert "Promotion" in context.driver.title


@when('I enter "{text}" as the promotion name')
def step_impl(context, text):
    name_input = context.driver.find_element(By.ID, "promotion_name")
    name_input.clear()
    name_input.send_keys(text)


@when('I set the "Promotion ID" to "{promotion_id}"')
def step_impl(context, promotion_id):
    unique_id = f"{promotion_id}-{int(time.time() % 10000)}"
    field = context.driver.find_element(By.ID, "promotion_id")
    field.clear()
    field.send_keys(unique_id)
    context.promotion_id = unique_id


@when("I store the current promotion ID")
def step_impl(context):
    field = context.driver.find_element(By.ID, "promotion_id")
    context.promotion_id = field.get_attribute("value")


@when("I enter the stored promotion ID")
def step_impl(context):
    field = context.driver.find_element(By.ID, "promotion_id")
    field.clear()
    field.send_keys(context.promotion_id)


@when('I set the "Status" to "{status}"')
def step_impl(context, status):
    dropdown = context.driver.find_element(By.ID, "state")
    for option in dropdown.find_elements(By.TAG_NAME, "option"):
        if option.text.lower() == status.lower():
            option.click()
            break


@when('I set the "Amount" to "{amount}"')
def step_impl(context, amount):
    input_box = context.driver.find_element(By.ID, "amount")
    input_box.clear()
    input_box.send_keys(amount)


@when('I set the "Start Date" to "{start_date}"')
def step_impl(context, start_date):
    field = context.driver.find_element(By.ID, "start_date")
    context.driver.execute_script(f"arguments[0].value = '{start_date}';", field)


@when('I set the "End Date" to "{end_date}"')
def step_impl(context, end_date):
    field = context.driver.find_element(By.ID, "end_date")
    context.driver.execute_script(f"arguments[0].value = '{end_date}';", field)


@when('I click the "Create" button')
def step_impl(context):
    context.driver.find_element(By.ID, "create-btn").click()
    time.sleep(1)


# @when("I store the internal promotion ID")
# def step_impl(context):
#     field = context.driver.find_element(By.ID, "promotion_db_id")
#     context.internal_id = field.get_attribute("value")


# @then("I store the internal promotion ID")
# def step_impl(context):
#     field = context.driver.find_element(By.ID, "promotion_db_id")
#     context.internal_id = field.get_attribute("value")
#     print("[Debug] Stored internal ID:", context.internal_id)


@then('I should see a confirmation message "{message}"')
def step_impl(context, message):
    flash_message = context.driver.find_element(By.ID, "flash_message")
    print("[Debug] Flash message text is:", flash_message.text)
    assert message.lower() in flash_message.text.lower()


@when("I enter the stored internal ID")
def step_impl(context):
    field = context.driver.find_element(By.ID, "promotion_id")
    field.clear()
    field.send_keys(context.internal_id)


@when('I click the "Search" button')
def step_impl(context):
    context.driver.find_element(By.ID, "search-btn").click()
    time.sleep(1)


@then('I should see "{name}" in the promotion list')
def step_impl(context, name):
    table = context.driver.find_element(By.CSS_SELECTOR, "#search_results table")
    print("[Debug] Table text:", table.text)
    assert name in table.text


@when('I enter "{id}" as the promotion ID')
def step_impl(context, id):
    field = context.driver.find_element(By.ID, "promotion_id")
    field.clear()
    field.send_keys(id)


@when('I click the "Retrieve" button')
def step_impl(context):
    context.driver.find_element(By.ID, "retrieve-btn").click()
    time.sleep(1)


@when('I click the "Update" button')
def step_impl(context):
    context.driver.find_element(By.ID, "update-btn").click()
    time.sleep(1)


@when('I click the "Delete" button')
def step_impl(context):
    context.driver.find_element(By.ID, "delete-btn").click()
    time.sleep(1)


@then('I should see the promotion name field containing "{text}"')
def step_impl(context, text):
    name_field = context.driver.find_element(By.ID, "promotion_name")
    print("[Debug] Expected:", text)
    print("[Debug] Actual:", name_field.get_attribute("value"))
    assert text in name_field.get_attribute("value")
