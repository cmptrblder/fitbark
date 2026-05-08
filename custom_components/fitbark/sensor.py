
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

SENSOR_TYPES = {
    "activity": "Activity",
    "age": "Age",
    "daily_average": "Daily Average",
    "daily_goal": "Daily Goal",
    "goal_percent": "Goal %",
    "last_sync": "Last Sync",
    "gender": "Gender",
    "birthday": "Birthday",
    "primary_breed": "Primary Breed",
    "secondary_breed": "Secondary Breed",
    "status": "Status",
    "weight": "Weight",
    "location": "Location",
    "medical_conditions": "Medical Conditions",
    "timezone": "Timezone",
}

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities = []

    for dog_name in coordinator.data:
        entities.append(FitBarkPhotoSensor(coordinator, dog_name))

        for sensor_key in SENSOR_TYPES:
            entities.append(FitBarkSensor(coordinator, dog_name, sensor_key))

    async_add_entities(entities)

class FitBarkSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, dog_name, sensor_key):
        super().__init__(coordinator)

        self.dog_name = dog_name
        self.sensor_key = sensor_key

        display_name = self._dog_display_name

        self._attr_name = f"{display_name} {SENSOR_TYPES[sensor_key]}"
        self._attr_unique_id = f"{dog_name}_{sensor_key}"

    @property
    def _dog_data(self):
        return self.coordinator.data.get(self.dog_name, {})

    @property
    def _dog_display_name(self):
        return self._dog_data.get("display_name") or self.dog_name.title()

    @property
    def native_value(self):
        value = self._dog_data.get(self.sensor_key)

        if value in ["", "None", "N/A", "Unknown", None]:
            return None

        return value

    @property
    def extra_state_attributes(self):
        data = self._dog_data

        return {
            "profile_url": data.get("profile_url"),
            "slug": data.get("slug"),
            "photo": data.get("local_image"),
        }

    @property
    def device_info(self):
        data = self._dog_data
        breed = data.get("primary_breed")

        return {
            "identifiers": {("fitbark", self.dog_name)},
            "name": self._dog_display_name,
            "manufacturer": "FitBark",
            "model": breed or "Activity Tracker",
        }

class FitBarkPhotoSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, dog_name):
        super().__init__(coordinator)

        self.dog_name = dog_name

        display_name = self._dog_display_name

        self._attr_name = f"{display_name} Photo"
        self._attr_unique_id = f"{dog_name}_photo"

    @property
    def _dog_data(self):
        return self.coordinator.data.get(self.dog_name, {})

    @property
    def _dog_display_name(self):
        return self._dog_data.get("display_name") or self.dog_name.title()

    @property
    def native_value(self):
        return self._dog_data.get("local_image") or "unavailable"

    @property
    def entity_picture(self):
        return self._dog_data.get("local_image")

    @property
    def extra_state_attributes(self):
        data = self._dog_data

        return {
            "profile_url": data.get("profile_url"),
            "slug": data.get("slug"),
        }

    @property
    def device_info(self):
        data = self._dog_data
        breed = data.get("primary_breed")

        return {
            "identifiers": {("fitbark", self.dog_name)},
            "name": self._dog_display_name,
            "manufacturer": "FitBark",
            "model": breed or "Activity Tracker",
        }
