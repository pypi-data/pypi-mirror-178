from __future__ import annotations
from typing import List, Optional, Sequence, Tuple

from parsec._parsec_pyi.crypto import VerifyKey
from parsec._parsec_pyi.ids import UserID, DeviceID
from parsec._parsec_pyi.protocol import Trustchain
from parsec._parsec_pyi.time import DateTime, TimeProvider
from parsec._parsec_pyi.certif import (
    UserCertificate,
    RevokedUserCertificate,
    DeviceCertificate,
)

class TrustchainContext:
    def __init__(
        self,
        root_verify_key: VerifyKey,
        time_provider: TimeProvider,
        cache_validity: int,
    ) -> None: ...
    @property
    def cache_validity(self) -> int: ...
    def invalidate_user_cache(self, user_id: UserID) -> None: ...
    def get_user(self, user_id: UserID) -> Optional[UserCertificate]: ...
    def get_revoked_user(self, user_id: UserID) -> Optional[RevokedUserCertificate]: ...
    def get_device(self, device_id: DeviceID) -> Optional[DeviceCertificate]: ...
    def load_user_and_devices(
        self,
        trustchain: Trustchain,
        user_certif: bytes,
        revoked_user_certif: Optional[bytes] = None,
        devices_certifs: Sequence[bytes] = (),
        expected_user_id: Optional[UserID] = None,
    ) -> Tuple[UserCertificate, Optional[RevokedUserCertificate], List[DeviceCertificate],]: ...
    def load_trustchain(
        self,
        users: Sequence[bytes] = (),
        revoked_users: Sequence[bytes] = (),
        devices: Sequence[bytes] = (),
    ) -> Tuple[List[UserCertificate], List[RevokedUserCertificate], List[DeviceCertificate],]: ...

class TrustchainErrorException(BaseException, TrustchainError): ...

class TrustchainError:
    @property
    def path(self) -> str: ...
    @property
    def exc(self) -> str: ...
    @property
    def user_id(self) -> UserID: ...
    @property
    def device_id(self) -> DeviceID: ...
    @property
    def verified_timestamp(self) -> DateTime: ...
    @property
    def user_timestamp(self) -> DateTime: ...
    @property
    def expected(self) -> UserID: ...
    @property
    def got(self) -> UserID: ...
