import requests
from compare3 import expect
from behave import given, when, then

API_URL = "http://localhost:8081/api/promotions"


@given("the promotion service is available")
def step_impl(context):
    response = requests.get(API_URL)
    expect(response.status_code).to_equal(200)


@when('I create a promotion with name "{name}" and ID "{pid}"')
def step_impl(context, name, pid):
    payload = {
        "name": name,
        "promotion_id": pid,
        "amount": 10.5,
        "start_date": "2025-04-23",
        "end_date": "2025-04-30",
        "state": "Active",
        "description": "Seasonal discount",
        "discount_type": "FLASH",
        "usage_count": 100,
    }
    context.response = requests.post(API_URL, json=payload)
    context.result = context.response.json()


@then("the response code should be {code:d}")
def step_impl(context, code):
    expect(context.response.status_code).to_equal(code)


@then('the response should contain name "{name}"')
def step_impl(context, name):
    expect(context.result["name"]).to_equal(name)


@then('the response should contain promotion ID "{pid}"')
def step_impl(context, pid):
    expect(context.result["promotion_id"]).to_equal(pid)


@when('I retrieve the promotion by ID "{pid}"')
def step_impl(context, pid):
    context.response = requests.get(f"{API_URL}/{pid}")
    context.result = context.response.json()


@when('I delete the promotion with ID "{pid}"')
def step_impl(context, pid):
    context.response = requests.delete(f"{API_URL}/{pid}")
