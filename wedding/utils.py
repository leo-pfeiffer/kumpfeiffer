import os
import string
import random
import csv


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
            rows.append(clean_row[:3])
    return rows
