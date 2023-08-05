import dataclasses

from pointevector.zip import _compression, _flags, exceptions


MAGIC = b"PK\x03\x04"
_STATIC_SIZE_ = 30


@dataclasses.dataclass(frozen=True)
class LocalHeader:
    min_version_needed: int
    bit_flags: _flags.BitFlags
    compression_method: _compression.CompressionMethod
    last_modified_time: bytes
    last_modified_date: bytes
    uncompressed_checksum: bytes
    compressed_size: int
    uncompressed_size: int
    filename_length: int
    extra_field_length: int
    filename: str = ""
    extra_field: bytes = b""

    @classmethod
    def from_memoryview(cls, view: memoryview):
        if view.nbytes < _STATIC_SIZE_:
            raise exceptions.IncompleteParse()

        if view[:4] != MAGIC:
            raise exceptions.BadMagic(view[:4].tobytes())

        filename_length = int.from_bytes(view[26:28], byteorder="little")
        extra_field_length = int.from_bytes(view[28:30], byteorder="little")
        if extra_field_length > 0:
            raise NotImplementedError()

        if view.nbytes < (_STATIC_SIZE_ + filename_length + extra_field_length):
            raise exceptions.IncompleteParse()

        try:
            compression_method = _compression.CompressionMethod(
                int.from_bytes(view[8:10], byteorder="little")
            )
        except ValueError:
            raise NotImplementedError()

        bit_flags = _flags.BitFlags.from_bytes(
            compression_method=compression_method, data=view[6:8]
        )

        return cls(
            min_version_needed=int.from_bytes(view[4:6], byteorder="little"),
            bit_flags=bit_flags,
            compression_method=compression_method,
            last_modified_time=view[10:12].tobytes(),
            last_modified_date=view[12:14].tobytes(),
            uncompressed_checksum=view[14:18].tobytes(),
            compressed_size=int.from_bytes(view[18:22], byteorder="little"),
            uncompressed_size=int.from_bytes(view[22:26], byteorder="little"),
            filename_length=filename_length,
            extra_field_length=extra_field_length,
            filename=view[_STATIC_SIZE_ : (_STATIC_SIZE_ + filename_length)]
            .tobytes()
            .decode("utf-8" if bit_flags.uses_utf8 else "cp437"),
        )

    def __len__(self):
        return _STATIC_SIZE_ + self.filename_length + self.extra_field_length
