from SR02 import SR02_Ultrasonic as Ultrasonic_Sensor

import front_wheels
import rear_wheels
import time

if __name__ == '__main__':
    
    try:
        
        # Example Of Front Servo Motor Control
        
        direction_controller = front_wheels.Front_Wheels(db='config')
        
        direction_controller.turn_straight()
        time.sleep(1)
        
        # Example Of Real Motor Control
        
        driving_controller = rear_wheels.Rear_Wheels(db='config')
        
        driving_controller.ready()
        driving_controller.forward_with_speed(50)
        time.sleep(1)
        driving_controller.stop()
        time.sleep(1)
        driving_controller.backward_with_speed(50)
        time.sleep(1)
                
        driving_controller.stop()
        driving_controller.power_down()
        
        # Exmaple of Ultrasonic Sensor
        
        distance_detector = Ultrasonic_Sensor.Ultrasonic_Avoidance(35)
        
        for i in range(10):
            distance = distance_detector.get_distance()
            print("Distance is ", distance)
            time.sleep(1)
        
    except KeyboardInterrupt:
        back.stop()
        back.power_down()
        