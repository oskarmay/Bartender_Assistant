import json
import random
import secrets

from Bartender_Assistant.settings import BASE_DIR
from core.exceptions import TooManyTry
from core.models import User


def generate_user_with_password(additional_text: str = "") -> dict[str]:
    """Function generating pair of login and password for customer account."""

    with open(f"{BASE_DIR}/secrets_static/data/accounts_data.json") as json_file:
        data = json.load(json_file)

    login_data_dict = data["login"]
    password_data_dict = data["password"]

    username = [f"{additional_text.replace(' ', '')}"] if additional_text else []
    counter = 0
    while counter < 150:
        for data in login_data_dict.values():
            username.append(secrets.choice(data))
        username.append(str(random.randint(1000, 9999)))
        username = "-".join(username)

        try:
            User.objects.get(username=username)
            counter += 1
        except User.DoesNotExist:
            break

    if counter > 150:
        raise TooManyTry(
            "There was over 10 000 try to creating unique username for customer. "
            "Probably we dont have enough combination"
        )

    password = []
    for data in password_data_dict.values():
        password.append(secrets.choice(data))
    password.append(str(random.randint(1000, 9999)))
    password = "-".join(password)

    return {"login": username, "password": password}
