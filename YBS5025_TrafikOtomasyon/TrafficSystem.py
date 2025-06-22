from TrafficController import TrafficController
import time, threading
from gpiozero import LED
from gpiozero import RGBLED
from gpiozero import Button

class TrafficSystem:

	def __init__(self):
		self.controller = TrafficController()
		self.current_scenario = None
		self.scenarios = ["S1", "S2", "S3"]
		self.scenario_active = False
		
		self.rgb_led1 = RGBLED(red=26, green=19, blue=13)
		self.rgb_led2 = RGBLED(red=11, green=9, blue=10)
		
		self.ped_button = Button(12)
		self.last_ped_time = 0
		self.ped_request = False
		self.ped_button.when_pressed = self._on_ped_button
		
		self.remaining_time = 0
		
	def _on_ped_button(self):
		now = time.time()
		
		if now - self.last_ped_time >=60:
			print("Yaya istegi alindi. S3'e gecilecek.")
			self.ped_request = True
		else:
			print("Yaya istegi kilitli")
			
	def update_remaining_time(self,green_duration):
		self.remaining_time = green_duration
		while self.remaining_time > 0:
			time.sleep(1)
			self.remaining_time -= 1
		
	def next_scenario(self):
		if self.ped_request:
			return "S3"
			
		prev = self.current_scenario
		if prev == "S1" or None:
			return "S2"
		elif prev   == "S2" or "S3":
			if self.controller.waiting_cars["B"] > 0:
				return "S1"
			else:
				return "S2"
				
		'''
		if self.current_scenario is None:
			self.current_scenario = self.scenarios[0]
		else:
			current_index = self.scenarios.index(self.current_scenario)
			self.current_scenario = self.scenarios[(current_index + 1) % len(self.scenarios)]
		return self.current_scenario      '''  
		
	def execute_scenario(self, scenario):
		self.scenario_active = True
		self.current_scenario = scenario

		if scenario == "S1":
			green_direction = "B"
			red_directions = [("A1", "A1_Entry"), ("A2", "A2_Entry")]
			self.rgb_led1.color = (0, 1, 0) #yesil
			self.rgb_led2.color = (1, 0, 0) #kÄ±rmÄ±zÄ±

			green_duration = self.controller.calculate_green_time(green_direction)
			self.update_remaining_time(green_duration)
			
			print(f"\n{green_direction} yonu icin yesil isik yaniyor. Sure: {green_duration} saniye.")
			
			#time.sleep(green_duration)

			passed = self.controller.reset_passing_cars(green_direction)
			remaining = self.controller.waiting_cars[green_direction]

			print(f"{green_direction} yonu: Gecen arac sayisi: {passed}, Kalan arac: {remaining}")

			for red_dir, _ in red_directions:
				print(f"{red_dir} yonunde bekleyen arac: {self.controller.waiting_cars[red_dir]}")
			
			#self.led_s1.off()
			#time.sleep(2) # Sari yanma suresi

		elif scenario == "S2":
			#green_directions = ["A1", "A2"]
			green_directions = ["A1"]
			red_direction = ("B", "B_entry")
			self.rgb_led1.color = (1, 0, 0) 
			self.rgb_led2.color = (0, 1, 0) 
			
			threads = []

			def handle_green(direction):
				green_duration = self.controller.calculate_green_time("A1")
				self.update_remaining_time(green_duration)
				
				print(f"\n{direction} yonu icin yesil isik yaniyor. Sure: {green_duration} saniye.")
				#time.sleep(green_duration)

				passed = self.controller.reset_passing_cars(direction)
				remaining = self.controller.waiting_cars[direction]
				print(f"{direction} yonu: Gecen arac sayisi: {passed}, Kalan arac: {remaining}")

			for direction in green_directions:
				t = threading.Thread(target=handle_green, args=(direction,))
				threads.append(t)
				t.start()

			for t in threads:
				t.join()

			print(f"{red_direction[0]} yonunde bekleyen arac: {self.controller.waiting_cars[red_direction[0]]}")
			
			#self.led_s2.off()
			#time.sleep(2) # Sari yanma suresi

		elif scenario == "S3":
			print("\nSistem bekleme modunda. (S3)")
			green_duration = 10
			self.rgb_led1.color = (1, 0, 0) 
			self.rgb_led2.color = (1, 0, 0) 
			self.update_remaining_time(green_duration)
			#time.sleep(green_duration)
			print("Yaya gecisi tamamlandi.")
			self.ped_request = False
			self.last_ped_time = time.time()

		self.scenario_active = False
