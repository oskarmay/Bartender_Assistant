import random
import secrets


def generate_user_with_password(additional_text: str = "") -> dict[str]:
    """TODO"""
    color_list = [
        "yellow",
        "green",
        "blue",
        "violet",
        "red",
        "orange",
    ]
    animal_list = [
        "cat",
        "dog",
        "ant",
        "bird",
        "cow",
        "fish",
        "fox",
        "lion",
        "pig",
        "sheep",
        "tiger",
        "whale",
        "wolf",
        "horse",
    ]
    countries_list = [
        "chad",
        "cuba",
        "fiji",
        "iran",
        "iraq",
        "laos",
        "mali",
        "oman",
        "peru",
        "togo",
    ]
    code_list = [
        "alpha",
        "bravo",
        "charlie",
        "delta",
        "echo",
        "golf",
        "hotel",
        "india",
        "juliet",
        "kilo",
        "lima",
        "mike",
        "oscar",
        "papa",
        "romeo",
        "sierra",
        "tango",
        "victor",
        "zulu",
    ]
    # TODO Dodac sprawdzenie czy nie mamy takie uzytkownika w bazie
    random.shuffle(color_list)
    random.shuffle(animal_list)
    number = random.randint(1000, 9999)
    number2 = random.randint(1000, 9999)
    if additional_text:
        additional_text = additional_text.replace(" ", "") + "-"
    username = f"{additional_text}{secrets.choice(animal_list)}-{secrets.choice(color_list)}-{number}"
    password = f"{secrets.choice(countries_list)}{secrets.choice(code_list)}{number2}"
    return {"login": username, "password": password}
