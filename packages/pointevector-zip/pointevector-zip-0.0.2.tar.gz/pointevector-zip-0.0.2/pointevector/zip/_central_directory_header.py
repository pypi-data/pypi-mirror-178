import dataclasses

from pointevector.zip import _compression, _flags, exceptions

MAGIC = b"PK\x01\x02"
_STATIC_SIZE_ = 46


@dataclasses.dataclass(frozen=True)
class CentralDirectoryHeader:
    version_created_by: int
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
    comment_length: int
    file_start_disk: int
    internal_file_attributes: bytes
    external_file_attributes: bytes
    local_file_header_offset: int
    filename: str = ""
    extra_field: bytes = b""
    comment: str = ""

    @classmethod
    def from_memoryview(cls, view: memoryview):
        if view.nbytes < _STATIC_SIZE_:
            raise exceptions.IncompleteParse()

        if view[:4] != MAGIC:
            raise exceptions.BadMagic(view[:4].tobytes())

        filename_length = int.from_bytes(view[28:30], byteorder="little")
        extra_field_length = int.from_bytes(view[30:32], byteorder="little")
        if extra_field_length > 0:
            raise NotImplementedError()
        comment_length = int.from_bytes(view[32:34], byteorder="little")

        if view.nbytes < (
            _STATIC_SIZE_ + filename_length + extra_field_length + comment_length
        ):
            raise exceptions.IncompleteParse()

        try:
            compression_method = _compression.CompressionMethod(
                int.from_bytes(view[10:12], byteorder="little")
            )
        except ValueError:
            raise NotImplementedError()

        bit_flags = _flags.BitFlags.from_bytes(
            compression_method=compression_method, data=view[8:10]
        )

        return cls(
            version_created_by=int.from_bytes(view[4:6], byteorder="little"),
            min_version_needed=int.from_bytes(view[6:8], byteorder="little"),
            bit_flags=bit_flags,
            compression_method=compression_method,
            last_modified_time=view[12:14].tobytes(),
            last_modified_date=view[14:16].tobytes(),
            uncompressed_checksum=view[16:20].tobytes(),
            compressed_size=int.from_bytes(view[20:24], byteorder="little"),
            uncompressed_size=int.from_bytes(view[24:28], byteorder="little"),
            filename_length=filename_length,
            extra_field_length=extra_field_length,
            comment_length=comment_length,
            file_start_disk=int.from_bytes(view[34:36], byteorder="little"),
            internal_file_attributes=view[36:38].tobytes(),
            external_file_attributes=view[38:40].tobytes(),
            local_file_header_offset=int.from_bytes(view[40:46], byteorder="little"),
            filename=view[_STATIC_SIZE_ : (_STATIC_SIZE_ + filename_length)]
            .tobytes()
            .decode("utf-8" if bit_flags.uses_utf8 else "cp437"),
            comment=view[
                (_STATIC_SIZE_ + filename_length + extra_field_length) : (
                    _STATIC_SIZE_
                    + filename_length
                    + extra_field_length
                    + comment_length
                )
            ]
            .tobytes()
            .decode("utf-8" if bit_flags.uses_utf8 else "cp437"),
        )

    def __len__(self):
        return (
            _STATIC_SIZE_
            + self.filename_length
            + self.extra_field_length
            + self.comment_length
        )
