#!/usr/bin/python3

import smbus
import time
import sys
import struct

cmdValid = 0
if __name__ == "__main__":
    if len(sys.argv) == 5:
        if sys.argv[1] == "-rb":
            hw_add = int(sys.argv[2])
            mem_add = int(sys.argv[3])
            len = int(sys.argv[4])
            bus = smbus.SMBus(1)
            buff = bus.read_i2c_block_data(hw_add, mem_add, len)
            print(buff)
            bus.close()
            cmdValid = 1
        if sys.argv[1] == "-rw":
            hw_add = int(sys.argv[2])
            mem_add = int(sys.argv[3])
            len = int(sys.argv[4])
            bus = smbus.SMBus(1)
            for i in range(len):
                val = bus.read_word_data(hw_add, mem_add + 2 * i)
                print(val)
            bus.close()
            cmdValid = 1
        if sys.argv[1] == "-rf":
            hw_add = int(sys.argv[2])
            mem_add = int(sys.argv[3])
            len = int(sys.argv[4])
            bus = smbus.SMBus(1)
            for i in range(len):
                buff = bus.read_i2c_block_data(hw_add, mem_add + 4 * i, 4)
                val = struct.unpack('f', bytearray(buff))
                print(val[0])
            bus.close()
            cmdValid = 1
        if sys.argv[1] == "-ri":
            hw_add = int(sys.argv[2])
            mem_add = int(sys.argv[3])
            len = int(sys.argv[4])
            bus = smbus.SMBus(1)
            for i in range(len):
                buff = bus.read_i2c_block_data(hw_add, mem_add + 4 * i, 4)
                val = struct.unpack('i', bytearray(buff))
                print(val[0])
            bus.close()
            cmdValid = 1
        if sys.argv[1] == "-ww":
            hw_add = int(sys.argv[2])
            mem_add = int(sys.argv[3])
            val = int(sys.argv[4])
            bus = smbus.SMBus(1)
            bus.write_word_data(hw_add, mem_add, val)
            bus.close()
            cmdValid = 1
        if sys.argv[1] == "-wb":
            hw_add = int(sys.argv[2])
            mem_add = int(sys.argv[3])
            val = int(sys.argv[4])
            bus = smbus.SMBus(1)
            bus.write_byte_data(hw_add, mem_add, val)
            bus.close()
            cmdValid = 1
    else:
        if len(sys.argv) == 2:
            if sys.argv[1] == "-s":
                bus = smbus.SMBus(1)
                for i in range(0x7e):
                    try:
                        buff = bus.read_i2c_block_data(i + 1, 0, 1)
                        print(i + 1)
                    except Exception as e:
                        pass
                bus.close()
                cmdValid = 1
    if cmdValid == 0:
        print("Invalid options! \n\rUsage:")
        print("Read buffer => \tpython i2c.py -rb <hwAdd> <memAdd> <bytesCount>")
        print("Read word => \tpython i2c.py -rw <hwAdd> <memAdd> <len>")
        print("Read float => \tpython i2c.py -rf <hwAdd> <memAdd> <len>")
        print("Read int32 => \tpython i2c.py -ri <hwAdd> <memAdd> <len>")
        print("Write byte => \tpython i2c.py -wb <hwAdd> <memAdd> <byteVal>")
        print("Write word => \tpython i2c.py -ww <hwAdd> <memAdd> <woedVal>")
        print("Scan bus => \tpython i2c.py -s")
