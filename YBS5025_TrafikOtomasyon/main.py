from TrafficSystem import TrafficSystem as TS
from RPLCD.i2c import CharLCD
import time, threading

def main():
    system = TS()
    print("sistem hazirlaniyor...")
    time.sleep(4)
    
    lcd = CharLCD('PCF8574', 0x27)
    lcd.clear()

    def sensor_loop():
        while True:
            system.controller.update_waiting_car("A1_entry", "A1")
            #system.controller.update_waiting_car("A2_entry", "A2")
            system.controller.update_waiting_car("B_entry", "B")

            system.controller.update_passing_car("A1_exit", "A1")
            #system.controller.update_passing_car("A2_exit", "A2")
            system.controller.update_passing_car("B_exit", "B")

            time.sleep(0.5)

    sensor_thread = threading.Thread(target=sensor_loop, daemon=True)
    sensor_thread.start()
    
    def lcd_loop():

        while True:
            current = system.current_scenario 
            remaining_time = system.remaining_time
                    
            waiting_A = system.controller.waiting_cars["A1"]
            waiting_B = system.controller.waiting_cars["B"]
            passed_A = system.controller.passing_cars["A1"]
            passed_B = system.controller.passing_cars["B"]

            lcd.clear()
            lcd.cursor_pos = (0, 0)
            lcd.write_string(f"{current}  Yesil:{remaining_time:02}s")
        
            lcd.cursor_pos = (1, 0)
            lcd.write_string(f"A:{waiting_A}/{passed_A} B:{waiting_B}/{passed_B}")

            time.sleep(1)
            
    lcd_thread = threading.Thread(target=lcd_loop, daemon=True)
    lcd_thread.start()
        
    try:
        while True:  
            next_scenario = system.next_scenario()
            print(f"Secilen senaryo: {next_scenario}")
            system.execute_scenario(next_scenario)
            time.sleep(1)

    except KeyboardInterrupt:
        lcd.clear()
        lcd.write_string("Sistem durdu")
        print("\nSistem manuel olarak durduruldu.")
        time.sleep(1)
        lcd.clear()
        system.controller.sensor_manager.cleanup()
        print("Sensorler temizlendi. Sistem kapatÄ±ldÄ±.")
        
if __name__ == "__main__":
        main()
