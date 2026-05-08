
import logging

from datetime import timedelta

from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .session import FitBarkSession
from .parser import parse_dashboard, parse_profile

_LOGGER = logging.getLogger(__name__)

class FitBarkCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, entry):
        super().__init__(
            hass,
            _LOGGER,
            name="fitbark",
            update_interval=timedelta(minutes=5),
        )

        self.session = FitBarkSession(
            hass,
            entry.data["username"],
            entry.data["password"],
        )

    async def _async_update_data(self):
        try:
            logged_in = await self.session.login()

            if not logged_in:
                raise UpdateFailed("FitBark login failed")

            dashboard_html = await self.session.get_dashboard_html()
            data = parse_dashboard(dashboard_html)

            for dog_name, dog_data in data.items():
                profile_url = dog_data.get("profile_url")

                if profile_url:
                    profile_html = await self.session.get_profile_html(profile_url)
                    profile_data = parse_profile(profile_html)

                    # Profile page data wins when available. Dashboard data remains as fallback.
                    for key, value in profile_data.items():
                        if value is not None:
                            dog_data[key] = value

                if not dog_data.get("primary_breed"):
                    dog_data["primary_breed"] = dog_data.get("dashboard_primary_breed")

                if not dog_data.get("secondary_breed"):
                    dog_data["secondary_breed"] = dog_data.get("dashboard_secondary_breed")

                image_url = dog_data.get("image_url")

                if image_url:
                    local_image = await self.session.download_image(
                        image_url,
                        f"{dog_name}.jpg",
                    )
                    dog_data["local_image"] = local_image

            return data or {}

        except Exception as err:
            raise UpdateFailed(str(err)) from err
