import json
import time
from dataclasses import dataclass, field

from spotify_internal import login

__all__ = [
    'Tokens',
    'Credentials',
    'prepare_url',
    'INTERNAL_BASE_URL',
    'INTERNAL_URL'
]


INTERNAL_BASE_URL = 'https://api-partner.spotify.com/pathfinder/v1/query'
INTERNAL_URL = 'https://api-partner.spotify.com/pathfinder/v1/query?operationName=%(operation_name)s&variables=%(variables)s&extensions={"persistedQuery":{"version":1,"sha256Hash":"%(hash)s"}}'

PERSISTED_QUERY_HASH = {
    'searchDesktop': '1d3a8f81abf4f33f49d1e389ed0956761af669eedb62a050c6c7bce5c66070bb',
    'browseAll': '864fdecccb9bb893141df3776d0207886c7fa781d9e586b9d4eb3afa387eea42',
    'home': '3a67ee0ea6abad2ebad2e588a9aa130fc98d6b553f5b05ac6467503d02133bdc',
    'fetchPlaylistForRecentlyPlayed': '357c4bb9f0dcce45dfee3f99371f79c9abec57c274a795bcdfd6050f07a63dde',
    'fetchAlbumForRecentlyPlayed': '4b210cde21b092f94056b108317be7ddc917e99cc684138ffceae32d8fb1a3f1',
    'homeSection': '60c1b102f74bea3bb2062eb4b3979860c7ff5c96f4e9586e9f8bfa8619c8ad07',
    'fetchLibraryTracks': '8474ec383b530ce3e54611fca2d8e3da57ef5612877838b8dbf00bd9fc692dfb'
}


@dataclass
class Credentials:
    username: str
    password: str

    def get_tokens(self) -> "Tokens":
        Tokens.from_creds(self)


@dataclass
class Tokens:
    access_token: str
    client_token: str = field(default="AADHU245K/LDrxWbEFzVu/6SXnvisFYKHWL/5GOArj4t0pova2MSLooib1A6y+nzd6rbWeoMBX1/3TA1rDCWm8hHNZTGxGbcns93k9AfquPGSAkCbEOfaFGyMeHhm28qPSG8XGyGdHJLivFfeI7wfnlsQat7GtFkB4HhEoiX4+3sSLUtt2Yks/Ruh9MUialJI2nyhHLA5jHDivKJdNPeq402VW4PaK3kF2E0qMyg+abRdyeNpc165vJcE69ZiF+CI7gsIayKRK2gYjxi502F55Zclj/LZIxvhUgRJ1hj9WKa93eYCw==", init=False)

    def __post_init__(self):
        object.__setattr__(self, 'expires_at', (int(time.time()) + 3600) - 10)

    @classmethod
    def from_credentials(cls, credentials: Credentials) -> "Tokens":
        return cls(login.get_auth_token(credentials))


def prepare_url(operation_name: str, variables: dict, hash: str):
    url = INTERNAL_URL % {'operation_name': operation_name,
                          'variables': json.dumps(variables),
                          'hash': hash}
    url = url.replace(' ', '').replace("'", '"')
    return url


if __name__ == '__main__':
    tokens = Tokens.lmao('sadfa')
    print(tokens.client_token)
    print(tokens.expires_at)
