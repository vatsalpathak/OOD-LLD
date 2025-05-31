from abc import ABC, abstractmethod

class Toggle():
    def __init__(self):
        self.is_active = False
    def toggle(self):
        self.is_active = not self.is_active
        if self.is_active:
            print("Turned on")
        else:
            print("Turned off")

class Dim(ABC):
    @abstractmethod
    def dim(self):
        pass

class Temperature(ABC):
    @abstractmethod
    def set_temperature(self,value):
        pass

class PlayMusic(ABC):
    @abstractmethod
    def play_music(self,music_name):
        pass

class SmartLight(Toggle,Dim):
    def __init__(self):
        super().__init__()
    def dim(self):
        print("Lights Dimmed")

class SmartThermostat(Toggle,Temperature):
    def __init__(self):
        super().__init__()
        self.temperature = 0
    def set_temperature(self,value):
        self.temperature = value
        print(f"Temperature is set to {value}")

class SmartSpeaker(Toggle,PlayMusic):
    def __init__(self):
        super().__init__()
    def play_music(self,music_name):
        print(f"Playing music {music_name}")

#for smart light
print("\n light \n")
light = SmartLight()
light.toggle()
light.dim()
light.toggle()

#for smart thermostat
print("\n thermostat \n")
thermostat = SmartThermostat()
thermostat.toggle()
thermostat.set_temperature(27)
thermostat.toggle()

#for smart speaker
print("\n speaker \n")
speaker = SmartSpeaker()
speaker.toggle()
speaker.play_music("Love beats")
speaker.toggle()
print("\n\n")