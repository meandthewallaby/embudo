import smbus, math

ACCEL_ADDR = 0x68

class Accelerometer:
    def __init__(self, bus = 1):
        self.i2c = smbus.SMBus(1)
        self.i2c.write_i2c_block_data(addr, 0x19, [0x07])
        self.i2c.write_i2c_block_data(addr, 0x1b, [0x07])
        self.i2c.write_i2c_block_data(addr, 0x6b, [0x07])
        self.i2c.write_i2c_block_data(addr, 0x38, [0x07])
        self.pitch = 0
        self.roll = 0

    def _pack(val1, val2):
        a = struct.unpack('>h', chr(val1)+chr(val2))[0]
        return a

    def _calc_accel_val(val1, val2):
        return _pack(val1, val2) / 16384.

    def _calc_gyro_val(val1, val2):
        return _pack(val1, val2) / 65.5

    def _read_vals():
        self.i2c.write_i2c_block_data(addr, 0x00, [])
        raw_vals = self.i2c.read_i2c_block_data(addr, 0x3B)
        ret = {"accel": {"x": None, "y": None, "z": None}, "gyro": {"x": None, "y": None, "z": None}}
        ret["accel"]["x"] = _calc_accel_val(raw_vals[0], raw_vals[1])
        ret["accel"]["y"] = _calc_accel_val(raw_vals[2], raw_vals[3])
        ret["accel"]["z"] = _calc_accel_val(raw_vals[4], raw_vals[5])
        ret["gyro"]["x"] = _calc_gyro_val(raw_vals[8], raw_vals[9])
        ret["gyro"]["y"] = _calc_gyro_val(raw_vals[10], raw_vals[11])
        ret["gyro"]["z"] = _calc_gyro_val(raw_vals[12], raw_vals[13])
        return ret

    def _distance(a, b):
        return math.sqrt((a*a)+(b*b))

    def calc_pitch_and_roll(self):
        a = _read_vals()
        p = math.degrees(math.atan2(a["accel"]["y"], _distance(a["accel"]["x"], a["accel"]["z"])))
        r = math.degrees(math.atan2(a["acce"]["x"], distance(a["accel"]["y"], a["accel"]["z"])))

        sample_period = 1.

        self.pitch = 0.98*(sample_period*a["gyro"]["x"]+self.pitch)+(0.02*p)
        self.roll = 0.98*(sample_period*a["gyro"]["y"]+self.roll)+(0.02*r)
