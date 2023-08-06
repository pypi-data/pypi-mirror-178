import os
import sys
from pathlib import Path

import pytest

test_dir = Path(__file__).parent


def pytest_addoption(parser):
    pass


def pytest_configure(config):
    sys.path.insert(0, (test_dir / "../src").absolute())
    sys.path.insert(0, (test_dir / "demo").absolute())
    os.environ["DJANGO_SETTINGS_MODULE"] = "demoapp.settings"
    sys._called_from_pytest = True


@pytest.fixture(scope="function")
def app(django_app):
    # res = django_app.get(reverse('admin:login'))
    # res.form['username'] = 'sax'
    # res.form['password'] = '123'
    # res = res.form.submit()
    return django_app


@pytest.fixture()
def user(
    db: None,
    django_user_model,
    django_username_field: str,
):
    UserModel = django_user_model
    username_field = django_username_field
    username = "user@example.com" if username_field == "email" else "user"

    try:
        user = UserModel._default_manager.get_by_natural_key(username)
    except UserModel.DoesNotExist:
        user_data = {}
        if "email" in UserModel.REQUIRED_FIELDS:
            user_data["email"] = "user@example.com"
        user_data["password"] = "password"
        user_data["is_superuser"] = False
        user_data["is_staff"] = False
        user_data[username_field] = username
        user = UserModel._default_manager._create_user(**user_data)
    return user
