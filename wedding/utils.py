import os
import string
import random
import csv

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from wedding.models import Guest

User = get_user_model()


def generate_invite_code() -> str:
    """
    Generate an alphanumeric invite code of length 6
    :return: invite code
    """
    alphabet = string.ascii_uppercase
    code = []
    for i in range(4):
        code.append(random.choice(alphabet))
    return "".join(code)


def read_guest_csv(path: str) -> list:
    """
    Read guest list from a csv file.
    First four columns must be: guest, primary guest, email, is rehearsal guest
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
            if len(clean_row) >= 4:
                rows.append(clean_row[:4])
    return rows


def save_guest_list_rows(rows: list[list[str]]):
    seen_users = {}

    for row in rows:
        if len(row) < 4:
            continue

        first_name = row[1]
        email = row[2]
        is_rehearsal_guest = row[3].lower() == "true"
        user_key = first_name + email

        # create user
        if not user_key in seen_users:
            invite_code = generate_invite_code()
            user = User(username=invite_code)
            user.first_name = first_name
            user.email = email
            user.is_rehearsal_guest = is_rehearsal_guest
            user.password = make_password(invite_code)
            user.save()
            seen_users[user_key] = user

        # get existing user from seen_users
        else:
            user = seen_users[user_key]

        # create guest
        guest = Guest()
        guest.primary_guest = user
        guest.name = row[0]
        guest.save()
