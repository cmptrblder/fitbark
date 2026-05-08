
import re
from bs4 import BeautifulSoup

BASE_URL = "https://app.fitbark.com"

def parse_dashboard(html):
    soup = BeautifulSoup(html, "html.parser")
    dogs = {}

    for row in soup.select("tr.dog-line"):
        cols = [c.get_text(strip=True) for c in row.select("td")]

        if len(cols) < 10:
            continue

        name = cols[2].strip()
        if not name:
            continue

        dog_key = slugify(name)

        dogs[dog_key] = {
            "display_name": name,
            "slug": row.get("data-dogslug"),
            "profile_url": absolute_url(row.get("data-href")),
            "activity": clean(cols[7]),
            "age": clean(cols[5]),
            "daily_average": clean(cols[8]),
            "daily_goal": clean(cols[9]),
            "last_sync": clean(cols[6]),
            "goal_percent": calc_goal(cols[7], cols[9]),
        }

        image_cell = row.select_one(".td-dog-image")
        if image_cell:
            style = image_cell.get("style", "")
            m = re.search(r"url\(['\"]?([^'\")]+)", style)
            if m:
                dogs[dog_key]["image_url"] = absolute_url(m.group(1))

    return dogs

def parse_profile(html):
    soup = BeautifulSoup(html, "html.parser")

    profile = {}

    gender_input = soup.select_one('input[name="gender"]')
    if gender_input:
        gender_value = gender_input.get("value")
        if gender_value == "M":
            profile["gender"] = "Male"
        elif gender_value == "F":
            profile["gender"] = "Female"

    neutered_input = soup.select_one('input[name="neutered"]')
    if neutered_input:
        value = neutered_input.get("value")
        profile["status"] = "Neutered" if value == "true" else "Intact"

    breed1 = soup.select_one('input[name="dog_breed1_id"]')
    if breed1:
        profile["primary_breed"] = clean(breed1.get("value"))

    breed2 = soup.select_one('input[name="dog_breed2_id"]')
    if breed2:
        profile["secondary_breed"] = clean(breed2.get("value"))

    weight = soup.select_one('input[name="dog_weight"]')
    if weight:
        profile["weight"] = clean(weight.get("value"))

    med = soup.select_one('input[name="medical_conditions"]')
    if med:
        profile["medical_conditions"] = clean(med.get("value"))

    country = soup.select_one('input[name="country"]')
    zipcode = soup.select_one('input[name="zip"]')
    location_parts = []

    if country and clean(country.get("value")):
        location_parts.append(country.get("value"))

    if zipcode and clean(zipcode.get("value")):
        location_parts.append(zipcode.get("value"))

    if location_parts:
        profile["location"] = " ".join(location_parts)

    goal = soup.select_one('input[name="daily_goal"]')
    if goal:
        profile["daily_goal"] = clean(goal.get("value"))

    month = soup.select_one('input[name="dog_birth_2i_"]')
    day = soup.select_one('input[name="dog_birth_3i_"]')
    year = soup.select_one('input[name="dog_birth_1i_"]')

    if month and day and year:
        profile["birthday"] = f'{month.get("value")}/{day.get("value")}/{year.get("value")}'

    timezone = soup.select_one('#dog_tzname option[selected]')
    if timezone:
        profile["timezone"] = clean(timezone.get_text(" ", strip=True))

    return profile

def absolute_url(url):
    if not url:
        return None

    if url.startswith("http"):
        return url

    if not url.startswith("/"):
        url = "/" + url

    return BASE_URL + url

def clean(value):
    if value is None:
        return None

    value = str(value).strip()

    if value.lower() in ["none", "n/a", "unknown", ""]:
        return None

    return value

def calc_goal(activity, goal):
    try:
        activity = float(str(activity).replace(",", ""))
        goal = float(str(goal).replace(",", ""))

        if goal == 0:
            return None

        return round((activity / goal) * 100, 1)
    except Exception:
        return None

def slugify(name):
    return re.sub(r'[^a-z0-9]+', '_', name.lower()).strip('_')
