import smbus, math

addr = 0x68
i2c = smbus.SMBus(1)
i2c.write_i2c_block_data(addr, 0x19, [0x07])
i2c.write_i2c_block_data(addr, 0x1b, [0x07])
i2c.write_i2c_block_data(addr, 0x6b, [0x07])
i2c.write_i2c_block_data(addr, 0x38, [0x07])

def pack(val1, val2):
    a = struct.unpack('>h', chr(val1)+chr(val2))[0]
    return a

def calc_accel_val(val1, val2):
    return pack(val1, val2) / 16384.

def calc_gyro_val(val1, val2):
    return pack(val1, val2) / 65.5

def read_vals():
    i2c.write_i2c_block_data(addr, 0x00, [])
    raw_vals = i2c.read_i2c_block_data(addr, 0x3B)
    ret = {"accel": {"x": None, "y": None, "z": None}, "gyro": {"x": None, "y": None, "z": None}}
    ret["accel"]["x"] = calc_accel_val(raw_vals[0], raw_vals[1])
    ret["accel"]["y"] = calc_accel_val(raw_vals[2], raw_vals[3])
    ret["accel"]["z"] = calc_accel_val(raw_vals[4], raw_vals[5])
    ret["gyro"]["x"] = calc_gyro_val(raw_vals[8], raw_vals[9])
    ret["gyro"]["y"] = calc_gyro_val(raw_vals[10], raw_vals[11])
    ret["gyro"]["z"] = calc_gyro_val(raw_vals[12], raw_vals[13])
    return ret

def distance(a, b):
    return math.sqrt((a*a)+(b*b))

def calc_pitch_and_roll(a):
    p = math.degrees(math.atan2(a["accel"]["y"], distance(a["accel"]["x"], a["accel"]["z"])))
    pitch=0.98*a["gyro"]["x"]+0.02*p
    return pitch
