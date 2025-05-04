from time import time
from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import re


@when('I visit the "{page}" Page')
def step_impl(context, page):
    url = context.base_url + "/"
    context.driver.get(url)
    WebDriverWait(context.driver, 10).until(EC.title_contains("Promotion"))


@when('I visit the "Promotions Page"')
def step_impl(context):
    context.driver.get(context.base_url + "/")
    assert "Promotion" in context.driver.title


@when('I copy the "ID" field')
def step_impl(context):
    context.feature_clipboard = context.driver.find_element(
        By.ID, "promotion_db_id"
    ).get_attribute("value")


@when('I paste the "ID" field')
def step_impl(context):
    field = context.driver.find_element(By.ID, "promotion_db_id")
    field.clear()
    clipboard_val = context.driver.find_element(By.ID, "id_clipboard").get_attribute(
        "value"
    )
    print(f"[Debug] Clipboard value from hidden input: '{clipboard_val}'")
    field.send_keys(context.shared_db_id)


@then('the "ID" field should be empty')
def step_impl(context):
    assert (
        context.driver.find_element(By.ID, "promotion_db_id").get_attribute("value")
        == ""
    )


@then('the "Promotion Name" field should be empty')
def step_impl(context):
    assert (
        context.driver.find_element(By.ID, "promotion_name").get_attribute("value")
        == ""
    )


@then('I should see "Spring Sale" in the "Promotion Name" field')
def step_impl(context):
    # Wait for the element to be present
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, "promotion_name"))
    )
    # Check the value of the "Promotion Name" field
    value = context.driver.find_element(By.ID, "promotion_name").get_attribute("value")
    print(f"[Debug] Promotion Name field value: '{value}'")
    assert "Spring Sale" in value


@when('I change "Promotion Name" to "Spring Sale Updated"')
def step_impl(context):
    name_field = context.driver.find_element(By.ID, "promotion_name")
    name_field.clear()
    name_field.send_keys("Spring Sale Updated")


@then('I should see "Spring Sale Updated" in the results')
def step_impl(context):
    table = context.driver.find_element(By.CSS_SELECTOR, "#search_results table")
    assert "Spring Sale Updated" in table.text


@when('I set the "{field_name}" to "{value}"')
def step_impl(context, field_name, value):
    field_id = field_name.lower().replace(" ", "_")
    input_element = context.driver.find_element(By.ID, field_id)

    if "date" in field_id:
        context.driver.execute_script(f"arguments[0].value = '{value}';", input_element)
    else:
        input_element.clear()
        input_element.send_keys(value)


@when('I select "{option}" in the "{dropdown}" dropdown')
def step_impl(context, option, dropdown):
    dropdown_id = dropdown.lower().replace(" ", "_")
    select = Select(context.driver.find_element(By.ID, dropdown_id))
    select.select_by_visible_text(option)


@when('I press the "{button}" button')
def step_impl(context, button):
    import time

    button_id = button.lower().replace(" ", "_") + "-btn"
    WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable((By.ID, button_id))
    )
    time.sleep(1)
    print(f"[Debug] Clicking button: {button} (id: {button_id})")
    context.driver.find_element(By.ID, button_id).click()


@then('I should see "{text}" in the title')
def step_impl(context, text):
    WebDriverWait(context.driver, 10).until(EC.title_contains(text))


@then('I should see the message "{message}"')
def step_impl(context, message):
    try:
        WebDriverWait(context.driver, 5).until(
            EC.text_to_be_present_in_element((By.ID, "flash_message"), message)
        )
    except Exception as e:
        flash = context.driver.find_element(By.ID, "flash_message")
        print(
            f"[Timeout Debug] flash_message content: '{flash.text}' (expecting: '{message}')"
        )
        raise e
    context.shared_db_id = context.driver.find_element(
        By.ID, "promotion_db_id"
    ).get_attribute("value")
    print(f"[Debug] Shared DB ID: {context.shared_db_id}")
    flash = context.driver.find_element(By.ID, "flash_message")
    assert message.lower() in flash.text.lower()


@when('I generate a unique Promotion ID with prefix "{prefix}"')
def step_impl(context, prefix):
    context.generated_promotion_id = f"{prefix}-{int(time())}"


@when('I set the "Promotion ID" to the generated ID')
def step_impl(context):
    promotion_id_field = context.driver.find_element(By.ID, "promotion_id")
    promotion_id_field.clear()
    promotion_id_field.send_keys(context.generated_promotion_id)
