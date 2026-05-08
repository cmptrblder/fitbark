# FitBark Home Assistant Integration

A custom Home Assistant integration that scrapes activity and profile data directly from the FitBark web dashboard.

This integration was built specifically for users who want FitBark data inside Home Assistant without relying on the limited official API.

---
# Screenshots

<img width="222" height="617" alt="Screenshot 2026-05-08 at 5 41 23 PM" src="https://github.com/user-attachments/assets/7ace366f-cdfc-4c71-868b-692d1ad33f53" />
<img width="702" height="323" alt="Screenshot 2026-05-08 at 5 40 45 PM" src="https://github.com/user-attachments/assets/9dd3f5f4-cfcd-45bc-a7a0-7e6a30ba1374" />
<img width="234" height="98" alt="Screenshot 2026-05-08 at 5 40 27 PM" src="https://github.com/user-attachments/assets/a324dd5a-3e30-4027-885d-5ab0b18391c9" />


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
