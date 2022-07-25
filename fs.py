import io
import os
import sys

import utils



NAME_SIZE_SIZE = 1
CONTENTS_SIZE_SIZE = 4
COMMONS_ADDRESS_SIZE = 4

operations = [
    'startFS'
]

class Commons:
    def __init__(self, filename: str, index: int, name=None, contents=bytes([])):
        self.filename = filename
        self.index = index

        if os.path.isfile(self.filename):
            with open(self.filename, 'rb') as fh:
                self.name_size = int.from_bytes(fh.read(NAME_SIZE_SIZE), 'big')
                self.name = fh.read(self.name_size)
                self.contents_size = int.from_bytes(fh.read(CONTENTS_SIZE_SIZE), 'big')
                self.contents = fh.read(self.contents_size)
        else:
            if name is None:
                raise RuntimeError('You must provide a name for Commons.')
            with open(self.filename, 'wb') as fh:
                self.name_size = len(name)
                self.name = name
                if contents is None:
                    self.contents_size = 0
                else:
                    self.contents_size = len(contents)
                self.contents = contents
                self.name_bytes = bytes(self.name, 'ascii')
                self.contents_size_bytes = bytes([self.contents_size])
                fh.write(bytes([
                    self.name_size,
                    *self.name_bytes,
                    *self.contents_size_bytes,
                    *self.contents
                ]))

    def dump(self):
        """
        save name_size, name, contents_size, contents to fs file
        """

        pass

    def is_file(self):
        return self.name[-1] != '/'
    
    def is_folder(self):
        return self.name[-1] == '/'

    def __len__(self):
        return NAME_SIZE_SIZE + self.name_size + CONTENTS_SIZE_SIZE + self.contents_size

    def seek(self, index=0, mode=0):
        self.fh.seek(self.index+index, mode)
    
    def read(self, size: int):
        return self.fh.read(size)

    def write(self, contents: bytes):
        self.fh.write(contents)
    
    def append(self, contents: bytes):
        self.seek_end()
        self.fh.write(contents)

    def append_contents(self, append_contents: bytes):
        append_size = len(append_contents)
        index_start = len(self)
        index_end = index_start + append_size
        folders = [Folder(self.filename, 0)]
        update_folders = []

        while len(folders) > 0:
            current_folder = folders.pop(0)
            if current_folder.has_file_address_between(index_start, index_end):
                update_folders.append(current_folder)
            folders += current_folder.get_folders()

        # todo: update addresses in folder before shifting
        utils.insert_null(self.filename, index_start, 1)

    def raw(self, return_int=False):
        with open(self.filename, 'rb') as fh:
            data = fh.read()
            if return_int:
                data = list(data)
            return data

class File(Commons):
    
    pass

class Folder(Commons):
    def get_folders(self):
        """
        check for Commons in folder which are folders
        """
        folders = []

        with open(self.filename, 'rb') as fh:
            fh.seek(self.index)
            chunk = fh.read(COMMONS_ADDRESS_SIZE)
            while chunk:
                chunk_int = int.from_bytes(chunk, 'big')
                folder = Folder(self.filename, chunk_int)
                if folder.is_folder():
                    folders.append(folder)
                chunk = fh.read(COMMONS_ADDRESS_SIZE)
        
        return folders

    def has_file_address_between(self, start: int, end: int):
        """
        check in folder for file addresses between 'start' (included) and 'end' (not included)
        """
        with open(self.filename, 'rb') as fh:
            fh.seek(self.index)
            chunk = fh.read(COMMONS_ADDRESS_SIZE)
            while chunk:
                chunk_int = int.from_bytes(chunk, 'big')
                if start <= chunk_int and chunk_int < end:
                    return True
                chunk = fh.read(COMMONS_ADDRESS_SIZE)

        return False

    
    def find_file_addresses(self, start: int, end: int):
        """
        search in folder for file addresses between 'start' (included) and 'end' (not included)
        """
        addresses = []

        with open(self.filename, 'rb') as fh:
            fh.seek(self.index)
            chunk = fh.read(COMMONS_ADDRESS_SIZE)
            while chunk:
                chunk_int = int.from_bytes(chunk, 'big')
                if start <= chunk_int and chunk_int < end:
                    addresses.append(chunk_int)
                chunk = fh.read(COMMONS_ADDRESS_SIZE)

        return addresses



    def create_file(self, name: str, contents: bytes):
        # todo: discover index after folder's content
        self.contents
        index_shift = len(self)
        utils.insert_null(self.filename, index_shift, 1)
        self.contents_size += 1
        pass
    
    def has_commons(self, commons_index: int):
        with open(self.filename, 'rb') as fh:
            fh.seek(self.index)
            chunk = fh.read(COMMONS_ADDRESS_SIZE)
            while chunk:
                chunk_int, tell = int.from_bytes(chunk, 'big'), fh.tell()
                if chunk_int == commons_index:
                    return tell
                chunk = fh.read(COMMONS_ADDRESS_SIZE)
        return -1

    def __find_address_at_folder(self):
        index = 0
        folders = [0]
        while len(folders) > 0:
            current_index = folders.pop(0)
            current_commons = Commons(self.filename, current_index)
            if current_commons.is_folder():
                if current_commons.has_commons(self.index):
                    pass
        pass


    


class FS:
    current_index = 0

    def __init__(self, name: str):
        self.filename = f'{name}.fs'
        if os.path.isfile(self.filename):
            self.root = Folder(self.filename, 0)
        else:
            self.root = Folder(self.filename, 0, './')

    def total_size(self):
        return len(Folder(self.filename, 0))
    
    def raw(self, return_int=False):
        return Folder(self.filename, 0).raw(return_int)

    def current_folder(self):
        return Folder(self.filename, self.current_index)


# try:
#     pass
#     operation = sys.argv[1]
#     if operation not in operations:
#         raise RuntimeError(f'Operation \'{operation}\' doesn\'t exist.')
#     pass
# except IndexError:
#     print('You MUST provide an operation name.')
