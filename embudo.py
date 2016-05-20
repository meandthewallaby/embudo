import camera, accel
import threading

def run_accel(accelerometer):
    threading.Timer(0.1, run_accel, [accelerometer]).start()
    accelerometer.calc_pitch_and_roll()
    print "Pitch: {}, Roll: {}".format(accelerometer.pitch, accelerometer.roll)

if __name__ == "__main__":
    accelerometer = accel.Accelerometer(bus=1)
    run_accel(accelerometer)
