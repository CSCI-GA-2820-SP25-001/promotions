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


@when('I copy the "Promotion ID" field')
def step_impl(context):
    context.clipboard = context.driver.find_element(
        By.ID, "promotion_id"
    ).get_attribute("value")


@then('the "Promotion ID" field should be empty')
def step_impl(context):
    assert (
        context.driver.find_element(By.ID, "promotion_id").get_attribute("value") == ""
    )


@then('the "Promotion Name" field should be empty')
def step_impl(context):
    assert (
        context.driver.find_element(By.ID, "promotion_name").get_attribute("value")
        == ""
    )


@when('I paste the "Promotion ID" field')
def step_impl(context):
    context.driver.find_element(By.ID, "promotion_id").send_keys(context.clipboard)


@then('I should see "Spring Sale" in the "Promotion Name" field')
def step_impl(context):
    value = context.driver.find_element(By.ID, "promotion_name").get_attribute("value")
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
    input_element.clear()
    input_element.send_keys(value)


@when('I select "{option}" in the "{dropdown}" dropdown')
def step_impl(context, option, dropdown):
    dropdown_id = dropdown.lower().replace(" ", "_")
    select = Select(context.driver.find_element(By.ID, dropdown_id))
    select.select_by_visible_text(option)


@when('I press the "{button}" button')
def step_impl(context, button):
    button_id = button.lower().replace(" ", "_") + "-btn"
    context.driver.find_element(By.ID, button_id).click()


@then('I should see "{text}" in the title')
def step_impl(context, text):
    WebDriverWait(context.driver, 10).until(EC.title_contains(text))


@then('I should see the message "{message}"')
def step_impl(context, message):
    # 等待 flash_message 元素包含目标文本
    WebDriverWait(context.driver, 5).until(
        EC.text_to_be_present_in_element((By.ID, "flash_message"), message)
    )
    flash = context.driver.find_element(By.ID, "flash_message")
    print(f"[Debug] Flash message: {flash.text}")
    assert message.lower() in flash.text.lower()
