"""Python bindings for PGP key related objects in the sett rust crate."""

import os
from dataclasses import dataclass
from typing import Tuple

from ._sett_rs import (
    Key as Key,
    KeyType as KeyType,
    UserID as UserID,
    Validity as Validity,
    read_cert,
)

__all__ = ["Cert", "Key", "KeyType", "UserID", "Validity"]


class KeyParsingError(Exception):
    """Error raised when an input appears to not be a proper PGP key."""

    def __init__(self, detail: str):
        super().__init__(
            "Loading of PGP key failed. The input (file or bytes) is probably "
            f"not a proper PGP key. Detailed error: {detail}"
        )


@dataclass(frozen=True)
class Cert:
    """PGP certificate representation (public PGP key).

    Creating a new Cert instance should be done via either:
     * Cert.from_bytes() - load a Cert from a binary data stream.
     * Cert.from_file()  - load a Cert from a file on disk.
    """

    uids: Tuple[UserID, ...]
    keys: Tuple[Key, ...]
    validity: Validity

    @classmethod
    def from_bytes(cls, src: bytes) -> "Cert":
        try:
            c = read_cert(src)
        except RuntimeError as e:
            raise KeyParsingError(detail=str(e)) from e

        return cls(uids=tuple(c.uids), keys=tuple(c.keys), validity=c.validity)

    @classmethod
    def from_file(cls, src_file: str) -> "Cert":
        with open(os.path.expanduser(src_file), mode="rb") as f:
            return cls.from_bytes(src=f.read())

    @property
    def primary_key(self) -> Key:
        return self.keys[0]

    @property
    def fingerprint(self) -> str:
        return self.primary_key.fingerprint

    @property
    def key_id(self) -> str:
        return self.primary_key.key_id

    @property
    def uid(self) -> UserID:
        return self.uids[0]

    @property
    def subkeys(self) -> Tuple[Key, ...]:
        return self.keys[1:]
