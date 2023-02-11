import re
import pytest

from wedding.models import User, Guest
from wedding.utils import generate_invite_code, read_guest_csv, validate_guest_list_rows, create_user_from_row, \
    save_guest_list_rows


INVITE_CODE_PATTERN = re.compile(r"[A-Z]{4}")


def test_generate_invite_code_has_expected_pattern():
    for _ in range(100):
        invite_code = generate_invite_code()
        assert re.fullmatch(INVITE_CODE_PATTERN, invite_code)


def test_read_guest_csv(guests_csv):
    rows = read_guest_csv(guests_csv)
    assert len(rows) == 10
    for row in rows:
        assert len(row) == 4


def test_validate_guest_list_rows_throws_exception_for_row_with_length_not_4():
    with pytest.raises(ValueError):
        validate_guest_list_rows([["1", "2", "3"]])

    with pytest.raises(ValueError):
        validate_guest_list_rows([["1", "2", "3", "4", "5"]])


def test_validate_guest_list_rows_throws_exception_for_non_boolean_last_element():
    with pytest.raises(ValueError):
        validate_guest_list_rows([["1", "2", "3", "xxx"]])


def test_validate_guest_list_rows_throws_exception_for_duplicate_guest_entries():
    rows = [
        ["1", "2", "3", "xxx"],
        ["1", "2", "3", "yyy"]
    ]
    with pytest.raises(ValueError):
        validate_guest_list_rows(rows)


def test_create_user_from_row_creates_user():
    user = create_user_from_row(["not_used", "first_name", "email", "true"])
    assert user.first_name == "first_name"
    assert user.email == "email"
    assert user.is_rehearsal_guest is True
    assert user.password is not None
    assert re.fullmatch(INVITE_CODE_PATTERN, user.username)

    # is_rehearsal_guest not True
    user = create_user_from_row(["not_used", "first_name", "email", "false"])
    assert user.is_rehearsal_guest is False


@pytest.mark.django_db
def test_save_guest_list_rows_saves_users():
    rows = [
        ["jon", "jon", "jon@mail.com", "true"],
        ["jane", "jon", "jon@mail.com", "true"]
    ]
    save_guest_list_rows(rows)
    assert User.objects.count() == 1
    assert User.objects \
        .filter(first_name="jon", email="jon@mail.com", is_rehearsal_guest=True) \
        .exists()


@pytest.mark.django_db
def test_save_guest_list_rows_saves_guests():
    rows = [
        ["jon", "jon", "jon@mail.com", "true"],
        ["jane", "jon", "jon@mail.com", "true"]
    ]
    save_guest_list_rows(rows)
    assert Guest.objects.count() == 2
    assert Guest.objects \
        .filter(primary_guest__first_name="jon", name="jon") \
        .exists()
    assert Guest.objects \
        .filter(primary_guest__first_name="jon", name="jane") \
        .exists()


@pytest.mark.django_db
def test_save_guest_list_rows_does_not_create_new_user_if_already_exists():
    rows1 = [
        ["jon", "jon", "jon@mail.com", "true"],
    ]
    rows2 = [
        ["jane", "jon", "jon@mail.com", "true"],
    ]

    save_guest_list_rows(rows1)
    assert User.objects.count() == 1
    assert Guest.objects.count() == 1

    save_guest_list_rows(rows2)
    assert User.objects.count() == 1
    assert Guest.objects.count() == 2


@pytest.mark.django_db
def test_save_guest_list_rows_does_not_create_new_guest_if_already_exists():
    rows1 = [
        ["jon", "jon", "jon@mail.com", "true"],
        ["jane", "jon", "jon@mail.com", "true"],
    ]

    rows2 = [
        ["jane", "jon", "jon@mail.com", "true"],
    ]

    save_guest_list_rows(rows1)
    assert User.objects.count() == 1
    assert Guest.objects.count() == 2

    save_guest_list_rows(rows2)
    assert User.objects.count() == 1
    assert Guest.objects.count() == 2
