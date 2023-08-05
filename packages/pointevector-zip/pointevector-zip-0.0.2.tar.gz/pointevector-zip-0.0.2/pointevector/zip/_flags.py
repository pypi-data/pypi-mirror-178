import dataclasses
from typing import Union

from pointevector.zip import _compression


@dataclasses.dataclass(frozen=True)
class BitFlags:
    is_encrypted: bool  # Bit 0
    expect_descriptor: bool  # Bit 3
    uses_utf8: bool  # Bit 11
    deflate_flags: Union[_compression.DeflateFlags, None] = None

    @classmethod
    def from_bytes(
        cls, compression_method: _compression.CompressionMethod, data: bytes
    ):
        return cls(
            is_encrypted=bool(data[0] & 0x01),
            expect_descriptor=bool((data[0] & 0x08) >> 3),
            uses_utf8=bool((data[1] & 0x08) >> 3),
            deflate_flags=_compression.DeflateFlags.from_bytes(data)
            if compression_method == _compression.CompressionMethod.DEFLATED
            else None,
        )
