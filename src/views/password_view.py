import string, secrets, hashlib, base64
from pathlib import Path
from cryptography.fernet import Fernet, InvalidToken

class FernetHasher:
    RAMDOM_STRING_CHARS = string.ascii_lowercase + string.ascii_uppercase
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    KEY_DIR = BASE_DIR / 'keys'

    def __init__(self, key):
        if not isinstance(key, bytes):
            key = key.encode()

        self.fernet = Fernet(key)

    @classmethod
    def _get_ramdom_string(cls, length=32):
        ramdom_string = ''

        for i in range(length):
            ramdom_string = ramdom_string + secrets.choice(cls.RAMDOM_STRING_CHARS)

        return ramdom_string

    @classmethod
    def create_key(cls, archive=False):
        value = cls._get_ramdom_string()
        hasher = hashlib.sha256(value.encode('utf-8')).digest()
        key = base64.b64encode(hasher)

        if archive:
            return key, cls.archive_key(key)
        
        return key, None

    @classmethod
    def archive_key(cls, key):
        file_name = f'key_{cls._get_ramdom_string(length=8)}.key'
        while Path(cls.KEY_DIR / file_name).exists():
            file_name = f'key_{cls._get_ramdom_string(length=8)}.key'

        with open(cls.KEY_DIR / file_name, 'wb') as file:
            file.write(key)
        
        return cls.KEY_DIR / file_name

    def encrypt(self, value):
        if not isinstance(value, bytes):
            value = value.encode()

        return self.fernet.encrypt(value)

    def decrypt(self, value):
        if not isinstance(value, bytes):
            value = value.encode()
        
        try:
            return self.fernet.decrypt(value).decode()
        except InvalidToken as err:
            return 'Token inválido'

print(FernetHasher.create_key('1234'))
