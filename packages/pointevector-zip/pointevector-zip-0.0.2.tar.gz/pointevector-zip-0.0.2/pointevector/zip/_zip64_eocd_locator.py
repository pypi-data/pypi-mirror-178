import dataclasses

from pointevector.zip import exceptions

MAGIC = b"PK\x06\x07"
_STATIC_SIZE_ = 20


@dataclasses.dataclass(frozen=True)
class Zip64EOCDLocator:
    zip64_eocd_start_disk: int
    zip64_eocd_offset: int
    total_disks: int

    @classmethod
    def from_memoryview(cls, view: memoryview):
        if view.nbytes < _STATIC_SIZE_:
            raise exceptions.IncompleteParse()

        if view[:4] != MAGIC:
            raise exceptions.BadMagic(view[:4].tobytes())

        return cls(
            zip64_eocd_start_disk=int.from_bytes(view[4:8], byteorder="little"),
            zip64_eocd_offset=int.from_bytes(view[8:16], byteorder="little"),
            total_disks=int.from_bytes(view[16:20], byteorder="little"),
        )

    def __len__(self):
        return _STATIC_SIZE_
