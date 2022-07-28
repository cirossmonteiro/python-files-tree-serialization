import os


NAME_SIZE_SIZE = 1 # maximum size for name: 255 bytes, then 255 ASCII characters
COMMONS_MAX_SIZE = 4 # maximum size for contents: 4294967296 bytes = 4194304 kilobytes = 4096 megabytes = 4 gibabytes


class Commons:
    def __init__(self, name: str, contents):
        """
        if Commons.name ends with '/' then it's a folder, otherwise it's a file.
        """
        self.name = name
        self.contents = contents # list of instances of Commons in folders,  bytes in files

    def __repr__(self):
        s = f'{self.name}'
        if self.name[-1] == '/':
            for content in self.contents:
                s += f'--{content}'
        return s

    def __eq__(self, other):
        if self.name != other.name:
            return False
        if self.name[-1] == '/':
            for content in self.contents:
                if content not in other.contents:
                    return False
            for content in other.contents:
                if content not in self.contents:
                    return False
            return True
        else:
            return self.contents == other.contents
            

def serialize_commons(commons: Commons):
    contents = commons.contents
    header = bytes([
        *len(commons.name).to_bytes(NAME_SIZE_SIZE, 'big'),
        *bytes(commons.name, 'ascii')
    ])

    if commons.name[-1] == '/' and len(contents) > 0:
        contents = [serialize_commons(contents) for contents in commons.contents]
        sizes = [len(content).to_bytes(COMMONS_MAX_SIZE, 'big') for content in contents]
        contents = [*sizes, *contents]
        body = bytes([
            *len(sizes).to_bytes(COMMONS_MAX_SIZE, 'big'),
            *b''.join(contents)
        ])
    else:
        body = bytes([
            *len(contents).to_bytes(COMMONS_MAX_SIZE, 'big'),
            *contents
        ])

    return bytes([*header, *body])


def serialize(root: Commons):
    return serialize_commons(root)


def unserialize_commons(data: bytes):
    index = 0
    name_size = int.from_bytes(data[index:index+NAME_SIZE_SIZE], 'big')
    index += NAME_SIZE_SIZE
    name = data[index:index+name_size].decode('ascii')
    index += name_size
    if name[-1] == '/':
        sizes_size = int.from_bytes(data[index:index+COMMONS_MAX_SIZE], 'big')
        index += COMMONS_MAX_SIZE
        sizes = [
            int.from_bytes(data[index+k*COMMONS_MAX_SIZE:index+(k+1)*COMMONS_MAX_SIZE], 'big')
            for k in range(sizes_size)
        ]
        index += sizes_size*COMMONS_MAX_SIZE
        contents = []
        for size in sizes:
            contents.append(unserialize_commons(data[index:index+size]))
            index += size
    else:
        contents_size = int.from_bytes(data[index:index+COMMONS_MAX_SIZE], 'big')
        index += COMMONS_MAX_SIZE
        contents = data[index:index+contents_size]
    
    return Commons(name, contents)


def unserialize(data: bytes):
    return unserialize_commons(data)


def track_commons(parent: str, current: str):
    path = f'{parent}/{current}'
    if current[-1] == '/':
        contents = [
            common if os.path.isfile(f'{path}/{common}') else f'{common}/'
            for common in os.listdir(f'{path}')
        ]
        contents = [track_commons(path, content) for content in contents]
    else:
        with open(path, 'rb') as fh:
            contents = fh.read()
    return Commons(current, contents)
