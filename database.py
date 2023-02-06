from MentoDB import Mento, MentoConnection, PrimaryKey, UniqueMatch
from models import EarthQuakeModel
con = MentoConnection("./quakes.db")
database = Mento(con, default_table="quakes")

database.create("quakes", model=EarthQuakeModel)

class Database:
    def __init__(self) -> None:
        self.db = database
    
    def auto_id(cls):
        import random
        number = random.randint(1000000, 999999999)
        if cls.get(id=number, order_by_id=True):
            return cls.auto_id()
        return number
    def insert(self,
    konum_il: str = " ",
    konum_ilce: str = " ",
    konum_apartman: str = " ",
    konum_mahalle: str = " ",
    kaynak: str = " ",
    telefon: int = "Bilinmiyor",
    isim: str = " "):
        id = self.auto_id()
        data = self.db.insert(self.db.default_table, data=dict(id=id, konum_il=konum_il, konum_ilce = konum_ilce,
    konum_apartman= konum_apartman,
    konum_mahalle= konum_mahalle,
    kaynak = kaynak,
    telefon = "Bilinmiyor" if not telefon else str(telefon).lstrip("+").lstrip("9"),
    isim = isim), check_model=EarthQuakeModel)
        if isinstance(data, list): data = data[0]
        if data:
            data.update({"id": id})
        return data

    def update(self, 
    id: int = 0,
    konum_il: str = " ",
    konum_ilce: str = " ",
    konum_apartman: str = " ",
    konum_mahalle: str = " ",
    kaynak: str = " ",
    telefon: int = "Bilinmiyor",
    isim: str = " "):
        return self.db.update(self.db.default_table, data=dict(id=self.auto_id(), konum_il=konum_il, konum_ilce = konum_ilce,
    konum_apartman= konum_apartman,
    konum_mahalle= konum_mahalle,
    kaynak = kaynak,
    telefon = "Bilinmiyor" if not telefon else str(telefon).lstrip("+").lstrip("9"),
    isim = isim), where=dict(id=id, isim=isim), model=EarthQuakeModel)
    def get(cls, id: int = 0, il: str = "Adana", ilce: str = "Çukurova", order_by_id: bool = False):
        data = cls.db.select(cls.db.default_table, model=EarthQuakeModel, where={"id": id} if order_by_id else {"konum_il": il} if il and not ilce else {"konum_il": il, "konum_ilce": ilce} if il and ilce else {})
        if data:
            return data
        return []
    