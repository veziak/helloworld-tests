import datetime
import json

from faker import Faker
from api import put_user, get_usermessage


def random_username():
    fake = Faker()
    username = fake.simple_profile()['name'].lower().replace(' ', '')
    print(f'username: {username}')
    return username


def test_create_user():
    result = put_user(random_username(), "2018-12-12")
    assert result.status_code == 204


def test_create_user_wrong_birthday():
    result = put_user(random_username(), "2030-12-12")
    assert result.status_code == 400


def test_update_user():
    now = datetime.datetime.utcnow()
    tomorrow = now + datetime.timedelta(days=1)
    after_tomorrow = tomorrow + datetime.timedelta(days=1)

    print(f'tomorrow: {tomorrow}')
    print(f'after_tomorrow: {after_tomorrow}')
    username = random_username()

    result = put_user(username, f"{tomorrow.year - 10}-{tomorrow.month:02d}-{tomorrow.day:02d}")
    assert result.status_code == 204

    result = get_usermessage(username)
    assert result.status_code == 200
    c = json.loads(result.content)
    assert 'message' in c
    assert c['message'] == f"Hello, {username}! Your birthday is in 1 day(s)"

    result = put_user(username, f"{after_tomorrow.year - 10}-{after_tomorrow.month:02d}-{after_tomorrow.day:02d}")
    assert result.status_code == 204

    result = get_usermessage(username)
    assert result.status_code == 200
    c = json.loads(result.content)
    assert 'message' in c
    assert c['message'] == f"Hello, {username}! Your birthday is in 2 day(s)"


def test_happy_birthday_message():
    now = datetime.datetime.utcnow()
    username = random_username()

    result = put_user(username, f"{now.year - 10}-{now.month:02d}-{now.day:02d}")
    assert result.status_code == 204

    result = get_usermessage(username)
    assert result.status_code == 200
    c = json.loads(result.content)
    assert 'message' in c
    assert c['message'] == f"Hello, {username}! Happy birthday!"