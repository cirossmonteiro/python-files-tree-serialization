import os

def shift_right(filename: str, size: int):
    with open(filename, 'rb') as fh_read:
        with open(filename, 'wb') as fh_write:
            count = 1
            while fh_read.tell() > 1:
                fh_read.seek(-count, os.SEEK_END)
                byte = fh_read.read(1)
                fh_write.seek(size-count, os.SEEK_END)
                fh_write.write(byte)
                count += 1

def insert_null(filename: str, start: int, size: int):
    with open(filename, 'rb') as fh_read:
        data = bytearray(fh_read.read())
        nulls = bytes([0 for _ in range(size)])
        data[start:start] = nulls # no idea why this even works
        with open(filename, 'wb') as fh_write:
            fh_write.write(data)