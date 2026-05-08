# FitBark Home Assistant Integration

A custom Home Assistant integration that scrapes activity and profile data directly from the FitBark web dashboard.

This integration was built specifically for users who want FitBark data inside Home Assistant without relying on the limited official API.

---

# Features

## Dashboard Activity Scraping

Includes:
- Activity
- Daily Average
- Daily Goal
- Goal Percentage
- Last Sync
- Age

## Multi-Dog Support

Automatically creates separate devices/entities for each dog.

## Profile Page Scraping

Includes:
- Gender
- Birthday
- Primary Breed
- Secondary Breed
- Status
- Weight
- Location
- Timezone
- Medical Conditions

## Local Image Caching

Dog profile images are cached locally under:

/config/www/fitbark/

## Config Flow Support

UI-based Home Assistant setup.
No YAML required.

---

# Installation

1. Copy the fitbark folder into:

/config/custom_components/

2. Restart Home Assistant

3. Add the integration from:
Settings → Devices & Services

---

# Disclaimer

This project is unofficial and not affiliated with or endorsed by FitBark.
