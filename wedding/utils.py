import os
import string
import random
import csv

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()


def generate_invite_code() -> str:
    """
    Generate an alphanumeric invite code of length 6
    :return: invite code
    """
    alphabet = string.ascii_letters + string.digits
    code = []
    for i in range(6):
        code.append(random.choice(alphabet))
    return "".join(code)


def read_guest_csv(path: str) -> list:
    """
    Read guest list from a csv file.
    First three columns must be: name, email, max_guests
    Header: None
    :param path: path to the csv file
    :return: list containing a list of two elements for each row
    """
    assert os.path.exists(path)
    with open(path, "r") as file:
        reader = csv.reader(file)
        rows = []
        for row in reader:
            clean_row = [word.strip() for word in row]
            if len(clean_row) >= 5:
                rows.append(clean_row[:5])
    return rows


def save_guest_list_rows(rows: list[list[str]]):
    for row in rows:
        if len(row) < 4:
            continue

        invite_code = generate_invite_code()
        user = User(username=invite_code)
        user.first_name = row[0]
        user.preferred_name = row[1]
        user.email = row[2]
        user.max_guests = row[3]  # todo remove
        user.is_rehearsal_guest = row[4] == "true"
        user.password = make_password(invite_code)
        user.save()
