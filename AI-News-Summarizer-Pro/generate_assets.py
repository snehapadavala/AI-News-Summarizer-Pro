from pathlib import Path
import struct
import zlib

base = Path('static/images')
base.mkdir(parents=True, exist_ok=True)

# Minimal PNG image (1x1 transparent pixel)
png_bytes = b'\x89PNG\r\n\x1a\n'
png_bytes += struct.pack('!I', 13) + b'IHDR' + struct.pack('!IIBBBBB', 1, 1, 8, 6, 0, 0, 0)
png_bytes += b'\x00\x00\x00\x00'  # no actual image data; placeholder but valid PNG bytes
png_bytes += struct.pack('!I', zlib.crc32(b'IHDR' + struct.pack('!IIBBBBB', 1, 1, 8, 6, 0, 0, 0)) & 0xFFFFFFFF)

# Build a proper PNG with zlib data
png_data = b'\x89PNG\r\n\x1a\n'

def chunk(chunk_type, data):
    return struct.pack('!I', len(data)) + chunk_type + data + struct.pack('!I', zlib.crc32(chunk_type + data) & 0xFFFFFFFF)

png_bytes = png_data + chunk(b'IHDR', struct.pack('!IIBBBBB', 1, 1, 8, 6, 0, 0, 0)) + chunk(b'IDAT', zlib.compress(b'\x00\x00\x00\x00')) + chunk(b'IEND', b'')
(base / 'logo.png').write_bytes(png_bytes)

# Minimal ICO file
ico_header = struct.pack('<HHHHHH', 0, 1, 1, 0, 0, 0)
# Use a tiny 16x16 icon
icon_data = bytearray()
icon_data.extend((0, 0, 1, 0, 1, 0))
icon_data.extend((16, 0, 16, 0, 32, 0))
icon_data.extend((0, 0, 0, 0, 0, 0, 0, 0))
icon_data.extend((0, 0, 0, 0, 0, 0, 0, 0))
icon_data.extend((0, 0, 0, 0, 0, 0, 0, 0))
Path('static/favicon.ico').write_bytes(icon_data)
