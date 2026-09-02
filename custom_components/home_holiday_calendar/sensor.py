"""Sensor platform for Home Holiday Calendar."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .entity import HomeHolidayCalendarEntity


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up Home Holiday Calendar sensors."""
    coordinator = entry.runtime_data
    async_add_entities([
        HolidayTodaySensor(coordinator, entry.entry_id),
        HolidayTonightSensor(coordinator, entry.entry_id),
        HolidayPreviousEveningSensor(coordinator, entry.entry_id),
        NextHolidaySensor(coordinator, entry.entry_id),
    ])


class _HolidaySensor(HomeHolidayCalendarEntity, SensorEntity):
    def __init__(self, coordinator, entry_id: str, key: str, name: str) -> None:
        super().__init__(coordinator)
        self._key = key
        self._attr_name = name
        self._attr_unique_id = f"{entry_id}_{key}"
        self._attr_icon = "mdi:calendar-star"

    @property
    def native_value(self) -> str:
        return self.coordinator.data[self._key].key

    @property
    def extra_state_attributes(self) -> dict:
        holiday = self.coordinator.data[self._key]
        attrs = {
            "display_name": holiday.display_name,
            "source": holiday.source,
            "raw_name": holiday.raw_name or "",
            "civil_date": self.coordinator.data["civil_date"],
        }
        if self._key == "tonight":
            jewish = self.coordinator.data["jewish_tonight"]
            attrs["raw_jewish_holiday_tonight"] = jewish.raw_name or ""
            attrs["normalized_jewish_holiday_tonight"] = jewish.key
        return attrs


class HolidayTodaySensor(_HolidaySensor):
    def __init__(self, coordinator, entry_id: str) -> None:
        super().__init__(coordinator, entry_id, "today", "Home Holiday Calendar Today")


class HolidayTonightSensor(_HolidaySensor):
    def __init__(self, coordinator, entry_id: str) -> None:
        super().__init__(coordinator, entry_id, "tonight", "Home Holiday Calendar Tonight")


class HolidayPreviousEveningSensor(_HolidaySensor):
    def __init__(self, coordinator, entry_id: str) -> None:
        super().__init__(
            coordinator,
            entry_id,
            "previous_evening",
            "Home Holiday Calendar Previous Evening",
        )


class NextHolidaySensor(HomeHolidayCalendarEntity, SensorEntity):
    _attr_name = "Home Holiday Calendar Next Holiday"
    _attr_icon = "mdi:calendar-arrow-right"

    def __init__(self, coordinator, entry_id: str) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry_id}_next"

    @property
    def native_value(self) -> str:
        return self.coordinator.data["next"].key

    @property
    def extra_state_attributes(self) -> dict:
        holiday = self.coordinator.data["next"]
        return {
            "display_name": holiday.display_name,
            "source": holiday.source,
            "raw_name": holiday.raw_name or "",
            "date": self.coordinator.data["next_date"],
        }
