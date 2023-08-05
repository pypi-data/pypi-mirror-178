import dataclasses

from pointevector.zip import exceptions

MAGIC = b"PK\x06\x06"
_STATIC_SIZE_ = 56


@dataclasses.dataclass(frozen=True)
class Zip64EOCD:
    size_of_zip64_eocd: int
    version_created_by: int
    min_version_needed: int
    disk_number: int
    eocd_start_disk: int
    cd_records_on_disk: int
    total_cd_records: int
    cd_size: int
    cd_start_offset: int
    zip64_extensible_data_sector: bytes

    @classmethod
    def from_memoryview(cls, view: memoryview):
        if view.nbytes < _STATIC_SIZE_:
            raise exceptions.IncompleteParse()

        if view[:4] != MAGIC:
            raise exceptions.BadMagic(view[:4].tobytes())

        size_of_zip64_eocd = int.from_bytes(view[4:12], byteorder="little")
        if (
            view.nbytes < size_of_zip64_eocd + 12
        ):  # size does not include signature and the size field
            raise exceptions.IncompleteParse()

        return cls(
            size_of_zip64_eocd=size_of_zip64_eocd,
            version_created_by=int.from_bytes(view[12:14], byteorder="little"),
            min_version_needed=int.from_bytes(view[14:16], byteorder="little"),
            disk_number=int.from_bytes(view[16:20], byteorder="little"),
            eocd_start_disk=int.from_bytes(view[20:24], byteorder="little"),
            cd_records_on_disk=int.from_bytes(view[24:32], byteorder="little"),
            total_cd_records=int.from_bytes(view[32:40], byteorder="little"),
            cd_size=int.from_bytes(view[40:48], byteorder="little"),
            cd_start_offset=int.from_bytes(view[48:56], byteorder="little"),
            zip64_extensible_data_sector=view[
                _STATIC_SIZE_ : (size_of_zip64_eocd + 12)
            ].tobytes(),
        )

    def __len__(self):
        return self.size_of_zip64_eocd + 12
