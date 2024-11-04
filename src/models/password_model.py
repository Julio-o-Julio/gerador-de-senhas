from datetime import datetime
from pathlib import Path

class BaseModel:
    BASE_DIR = Path(__file__).resolve().parent.parent
    DB_DIR = BASE_DIR / 'db'
    
    def save(self):
        db_path = Path(self.DB_DIR)
        if not db_path.exists():
            db_path.mkdir()

        table_path = Path(db_path / f'{self.__class__.__name__}.txt')
        if not table_path.exists():
            table_path.touch()
        
        with open(table_path, 'a') as file:
            file.write('|'.join(list(map(str, self.__dict__.values()))))
            file.write('\n')
    
    @classmethod
    def get(cls):
        db_path = Path(cls.DB_DIR)
        if not db_path.exists():
            db_path.mkdir()

        table_path = Path(db_path / f'{cls.__name__}.txt')
        if not table_path.exists():
            table_path.touch()
        
        with open(table_path, 'r') as file:
            data = file.readlines()

        results = []
        atributes = vars(cls())

        for i in data:
            split_values = i.split('|')
            tmp_dict = dict(zip(atributes, split_values))
            results.append(tmp_dict)

        return results

class Password(BaseModel):
    def __init__(self, domain=None, password=None, expire=False):
        self.domain = domain
        self.password = password
        self.expire = expire
        self.create_at = datetime.now().isoformat()
