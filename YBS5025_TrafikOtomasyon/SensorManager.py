from gpiozero import DistanceSensor

class SensorManager:

    def __init__(self):
        self.threshold_cm = 10
        self.sensors_initialized = False
        self.sensors = {}

        try:
            self.sensors_initialized = True

            self.sensors = {
                "A1_entry": DistanceSensor(echo=24, trigger=23),
                #"A2_entry": DistanceSensor(echo=16, trigger=26),
                "B_entry": DistanceSensor(echo=21, trigger=20),
                "A1_exit": DistanceSensor(echo=8, trigger=25),
                #"A2_exit": DistanceSensor(echo=25, trigger=8),
                "B_exit": DistanceSensor(echo=1, trigger=7),
            }
            
            self.vehicle_flags = {key: True for key in self.sensors.keys()} 

            print("Sensorler hazir")

        except Exception as e:
            print(f"Ultrasonik sensor baslatma hatasi: {e}")
            self.sensors_initialized = False
            print(f"LCD ekran baÅlatma hatasÄ±: {e}")
            self.lcd = None

    def measure_distance(self, sensor_key):
        sensor = self.sensors.get(sensor_key)
        if sensor:
            distance = sensor.distance * 100 
            print(f"Mesafe [{sensor_key}]: {distance:.2f} cm")
            return distance
        else:
            print(f"HATA: Sensor bulunamadi -> {sensor_key}")

    def detect_vehicle(self, sensor_key):
        distance = self.measure_distance(sensor_key)

        if distance is None:
            return False

        if distance < self.threshold_cm and self.vehicle_flags[sensor_key] == True:
            print(f"[{sensor_key}] Arac algilandi")
            self.vehicle_flags[sensor_key] = False
            return True
        else:        
            if distance > self.threshold_cm:
                self.vehicle_flags[sensor_key] = True
                return False
            else:
                return False
            
    def cleanup(self):
        pass
