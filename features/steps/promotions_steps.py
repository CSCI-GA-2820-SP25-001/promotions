from time import time
import requests
from compare3 import expect
from behave import given, when, then

API_URL = "http://localhost:8081/promotions"


@given("the promotion service is available")
def step_impl(context):
    response = requests.get(API_URL)
    expect(response.status_code).to_equal(200)


@when('I create a promotion with name "{name}" and ID prefix "{pid_prefix}"')
def step_impl(context, name, pid_prefix):
    unique_pid = f"{pid_prefix}-{int(time())}"
    context.promotion_id = unique_pid
    payload = {
        "name": name,
        "promotion_id": unique_pid,
        "start_date": "2025-04-23",
        "end_date": "2025-04-30",
        "promotion_type": "DISCOUNT",
        "promotion_amount": 10.0,
        "promotion_description": "Seasonal discount for all items",
        "usage_count": 100,
        "state": "Active",
    }
    context.response = requests.post(API_URL, json=payload)
    expect(context.response.status_code).to_equal(201)
    context.result = context.response.json()
    context.id = context.result["id"]


@then("the response code should be {code:d}")
def step_impl(context, code):
    expect(context.response.status_code).to_equal(code)


@then('the response should contain name "{name}"')
def step_impl(context, name):
    expect(context.result["name"]).to_equal(name)


@then('the response should contain promotion ID "{pid}"')
def step_impl(context, pid):
    expect(context.result["promotion_id"]).to_equal(pid)


@when("I retrieve the promotion by database ID")
def step_impl(context):
    context.response = requests.get(f"{API_URL}/{context.id}")
    expect(context.response.status_code).to_equal(200)
    context.result = context.response.json()


@when("I delete the promotion by database ID")
def step_impl(context):
    context.response = requests.delete(f"{API_URL}/{context.id}")
    expect(context.response.status_code).to_equal(204)


@then("the promotion should not be found")
def step_impl(context):
    response = requests.get(f"{API_URL}/{context.id}")
    expect(response.status_code).to_equal(404)
