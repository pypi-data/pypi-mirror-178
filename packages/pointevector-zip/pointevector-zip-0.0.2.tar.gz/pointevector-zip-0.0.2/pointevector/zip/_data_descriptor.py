import dataclasses

from pointevector.zip import exceptions


MAGIC = b"PK\x07\x08"
_STATIC_SIZE_ = 12


@dataclasses.dataclass(frozen=True)
class DataDescriptor:
    has_signature: bool
    uncompressed_checksum: bytes
    compressed_size: int
    uncompressed_size: int

    @classmethod
    def from_memoryview(cls, view: memoryview):
        if view.nbytes < _STATIC_SIZE_:
            raise exceptions.IncompleteParse()

        has_signature = view[:2] == MAGIC[:2]
        if has_signature and view[:4] != MAGIC:
            raise exceptions.BadMagic(view[:4].tobytes())

        if has_signature and view.nbytes < _STATIC_SIZE_ + 4:
            raise exceptions.IncompleteParse()

        return cls(
            has_signature=has_signature,
            uncompressed_checksum=(view[4:8] if has_signature else view[:4]).tobytes(),
            compressed_size=int.from_bytes(
                view[8:12] if has_signature else view[4:8],
                byteorder="little",
            ),
            uncompressed_size=int.from_bytes(
                view[12:16] if has_signature else view[8:12],
                byteorder="little",
            ),
        )

    def __len__(self):
        return _STATIC_SIZE_ + (4 if self.has_signature else 0)
