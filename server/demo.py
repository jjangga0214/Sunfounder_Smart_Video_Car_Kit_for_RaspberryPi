import rcar
import time

if __name__ == "__main__":
    car = rcar.RCar()

    car.forward()
    time.sleep(3)
    car.stop()
