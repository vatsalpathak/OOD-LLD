class AppConfig:
    # Your Singleton setup
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print("\n[AppConfig] Creating new App instance.")
            cls._instance = super().__new__(cls)
            cls._instance.config_map = {}
        else:
            print("\n[AppConfig] Using existing instance")
        return cls._instance

    def set_config(self, key, value):
        self.config_map[key] = value
        print(f"\n[set_config] Value  : {value} added for key : {key}")

    def get_config(self, key):
        if key in self.config_map:
            print(f"\n[get_config] Value : {self.config_map[key]}")
        else:
            print("\n[get_config] Value does not exist")

app = AppConfig()

app.set_config(12,12)
app.set_config(15,5)

app.get_config(15)
app.get_config(7)

app2 = AppConfig()

app2.get_config(15)
