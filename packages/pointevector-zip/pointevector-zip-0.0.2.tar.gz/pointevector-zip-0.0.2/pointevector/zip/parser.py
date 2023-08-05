import enum
import logging
import io
import zlib

from pointevector.zip import (
    _central_directory_header,
    _data_descriptor,
    _eocd,
    _local_header,
    _zip64_eocd,
    _zip64_eocd_locator,
    exceptions,
)


class StreamParser:
    class _State(int, enum.Enum):
        UNKNOWN = 0
        LOCAL_HEADER = 1
        DATA_DESCRIPTOR = 2
        CONTENT = 3
        CENTRAL_DIRECTORY_HEADER = 4
        ZIP64_EOCD = 5
        ZIP64_EOCD_LOCATOR = 6
        EOCD = 7

    def __init__(self):
        self.zip_state = StreamParser._State.LOCAL_HEADER
        self.buffer = io.BytesIO()
        self.decompressor = None
        self.header = None
        self.expect_descriptor = False
        self.content = io.BytesIO()
        self.end_of_files = False

    def feed(self, data: bytes):
        logger = logging.getLogger()

        # Update buffer
        self.buffer.write(data)

        # Process buffer
        while True:
            buf = self.buffer.getbuffer()
            logger.info("%s %s", self.zip_state, buf[:4].tobytes())
            if self.zip_state == StreamParser._State.LOCAL_HEADER:
                # Attempt to parse local header
                try:
                    self.header = _local_header.LocalHeader.from_memoryview(buf)
                except exceptions.IncompleteParse:
                    break
                except exceptions.BadMagic:
                    if buf[:4] == _central_directory_header.MAGIC:
                        self.zip_state = StreamParser._State.CENTRAL_DIRECTORY_HEADER
                        continue
                    else:
                        raise exceptions.BadMagic(buf[:4].tobytes())

                # Check compatibility
                if self.header.bit_flags.is_encrypted:
                    raise NotImplementedError()
                if self.header.min_version_needed > 20:
                    raise NotImplementedError()

                # Prepare for next state
                self.buffer = io.BytesIO(buf[len(self.header) :])
                self.buffer.seek(self.buffer.getbuffer().nbytes)
                self.decompressor = zlib.decompressobj(wbits=-zlib.MAX_WBITS)
                self.zip_state = StreamParser._State.CONTENT
            elif self.zip_state == StreamParser._State.CONTENT:
                self.content.write(self.decompressor.decompress(buf))
                self.buffer = io.BytesIO(self.decompressor.unused_data)
                self.buffer.seek(self.buffer.getbuffer().nbytes)
                if self.decompressor.eof:
                    yield self.header, self.content
                    if self.header.bit_flags.expect_descriptor:
                        self.zip_state = StreamParser._State.DATA_DESCRIPTOR
                    else:
                        self.header = None
                        self.zip_state = StreamParser._State.LOCAL_HEADER
                else:
                    break
            elif self.zip_state == StreamParser._State.DATA_DESCRIPTOR:
                # Attempt to parse data descriptor
                try:
                    descriptor = _data_descriptor.DataDescriptor.from_memoryview(buf)
                except exceptions.IncompleteParse:
                    break

                # Prepare for next state
                self.buffer = io.BytesIO(buf[len(descriptor) :])
                self.buffer.seek(self.buffer.getbuffer().nbytes)
                self.header = None
                self.zip_state = StreamParser._State.LOCAL_HEADER
            elif self.zip_state == StreamParser._State.CENTRAL_DIRECTORY_HEADER:
                # Attempt to parse central directory header
                try:
                    header = _central_directory_header.CentralDirectoryHeader.from_memoryview(
                        buf
                    )
                except exceptions.IncompleteParse:
                    break
                except exceptions.BadMagic:
                    logger.info("HIT")
                    if buf[:4] == _zip64_eocd.MAGIC:
                        self.zip_state = StreamParser._State.ZIP64_EOCD
                        continue
                    elif buf[:4] == _eocd.MAGIC:
                        self.zip_state = StreamParser._State.EOCD
                        continue
                    else:
                        raise exceptions.BadMagic(buf[:4].tobytes())
                self.end_of_files = True

                # Prepare for next state
                self.buffer = io.BytesIO(buf[len(header) :])
                self.buffer.seek(self.buffer.getbuffer().nbytes)
            elif self.zip_state == StreamParser._State.ZIP64_EOCD:
                # Attempt to parse Zip64 end of central directory
                try:
                    eocd = _zip64_eocd.Zip64EOCD.from_memoryview(buf)
                except exceptions.IncompleteParse:
                    break
                logger.info("ZIP64 %s", eocd)

                # Prepare for next state
                self.buffer = io.BytesIO(buf[len(eocd) :])
                self.buffer.seek(self.buffer.getbuffer().nbytes)
                self.zip_state = StreamParser._State.ZIP64_EOCD_LOCATOR
            elif self.zip_state == StreamParser._State.ZIP64_EOCD_LOCATOR:
                # Attempt to parse Zip64 end of central directory locator
                try:
                    locator = _zip64_eocd_locator.Zip64EOCDLocator.from_memoryview(buf)
                except exceptions.IncompleteParse:
                    break

                # Prepare for next state
                self.buffer = io.BytesIO(buf[len(locator) :])
                self.buffer.seek(self.buffer.getbuffer().nbytes)
                self.zip_state = StreamParser._State.EOCD
            elif self.zip_state == StreamParser._State.EOCD:
                # Attempt to parse end of central directory
                try:
                    eocd = _eocd.EOCD.from_memoryview(buf)
                except exceptions.IncompleteParse:
                    break

                # Prepare for next state
                self.buffer = io.BytesIO(buf[len(eocd) :])
                self.buffer.seek(self.buffer.getbuffer().nbytes)
            else:
                raise Exception("Bad state")

    def flush(self):
        raise NotImplementedError()
