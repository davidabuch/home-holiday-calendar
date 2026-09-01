"""Tests for the pure holiday calculation engine."""

from datetime import date

from custom_components.home_holiday_calendar.holiday_engine import (
    gregorian_holiday,
    resolve_tonight,
)


def test_fixed_holidays() -> None:
    assert resolve_tonight(date(2026, 1, 1)).key == "new_year"
    assert resolve_tonight(date(2026, 2, 14)).key == "valentines_day"
    assert resolve_tonight(date(2026, 3, 17)).key == "st_patricks_day"
    assert resolve_tonight(date(2026, 10, 31)).key == "halloween"
    assert resolve_tonight(date(2026, 12, 24)).key == "christmas"
    assert resolve_tonight(date(2026, 12, 25)).key == "christmas"
    assert resolve_tonight(date(2026, 12, 31)).key == "new_year"


def test_thanksgiving_actual_date_remains_literal() -> None:
    assert gregorian_holiday(date(2026, 11, 25)).key == "none"
    assert gregorian_holiday(date(2026, 11, 26)).key == "thanksgiving"
    assert gregorian_holiday(date(2026, 11, 27)).key == "none"


def test_thanksgiving_observance_is_wednesday_through_sunday() -> None:
    assert resolve_tonight(date(2026, 11, 24)).key != "thanksgiving"
    for day in range(25, 30):
        assert resolve_tonight(date(2026, 11, day)).key == "thanksgiving"
    assert resolve_tonight(date(2026, 11, 30)).key != "thanksgiving"


def test_july_4_saturday_observance_is_friday_through_sunday() -> None:
    # 2026-07-04 is Saturday.
    assert resolve_tonight(date(2026, 7, 2)).key != "july_4"
    for day in (3, 4, 5):
        assert resolve_tonight(date(2026, 7, day)).key == "july_4"
    assert resolve_tonight(date(2026, 7, 6)).key != "july_4"


def test_july_4_friday_observance_is_friday_through_sunday() -> None:
    # 2025-07-04 is Friday.
    for day in (4, 5, 6):
        assert resolve_tonight(date(2025, 7, day)).key == "july_4"
    assert resolve_tonight(date(2025, 7, 3)).key != "july_4"
    assert resolve_tonight(date(2025, 7, 7)).key != "july_4"


def test_july_4_sunday_observance_is_saturday_through_sunday() -> None:
    # 2027-07-04 is Sunday.
    assert resolve_tonight(date(2027, 7, 2)).key != "july_4"
    assert resolve_tonight(date(2027, 7, 3)).key == "july_4"
    assert resolve_tonight(date(2027, 7, 4)).key == "july_4"
    assert resolve_tonight(date(2027, 7, 5)).key != "july_4"


def test_july_4_midweek_observance_is_actual_date_only() -> None:
    # 2028-07-04 is Tuesday.
    assert resolve_tonight(date(2028, 7, 3)).key != "july_4"
    assert resolve_tonight(date(2028, 7, 4)).key == "july_4"
    assert resolve_tonight(date(2028, 7, 5)).key != "july_4"


def test_2026_hanukkah_evenings() -> None:
    for day in range(4, 12):
        assert resolve_tonight(date(2026, 12, day)).key == "hanukkah"
    assert resolve_tonight(date(2026, 12, 12)).key == "none"


def test_christmas_wins_if_jewish_holiday_overlaps() -> None:
    assert resolve_tonight(date(2026, 12, 24)).key == "christmas"
    assert resolve_tonight(date(2026, 12, 25)).key == "christmas"
