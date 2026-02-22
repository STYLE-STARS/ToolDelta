import struct
import msgpack
from dataclasses import dataclass
from io import BytesIO
from tooldelta.constants.packets import PacketIDS
from tooldelta.mc_bytes_packet.base_bytes_packet import BaseBytesPacket
from typing import Any


@dataclass
class PyRpc(BaseBytesPacket):
    Value: Any = None
    OperationType: int = 0

    def name(self) -> str:
        return "PyRpc"

    def custom_packet_id(self) -> int:
        return 4

    def real_packet_id(self) -> int:
        return PacketIDS.IDPyRpc

    def encode(self) -> bytes:
        raise NotImplementedError("Encode packet.PyRpc is not support")

    def decode(self, bs: bytes):
        reader = BytesIO(bs)
        length = 0
        shift = 0
        # 处理PyRpc的Value字段开头的VarInt
        while True:
            b = reader.read(1)[0]
            length |= (b & 0x7F) << shift
            if (b & 0x80) == 0:
                break
            shift += 7
        msgpack_bytes = reader.read(length)
        self.Value = msgpack.unpackb(msgpack_bytes, raw=False, strict_map_key=False)
        operation_type_bytes = bs[-4:]
        self.OperationType = struct.unpack("<I", operation_type_bytes)[0]
