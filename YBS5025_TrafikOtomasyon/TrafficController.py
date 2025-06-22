import time
from SensorManager import SensorManager

class TrafficController:

    def __init__(self):
        self.waiting_cars = {"A1": 0, "A2": 0, "B": 2}
        self.passing_cars = {"A1": 0, "A2": 0, "B": 0}
        self.road_capacity = {"A1": 20, "A2": 20, "B": 6}
        
        self.current_scenario = None

        self.min_green_time = 5
        self.max_green_time = 30 
        self.extra_time_per_car = 3

        self.sensor_manager = SensorManager()
    
    def update_waiting_car(self, sensor_key, direction):
        isDetected = self.sensor_manager.detect_vehicle(sensor_key)
        if isDetected:
            self.waiting_cars[direction] += 1
            print(f"[{direction}] Arac Algilandi -- BEKLEYEN: {self.waiting_cars[direction]}")

    def update_passing_car(self,sensor_key, direction):
        isDetected = self.sensor_manager.detect_vehicle(sensor_key)
        if isDetected:
            self.passing_cars[direction] += 1
            self.waiting_cars[direction] -= 1
            print(f"[{direction}] Arac gecti -- BEKLEYEN: {self.waiting_cars[direction]} -- GECEN: {self.passing_cars[direction]}")

    def reset_passing_cars(self, direction):
        count = self.passing_cars[direction]
        self.passing_cars[direction] = 0
        return count
    
    def calculate_green_time(self, direction):
        waiting = self.waiting_cars[direction]
        base_time = waiting * self.extra_time_per_car
        green_time = max(self.min_green_time, min(self.max_green_time, base_time))

        return int(green_time)
    
    def active_green_time (self, direction):
        green_time = self.calculate_green_time(direction)
        print(f"{direction} yonunde yesil isik {green_time} saniye boyunca yaniyor")

        entry_sensor = f"{direction}_entry"
        exit_sensor = f"{direction}_exit"

        start_time = time.time()

        while time.time() - start_time < green_time:
            self.update_waiting_car(entry_sensor, direction)
            self.update_passing_car(exit_sensor, direction)
            print(f"{direction} durumu - Bekleyen: {self.waiting_cars[direction]}, Gecen: {self.passing_cars[direction]}")

        print(f"{direction} yonunde yesil isik sondu")
    
        passed_cars = self.reset_passing_cars(direction)
        return passed_cars, green_time
