"""Tests for the pure holiday calculation engine."""

from datetime import date

from custom_components.home_holiday_calendar.holiday_engine import resolve_tonight


def test_fixed_holidays() -> None:
    assert resolve_tonight(date(2026, 1, 1)).key == "new_year"
    assert resolve_tonight(date(2026, 2, 14)).key == "valentines_day"
    assert resolve_tonight(date(2026, 3, 17)).key == "st_patricks_day"
    assert resolve_tonight(date(2026, 7, 4)).key == "july_4"
    assert resolve_tonight(date(2026, 10, 31)).key == "halloween"
    assert resolve_tonight(date(2026, 12, 24)).key == "christmas"
    assert resolve_tonight(date(2026, 12, 25)).key == "christmas"
    assert resolve_tonight(date(2026, 12, 31)).key == "new_year"


def test_thanksgiving() -> None:
    assert resolve_tonight(date(2026, 11, 26)).key == "thanksgiving"


def test_2026_hanukkah_evenings() -> None:
    for day in range(4, 12):
        assert resolve_tonight(date(2026, 12, day)).key == "hanukkah"
    assert resolve_tonight(date(2026, 12, 12)).key == "none"
