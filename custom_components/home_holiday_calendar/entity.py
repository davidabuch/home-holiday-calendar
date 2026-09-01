"""Base entity for Home Holiday Calendar."""

from __future__ import annotations

from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import HomeHolidayCalendarCoordinator


class HomeHolidayCalendarEntity(CoordinatorEntity[HomeHolidayCalendarCoordinator]):
    """Base Home Holiday Calendar entity."""

    _attr_has_entity_name = False
