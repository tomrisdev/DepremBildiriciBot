from pydantic.dataclasses import dataclass
from pydantic import BaseModel
from MentoDB import PrimaryKey
@dataclass
class EarthQuakeModel(BaseModel):
    id: PrimaryKey(int)
    konum_il: str
    konum_ilce: str
    konum_apartman: str
    konum_mahalle: str
    kaynak: str
    telefon: str
    isim: str