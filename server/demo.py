import rcar
import time

if __name__ == "__main__":
    car = rcar.RCar()

    car.forward(60)
    time.sleep(3)
    car.stop()
    time.sleep(1)
    car.backward(60)
    time.sleep(3)
    car.stop()
    time.sleep(1)
    car.forward(-60)
    time.sleep(3)
    car.stop()
