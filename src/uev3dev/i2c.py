import uctypes

from fcntl import ioctl

# from linux/i2c.h

I2C_M_TEN = 0x0010
I2C_M_RD = 0x0001
I2C_M_STOP = 0x8000
I2C_M_NOSTART = 0x4000
I2C_M_REV_DIR_ADDR = 0x2000
I2C_M_IGNORE_NAK = 0x1000
I2C_M_NO_RD_ACK = 0x0800
I2C_M_RECV_LEN = 0x0400

I2C_FUNC_I2C = 0x00000001
I2C_FUNC_10BIT_ADDR = 0x00000002
I2C_FUNC_PROTOCOL_MANGLING = 0x00000004
I2C_FUNC_SMBUS_PEC = 0x00000008
I2C_FUNC_NOSTART = 0x00000010
I2C_FUNC_SLAVE = 0x00000020
I2C_FUNC_SMBUS_BLOCK_PROC_CALL = 0x00008000
I2C_FUNC_SMBUS_QUICK = 0x00010000
I2C_FUNC_SMBUS_READ_BYTE = 0x00020000
I2C_FUNC_SMBUS_WRITE_BYTE = 0x00040000
I2C_FUNC_SMBUS_READ_BYTE_DATA = 0x00080000
I2C_FUNC_SMBUS_WRITE_BYTE_DATA = 0x00100000
I2C_FUNC_SMBUS_READ_WORD_DATA = 0x00200000
I2C_FUNC_SMBUS_WRITE_WORD_DATA = 0x00400000
I2C_FUNC_SMBUS_PROC_CALL = 0x00800000
I2C_FUNC_SMBUS_READ_BLOCK_DATA = 0x01000000
I2C_FUNC_SMBUS_WRITE_BLOCK_DATA = 0x02000000
I2C_FUNC_SMBUS_READ_I2C_BLOCK = 0x04000000
I2C_FUNC_SMBUS_WRITE_I2C_BLOCK = 0x08000000

I2C_SMBUS_BLOCK_MAX = 32

i2c_smbus_data = {
    'byte': uctypes.UINT8 | 0,
    'word': uctypes.UINT16 | 0,
    'block': (uctypes.ARRAY | 0, uctypes.UINT8 | (I2C_SMBUS_BLOCK_MAX + 2))
}

size_of_i2c_smbus_data = uctypes.sizeof(i2c_smbus_data)

I2C_SMBUS_READ = 1
I2C_SMBUS_WRITE = 0

I2C_SMBUS_QUICK = 0
I2C_SMBUS_BYTE = 1
I2C_SMBUS_BYTE_DATA = 2
I2C_SMBUS_WORD_DATA = 3
I2C_SMBUS_PROC_CALL = 4
I2C_SMBUS_BLOCK_DATA = 5
I2C_SMBUS_I2C_BLOCK_BROKEN = 6
I2C_SMBUS_BLOCK_PROC_CALL = 7
I2C_SMBUS_I2C_BLOCK_DATA = 8

# from linux/i2c-dev.h

I2C_RETRIES = 0x0701
I2C_TIMEOUT = 0x0702
I2C_SLAVE = 0x0703
I2C_SLAVE_FORCE = 0x0706
I2C_TENBIT = 0x0704
I2C_FUNCS = 0x0705
I2C_RDWR = 0x0707
I2C_PEC = 0x0708
I2C_SMBUS = 0x0720

i2c_smbus_ioctl_data = {
    'read_write': uctypes.UINT8 | 0,
    'command': uctypes.UINT8 | 1,
    'size': uctypes.UINT32 | 4,
    'data': uctypes.PTR | 8
}

size_of_i2c_smbus_ioctl_data = uctypes.sizeof(i2c_smbus_ioctl_data)


class SMBus():
    """Micropython implementation of SMBus"""

    _slave = 0

    def __init__(self, path):
        """Create a new SMBus instance
        :param string path: The path to the I2C device node, e.g. ``/dev/i2c0``.
        """
        self._devnode = open(path, 'w+')
        self._fd = self._devnode.fileno()
        flags = bytes(4)
        ioctl(self._fd, I2C_FUNCS, flags, mut=True)
        flags = uctypes.struct(uctypes.addressof(flags), {
            'flags': uctypes.UINT32  # unsigned long
        }).flags
        self._func = {
            'i2c': bool(flags & I2C_FUNC_I2C),
            'ten_bit_addr': bool(flags & I2C_FUNC_10BIT_ADDR),
            'protocol_mangling': bool(flags & I2C_FUNC_PROTOCOL_MANGLING),
            'smbus_pec': bool(flags & I2C_FUNC_SMBUS_PEC),
            'no_start': bool(flags & I2C_FUNC_NOSTART),
            'slave': bool(flags & I2C_FUNC_SLAVE),
            'smbus_block_proc_call': bool(flags & I2C_FUNC_SMBUS_BLOCK_PROC_CALL),
            'smbus_quick': bool(flags & I2C_FUNC_SMBUS_QUICK),
            'smbus_read_byte': bool(flags & I2C_FUNC_SMBUS_READ_BYTE),
            'smbus_write_byte': bool(flags & I2C_FUNC_SMBUS_WRITE_BYTE),
            'smbus_write_data': bool(flags & I2C_FUNC_SMBUS_WRITE_BYTE_DATA),
            'smbus_read_word_data': bool(flags & I2C_FUNC_SMBUS_READ_WORD_DATA),
            'smbus_write_word_data': bool(flags & I2C_FUNC_SMBUS_WRITE_WORD_DATA),
            'smbus_proc_call': bool(flags & I2C_FUNC_SMBUS_PROC_CALL),
            'smbus_read_block_data': bool(flags & I2C_FUNC_SMBUS_READ_BLOCK_DATA),
            'smbus_read_i2c_block': bool(flags & I2C_FUNC_SMBUS_READ_I2C_BLOCK),
            'smbus_write_i2c_block': bool(flags & I2C_FUNC_SMBUS_WRITE_I2C_BLOCK),
        }

    def set_address(self, address):
        ioctl(self._fd, I2C_SLAVE, address)

    def _access(self, read_write, command, size, data):
        b = bytearray(size_of_i2c_smbus_ioctl_data)
        args = uctypes.struct(uctypes.addressof(b), i2c_smbus_ioctl_data)
        args.read_write = read_write
        args.command = command
        args.size = size
        args.data = uctypes.addressof(data)
        ioctl(self._fd, I2C_SMBUS, args, mut=True)

    def write_quick(self, value):
        self._access(value, 0, I2C_SMBUS_QUICK, None)

    def read_byte(self):
        b = bytearray(size_of_i2c_smbus_data)
        data = uctypes.struct(uctypes.addressof(b), i2c_smbus_data)
        self._access(I2C_SMBUS_READ, 0, I2C_SMBUS_BYTE, data)
        return data.byte

    def write_byte(self, value):
        self._access(I2C_SMBUS_WRITE, value, I2C_SMBUS_BYTE, None)

    def read_byte_data(self, command):
        b = bytearray(size_of_i2c_smbus_data)
        data = uctypes.struct(uctypes.addressof(b), i2c_smbus_data)
        self._access(I2C_SMBUS_READ, command, I2C_SMBUS_BYTE_DATA, data)
        return data.byte

    def write_byte_data(self, command, value):
        b = bytearray(size_of_i2c_smbus_data)
        data = uctypes.struct(uctypes.addressof(b), i2c_smbus_data)
        data.byte = value
        self._access(I2C_SMBUS_WRITE, command, I2C_SMBUS_BYTE_DATA, data)

    def read_word_data(self, command):
        b = bytearray(size_of_i2c_smbus_data)
        data = uctypes.struct(uctypes.addressof(b), i2c_smbus_data)
        self._access(I2C_SMBUS_READ, command, I2C_SMBUS_WORD_DATA, data)
        return data.word

    def write_word_data(self, command, value):
        b = bytearray(size_of_i2c_smbus_data)
        data = uctypes.struct(uctypes.addressof(b), i2c_smbus_data)
        data.word = value
        self._access(I2C_SMBUS_WRITE, command, I2C_SMBUS_WORD_DATA, data)

    def process_call(self, command, value):
        b = bytearray(size_of_i2c_smbus_data)
        data = uctypes.struct(uctypes.addressof(b), i2c_smbus_data)
        data.word = value
        self._access(I2C_SMBUS_WRITE, command, I2C_SMBUS_PROC_CALL, data)
        return data.word

    def read_block_data(self, command, values):
        b = bytearray(size_of_i2c_smbus_data)
        data = uctypes.struct(uctypes.addressof(b), i2c_smbus_data)
        self._access(I2C_SMBUS_READ, command, I2C_SMBUS_BLOCK_DATA, data)
        return data.block

    def write_block_data(self, command, values):
        b = bytearray(size_of_i2c_smbus_data)
        data = uctypes.struct(uctypes.addressof(b), i2c_smbus_data)
        values = values[:32]
        data.block = [len(values)] + values
        self._access(I2C_SMBUS_WRITE, command, I2C_SMBUS_BLOCK_DATA, data)

    def read_i2c_block_data(self, command, length):
        b = bytearray(size_of_i2c_smbus_data)
        data = uctypes.struct(uctypes.addressof(b), i2c_smbus_data)
        length = min(length, 32)
        data.block[0] = length
        if length == 32:
            size = I2C_SMBUS_I2C_BLOCK_BROKEN
        else:
            size = I2C_SMBUS_I2C_BLOCK_DATA
        self._access(I2C_SMBUS_READ, command, size, data)
        return data.block[1:][:data.block[0]]

    def write_i2c_block_data(self, command, values):
        b = bytearray(size_of_i2c_smbus_data)
        data = uctypes.struct(uctypes.addressof(b), i2c_smbus_data)
        values = values[:32]
        data.block = [len(values)] + values
        self._access(I2C_SMBUS_WRITE, command, I2C_SMBUS_I2C_BLOCK_BROKEN, data)

    def block_process_call(self, command, values):
        b = bytearray(size_of_i2c_smbus_data)
        data = uctypes.struct(uctypes.addressof(b), i2c_smbus_data)
        values = values[:32]
        data.block = [len(values)] + values
        self._access(I2C_SMBUS_WRITE, command, I2C_SMBUS_BLOCK_PROC_CALL, data)
        return data.block[1:][:data.block[0]]
