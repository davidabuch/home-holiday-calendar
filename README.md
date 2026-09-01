# Home Holiday Calendar

A local Home Assistant custom integration that normalizes common Gregorian and Jewish holidays into stable, automation-friendly entities.

## Initial entities

- `sensor.home_holiday_calendar_today`
- `sensor.home_holiday_calendar_tonight`
- `sensor.home_holiday_calendar_next_holiday`
- `binary_sensor.home_holiday_calendar_holiday_tonight`

Entity IDs may receive a numeric suffix if conflicting entities already exist.

## Important semantic distinction

`Tonight` is deliberately forward-looking. For Jewish holidays it evaluates the Hebrew date that begins after sunset on the current civil date. This makes it safe to use with automations that start before sunset, such as holiday lighting at sunset minus two hours.

## Gregorian holidays currently normalized

- New Year (Dec 31 and Jan 1)
- Valentine's Day
- St. Patrick's Day
- Independence Day
- Halloween
- Thanksgiving (fourth Thursday of November)
- Christmas (Dec 24 and Dec 25)

## Jewish holidays currently normalized

When reported by `pyluach`:

- Hanukkah
- Purim
- Passover
- Shavuot
- Rosh Hashanah
- Yom Kippur
- Sukkot
- Shemini Atzeret
- Simchat Torah
- Lag BaOmer
- Tu BiShvat
- Tu B'Av
- Purim Katan
- Shushan Purim
- Pesach Sheni

## Design boundary

The integration intentionally contains no Hue, scene, lighting, sports, or Home Lighting Manager behavior. It only provides holiday intelligence that other Home Assistant automations can consume.

## Installation

Copy `custom_components/home_holiday_calendar` into your Home Assistant `/config/custom_components/` directory, restart Home Assistant, then add **Home Holiday Calendar** from **Settings → Devices & services → Add Integration**.

Leave **Use Israel Jewish holiday schedule** disabled for the diaspora schedule used in the United States.

## Version

Current integration version: **0.1.0**
