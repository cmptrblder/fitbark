
import os

from bs4 import BeautifulSoup
from homeassistant.helpers.aiohttp_client import async_get_clientsession

BASE = "https://app.fitbark.com"
LOGIN_PAGE = f"{BASE}/web/login"
LOGIN_POST = f"{BASE}/web/login_attempt"
DASHBOARD_URL = f"{BASE}/dashboard"

class FitBarkSession:
    def __init__(self, hass, username, password):
        self.hass = hass
        self.username = username
        self.password = password
        self.session = async_get_clientsession(hass)

    async def login(self):
        await self.session.get(BASE)

        response = await self.session.get(LOGIN_PAGE)
        html = await response.text()
        soup = BeautifulSoup(html, "html.parser")

        token = soup.select_one("input[name=authenticity_token]")

        if not token:
            raise Exception("FitBark login token missing")

        payload = {
            "authenticity_token": token["value"],
            "username_or_email": self.username,
            "login_password": self.password,
        }

        login_response = await self.session.post(LOGIN_POST, data=payload)
        login_text = await login_response.text()

        if "login" in login_text.lower() and "password" in login_text.lower():
            return False

        return True

    async def get_dashboard_html(self):
        response = await self.session.get(DASHBOARD_URL)
        return await response.text()

    async def get_profile_html(self, profile_url):
        response = await self.session.get(profile_url)
        return await response.text()

    async def download_image(self, url, filename):
        if not url:
            return None

        folder = "/config/www/fitbark"
        os.makedirs(folder, exist_ok=True)

        path = os.path.join(folder, filename)

        # Keep the local file once it exists. Profile photos rarely change and this avoids hammering FitBark.
        if os.path.exists(path) and os.path.getsize(path) > 0:
            return f"/local/fitbark/{filename}"

        response = await self.session.get(url)

        if response.status != 200:
            return None

        content = await response.read()

        with open(path, "wb") as f:
            f.write(content)

        return f"/local/fitbark/{filename}"
