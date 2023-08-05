import dataclasses
import enum


class CompressionMethod(int, enum.Enum):
    # STORED = 0
    DEFLATED = 8
    # ZSTANDARD = 93


class DeflateCompressionOption(int, enum.Enum):
    NORMAL = 0


@dataclasses.dataclass(frozen=True)
class DeflateFlags:
    compression_option: DeflateCompressionOption
    enhanced_deflating: bool

    @classmethod
    def from_bytes(cls, data: bytes):
        compression_option = (data[0] & 0x06) >> 1
        if compression_option not in (i.value for i in DeflateCompressionOption):
            raise NotImplementedError()
        compression_option = DeflateCompressionOption(compression_option)

        return cls(
            compression_option=compression_option,
            enhanced_deflating=bool((data[0] & 0x10) >> 4),
        )
