# Home Holiday Calendar

A local Home Assistant custom integration that normalizes common Gregorian and Jewish holidays into stable, automation-friendly entities.

## Entities

Current entities include:

- `sensor.home_holiday_calendar_today`
- `sensor.home_holiday_calendar_tonight`
- `sensor.home_holiday_calendar_previous_evening`
- `sensor.home_holiday_calendar_next_holiday`
- `binary_sensor.home_holiday_calendar_holiday_tonight`

Entity IDs may receive a numeric suffix if conflicting entities already exist.

## Important semantic distinction

### Today

`Today` represents the actual civil-date holiday.

### Tonight

`Tonight` is automation-friendly and deliberately forward-looking.

For Jewish holidays it evaluates the Hebrew date that begins after sunset on the current civil date.

For selected Gregorian holidays it can also represent an agreed observance window broader than the literal holiday date.

This supports automations that begin before sunset without changing the meaning of the actual civil-date holiday.

### Previous Evening

`Previous Evening` reports the holiday observance associated with the previous civil evening.

This exists primarily for restart-safe automation behavior after midnight. A consumer can reconstruct an observance that began the prior evening even if Home Assistant restarted after the civil date changed.

The calendar itself does not impose an automation end time; consumers decide how long the previous evening remains authoritative.

## Gregorian holidays currently normalized

- New Year
- Valentine's Day
- St. Patrick's Day
- Independence Day
- Halloween
- Thanksgiving
- Christmas

### Automation observance windows

Thanksgiving:

- Wednesday through Sunday of Thanksgiving week

Independence Day:

- Monday-Thursday July 4: July 4 only
- Friday July 4: Friday through Sunday
- Saturday July 4: Friday through Sunday
- Sunday July 4: Saturday through Sunday

Other supported Gregorian holidays currently use their actual civil date.

Gregorian observance has priority over Jewish holiday state for `Tonight`, preserving the policy that Christmas wins on Dec 24-25 if holidays overlap.

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

Home Holiday Calendar intentionally contains **no Hue, scene, lighting, sports, or Home Lighting Manager behavior**.

It only provides holiday intelligence that other Home Assistant automations can consume.

## Installation

Copy:

`custom_components/home_holiday_calendar`

into:

`/config/custom_components/home_holiday_calendar`

Restart Home Assistant, then add **Home Holiday Calendar** from:

**Settings -> Devices & services -> Add Integration**

Leave **Use Israel Jewish holiday schedule** disabled for the diaspora schedule used in the United States.
