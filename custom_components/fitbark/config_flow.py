
from homeassistant import config_entries
import voluptuous as vol

class FitBarkConfigFlow(config_entries.ConfigFlow, domain="fitbark"):

    async def async_step_user(self, user_input=None):

        if user_input is not None:
            return self.async_create_entry(
                title="FitBark",
                data=user_input
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("username"): str,
                vol.Required("password"): str,
            })
        )
