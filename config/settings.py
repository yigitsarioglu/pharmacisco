import json
import os

class AppConfig:
    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self.defaults = {
            "pharmacy_name": "ALP ECZANESI",
            "pharmacy_phone": "0212 269 87 27",
            "pharmacist_name": "",
            "pharmacy_address": "",
            "printer_name": "Default",
            "label_width_mm": 60,
            "label_height_mm": 40
        }
        self.settings = self.load()

    def load(self):
        if not os.path.exists(self.config_path):
            return self.defaults.copy()
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return {**self.defaults, **json.load(f)}
        except:
            return self.defaults.copy()

    def get(self, key):
        return self.settings.get(key, self.defaults.get(key))

    def set(self, key, value):
        self.settings[key] = value
        self.save()

    def save(self):
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving config: {e}")

cfg = AppConfig()
