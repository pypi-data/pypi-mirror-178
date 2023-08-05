"""Type hints (stub file) for the classes and functions exported from rust."""

from datetime import datetime
from enum import Enum
from typing import Sequence, List, Optional, Callable, Any

class SftpOpts:
    host: str
    port: int
    username: str
    destination_dir: str
    envelope_dir: Optional[str]
    pkey: Optional[str]
    pkey_password: Optional[str]

    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        destination_dir: Optional[str] = None,
        envelope_dir: Optional[str] = None,
        pkey: Optional[str] = None,
        pkey_password: Optional[str] = None,
    ) -> None: ...

def sftp_upload(
    files: Sequence[str],
    host: str,
    username: str,
    destination_dir: str,
    envelope_dir: Optional[str] = None,
    pkey: Optional[str] = None,
    pkey_password: Optional[str] = None,
    progress: Optional[Callable[[float], Any]] = None,
    buf_size: Optional[int] = None,
    two_factor_callback: Optional[Callable[[], str]] = None,
) -> None: ...
def encrypt(
    files: Sequence[str],
    recipients: Sequence[str],
    sender: Optional[str],
    password: Optional[str],
    dry_run: bool,
    force: bool,
    output: Optional[str] = None,
    purpose: Optional[str] = None,
    transfer_id: Optional[int] = None,
    compression_level: Optional[int] = None,
    max_cpu: Optional[int] = None,
    progress: Optional[Callable[[float], Any]] = None,
    remote: Optional[SftpOpts] = None,
    two_factor_callback: Optional[Callable[[], str]] = None,
) -> Optional[str]: ...
def decrypt(
    file: str,
    recipients: Sequence[str],
    signer: Optional[str],
    password: Optional[str],
    dry_run: bool,
    decrypt_only: bool,
    output: Optional[str] = None,
    max_cpu: Optional[int] = None,
    progress: Optional[Callable[[float], Any]] = None,
) -> Optional[str]: ...

class KeyType(Enum):
    Public: Any
    Secret: Any

class Validity(Enum):
    Expired: Any
    Invalid: Any
    Revoked: Any
    Unknown: Any
    Valid: Any

class UserID:
    value: bytes
    name: Optional[str]
    email: Optional[str]
    comment: Optional[str]

class Key:
    key_id: str
    key_type: KeyType
    fingerprint: str
    length: Optional[int]
    creation_date: datetime
    expiration_date: Optional[datetime]
    pub_key_algorithm: int
    validity: Validity

class Cert:
    key_id: str
    fingerprint: str
    uids: List[UserID]
    validity: Validity
    keys: List[Key]

def read_cert(src: bytes) -> Cert: ...
