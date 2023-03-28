import os
import string
import random
import csv
import re
import logging

import requests
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.db.models import Q

from wedding.models import Guest, Rsvp

logger = logging.getLogger(__name__)

User = get_user_model()

INVITE_CODE_PATTERN = re.compile(r"[A-Z]{4}")


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
    First four columns must be: guest, primary guest, email, is rehearsal guest, optional: invite_code
    Header: None
    :param path: path to the csv file
    :return: list containing a list of two elements for each row
    """
    if not os.path.exists(path):
        raise ValueError(f"Path {path} does not exist")

    with open(path, "r", encoding="utf-8-sig") as file:
        reader = csv.reader(file)
        rows = []
        for row in reader:
            clean_row = [word.strip() for word in row]
            if len(clean_row) != 4 and len(clean_row) != 5:
                raise ValueError(f"Expected row length 4 or 5 but got {len(clean_row)}")
            rows.append(clean_row)

    return rows


def validate_guest_list_rows(rows: list[list[str]]):
    guest_objects = {}
    user_to_rehearsal_flag = {}
    user_key_to_invite_code = {}
    for row in rows:
        if len(row) != 4 and len(row) != 5:
            raise ValueError(
                f"Expected row to have 4 or 5 elements but got {len(row)}."
            )
        guest_name = row[0]
        email = row[2]
        rehearsal_flag = row[3]
        if rehearsal_flag.lower() not in ("true", "false"):
            raise ValueError(f"Rehearsal element must be true or false, got {row[3]}.")
        guest_key = "".join(row[:3])
        if guest_key in guest_objects:
            raise ValueError(
                f"Duplicate guest entry for guest {guest_name} of user {email}"
            )
        user_key = get_user_key_from_row(row)
        if (
            user_key in user_to_rehearsal_flag
            and user_to_rehearsal_flag[user_key] != rehearsal_flag.lower()
        ):
            raise ValueError(
                f"Got two different values for rehearsal flag for user {email}"
            )
        user_to_rehearsal_flag[user_key] = rehearsal_flag.lower()
        if len(row) == 5:
            if not re.fullmatch(INVITE_CODE_PATTERN, row[4]):
                raise ValueError(f"Invite code has wrong format: {row[4]}.")
            if user_key in user_key_to_invite_code:
                if user_key_to_invite_code[user_key] != row[4]:
                    raise ValueError(f"Got two different invite codes for user {email}")
            user_key_to_invite_code[user_key] = row[4]


def create_user_from_row(row: list[str]):
    if len(row) == 5:
        invite_code = row[4]
    else:
        invite_code = generate_invite_code()
    user = User(username=invite_code)
    user.first_name = row[1]
    user.email = row[2]
    user.is_rehearsal_guest = row[3].lower() == "true"
    user.password = make_password(invite_code)
    return user


def get_user_key_from_row(row: list[str]):
    return row[1] + row[2]


def save_guest_list_rows(rows: list[list[str]]):
    """
    Takes the rows with new user data and inserts into the DB.
    A few things are to consider here:
    - A unique USER is identified by the combination of the first_name and email.
    - If the list contains a USER that already exists in the DB, the existing user
    will NOT be updated. Instead, the existing user will be referenced.
    - If the list contains a GUEST taht already exists in the DB, the existing guest
    will NOT be updated. Instead, it's creation will be skipped.
    - If the list contains duplicate USER entries in the rows (which is expected
    when one user has multiple GUESTS) the values from the first USER entry
    are used.
    - GUESTS of one USER must have unique names.
    - All CREATE operations of this method are performed in a sinle atomic transaction.
    """
    validate_guest_list_rows(rows)

    all_users = {}
    update_users = {}
    all_guests = []
    new_guests = []

    for row in rows:
        user_key = get_user_key_from_row(row)
        if user_key not in all_users:
            user = create_user_from_row(row)
            all_users[user_key] = user

    # query for any user in the list that already exists in the DB
    existing_users = Q()
    for user in all_users.values():
        existing_users = existing_users | Q(
            first_name=user.first_name, email=user.email
        )
    existing_users_query = User.objects.filter(existing_users)

    # we need the actual user object from the DB for existing users. Store it in update_users
    for existing_user in existing_users_query.all():
        logger.info(
            f"User {existing_user.email} already exists. Keeping existing user."
        )
        user_key = existing_user.first_name + existing_user.email
        update_users[user_key] = existing_user
        all_users.pop(user_key)

    # Create the guest objects with the correct user objects
    for row in rows:
        user_key = get_user_key_from_row(row)
        user = (
            update_users[user_key] if user_key in update_users else all_users[user_key]
        )
        all_guests.append(Guest(primary_guest=user, name=row[0]))

    # query for existing guests
    existing_guests = Q()
    for guest in all_guests:
        existing_guests = existing_guests | Q(
            primary_guest=guest.primary_guest, name=guest.name
        )
    existing_guests_query = Guest.objects.filter(existing_guests)
    existing_guests_set = {
        f"{guest.name}_{guest.primary_guest_id}" for guest in existing_guests_query
    }

    # remove existing guests from the list of guests to create
    for guest in all_guests:
        if f"{guest.name}_{guest.primary_guest_id}" not in existing_guests_set:
            new_guests.append(guest)

    with transaction.atomic():
        User.objects.bulk_create(all_users.values())
        Guest.objects.bulk_create(new_guests)

    logger.info(f"Inserted {len(all_users)} User objects.")
    logger.info(f"Inserted {len(new_guests)} Guest objects.")


def get_status_update_msg():
    total_users = get_user_model().objects.filter(~Q(username="admin")).count()
    total_guests = Guest.objects.count()
    total_rsvp = Rsvp.objects.count()
    rsvp_coming = Rsvp.objects.filter(coming=True).count()
    return (
        f"Here's your update:\n"
        f"Total users: {total_users}\n"
        f"Total guests: {total_guests}\n"
        f"Total RSVPs: {total_rsvp}\n"
        f"    Coming: {rsvp_coming}\n"
        f"    Not coming: {total_rsvp - rsvp_coming}"
    )


def notify_with_ntfy(data: str):
    requests.post("https://ntfy.sh/kumpfeiffer-rsvp", data=data)
