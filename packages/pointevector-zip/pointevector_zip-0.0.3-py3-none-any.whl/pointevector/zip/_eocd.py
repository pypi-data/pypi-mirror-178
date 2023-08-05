import dataclasses

from pointevector.zip import exceptions

MAGIC = b"PK\x05\x06"
_STATIC_SIZE_ = 22


@dataclasses.dataclass(frozen=True)
class EOCD:
    disk_number: int
    cd_disk: int
    cd_records_on_disk: int
    total_cd_records: int
    cd_size: int
    cd_start_offset: int
    comment_length: int
    comment: str = ""

    @classmethod
    def from_memoryview(cls, view: memoryview):
        if view.nbytes < _STATIC_SIZE_:
            raise exceptions.IncompleteParse()

        if view[:4] != MAGIC:
            raise exceptions.BadMagic(view[:4].tobytes())

        comment_length = int.from_bytes(view[20:22], byteorder="little")

        if view.nbytes < (_STATIC_SIZE_ + comment_length):
            raise exceptions.IncompleteParse()

        return cls(
            disk_number=int.from_bytes(view[4:6], byteorder="little"),
            cd_disk=int.from_bytes(view[6:8], byteorder="little"),
            cd_records_on_disk=int.from_bytes(view[8:10], byteorder="little"),
            total_cd_records=int.from_bytes(view[10:12], byteorder="little"),
            cd_size=int.from_bytes(view[12:16], byteorder="little"),
            cd_start_offset=int.from_bytes(view[16:20], byteorder="little"),
            comment_length=comment_length,
            comment=view[_STATIC_SIZE_ : (_STATIC_SIZE_ + comment_length)]
            .tobytes()
            .decode("cp437"),
        )

    def __len__(self):
        return _STATIC_SIZE_ + self.comment_length
