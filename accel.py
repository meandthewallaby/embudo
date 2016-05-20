import smbus, math, struct

ACCEL_ADDR = 0x68

class Accelerometer:
    def __init__(self, bus = 1):
        self.i2c = smbus.SMBus(1)
        self.i2c.write_i2c_block_data(ACCEL_ADDR, 0x19, [0x01]) # Set gyroscope sample rate (turn to 0x08 if low pass is enabled)
        self.i2c.write_i2c_block_data(ACCEL_ADDR, 0x1a, [0x01]) # Set gyroscope low pass filter
        self.i2c.write_i2c_block_data(ACCEL_ADDR, 0x1b, [0x10]) # Set gyroscope to +/- 1000 deg/s
        self.i2c.write_i2c_block_data(ACCEL_ADDR, 0x1c, [0x18]) # Set accelerometer to +/- 16g
        self.i2c.write_i2c_block_data(ACCEL_ADDR, 0x6b, [0x02]) # Set clock source to use PLL w/ y-axis gyroscope
        self.i2c.write_i2c_block_data(ACCEL_ADDR, 0x38, [0x01]) # Enable data ready interrupt
        self.pitch = None
        self.roll = None

    def _unpack(self, val1, val2):
        a = struct.unpack('>h', chr(val1)+chr(val2))[0]
        return a

    def _calc_accel_val(self, val1, val2):
        return self._unpack(val1, val2) / 16384.

    def _calc_gyro_val(self, val1, val2):
        return self._unpack(val1, val2) / 65.5

    def read_vals(self):
        self.i2c.write_i2c_block_data(ACCEL_ADDR, 0x00, [])
        raw_vals = self.i2c.read_i2c_block_data(ACCEL_ADDR, 0x3B)
        ret = {"accel": {"x": None, "y": None, "z": None}, "gyro": {"x": None, "y": None, "z": None}}
        ret["accel"]["x"] = self._calc_accel_val(raw_vals[0], raw_vals[1])
        ret["accel"]["y"] = self._calc_accel_val(raw_vals[2], raw_vals[3])
        ret["accel"]["z"] = self._calc_accel_val(raw_vals[4], raw_vals[5])
        ret["gyro"]["x"] = self._calc_gyro_val(raw_vals[8], raw_vals[9])
        ret["gyro"]["y"] = self._calc_gyro_val(raw_vals[10], raw_vals[11])
        ret["gyro"]["z"] = self._calc_gyro_val(raw_vals[12], raw_vals[13])
        return ret

    def _distance(self, a, b):
        return math.sqrt((a*a)+(b*b))

    def calc_pitch_and_roll(self):
        a = self.read_vals()
        self.pitch = math.degrees(math.atan2(a["accel"]["x"], self._distance(a["accel"]["y"], a["accel"]["z"])))
        self.roll = math.degrees(math.atan2(-a["accel"]["x"], a["accel"]["z"]))
