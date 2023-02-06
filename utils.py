from requests import post, get
from bs4 import BeautifulSoup as XParser
from database import Database
from pyrogram import client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import json, re

class TelegramClient(object):
    def __new__(cls, config_path: str = "./config.json") -> client.Client:
        with open(config_path) as config:
            credentials = config.read()
            return client.Client(**json.loads(credentials))


class DepremBildirici(object):
    konum_il: str
    konum_ilce: str
    konum_apartman: str
    konum_mahalle: str
    kaynak: str
    telefon: int
    isim: str
    def __new__(cls, konum_il: str = " ",
    konum_ilce: str = " ",
    konum_apartman: str = " ",
    konum_mahalle: str = " ",
    kaynak: str = " ",
    telefon: int = "Bilinmiyor",
    isim: str = " "):
        cls.konum_il = konum_il
        cls.konum_ilce = konum_ilce
        cls.konum_apartman = konum_apartman
        cls.konum_mahalle = konum_mahalle
        cls.kaynak = kaynak
        cls.telefon = telefon
        cls.isim = isim
        return super().__new__(cls)
    
    def enkaz_bildirim_ekle(cls, konum_il: str = " ",
    konum_ilce: str = " ",
    konum_apartman: str = " ",
    konum_mahalle: str = " ",
    kaynak: str = " ",
    telefon: int = "Bilinmiyor",
    isim: str = " "):
        cls.db = Database()
        res = cls.db.insert(
            konum_il=konum_il, konum_ilce = konum_ilce,
            konum_apartman= konum_apartman,
            konum_mahalle= konum_mahalle,
            kaynak = kaynak,
            telefon = "Bilinmiyor" if not telefon else str(telefon).lstrip("+").lstrip("9"),
            isim = isim
            )
        
        return cls.db.get(id=res.get("id", 0), il=konum_il, ilce=konum_ilce, order_by_id=True)
    
    async def enkaz_bildirim(cls):
        response = post("https://depremyardim.com", headers={"accept": "application/json"}, data={"konum_il": cls.konum_il, "konum_ilce": cls.konum_ilce, "konum_mahalle": cls.konum_mahalle, "konum_apartman":cls.konum_apartman, "kaynak":cls.kaynak, "telefon": cls.telefon, "isimsoyisim": cls.isim})
        if 200 <= response.status_code < 300:
            return cls.enkaz_bildirim_ekle(
                konum_il=cls.konum_il, konum_ilce = cls.konum_ilce,
                konum_apartman= cls.konum_apartman,
                konum_mahalle= cls.konum_mahalle,
                kaynak = cls.kaynak,
                telefon = "Bilinmiyor" if not cls.telefon else str(cls.telefon).lstrip("+").lstrip("9"),
                isim = cls.isim
            )
    def site_enkaz_bildirimi(cls, 
        konum_il: str = " ",
        konum_ilce: str = " ",
        konum_apartman: str = " ",
        konum_mahalle: str = " ",
        kaynak: str = " ",
        telefon: int = "Bilinmiyor",
        isim: str = " "
        ):
            r = post(r.url, headers={"accept": "application/json"}, data={"konum_il": konum_il, "konum_ilce": konum_ilce, "konum_mahalle": konum_mahalle, "konum_apartman":konum_apartman, "kaynak": kaynak, "telefon": telefon, "isimsoyisim": isim})
            if 200 <= r.status_code < 300 or r.status_code:
                return cls.db.insert(konum_il=konum_il, konum_ilce=konum_ilce, konum_mahalle=konum_mahalle, konum_apartman=konum_apartman, telefon=telefon, kaynak=kaynak)



class YeniDepremler:
    def __new__(cls, website: str = "https://depremyardim.com/"):
        cls.r = r = get(website, headers={"accept": "application/json"})
        cls.parser = XParser(r.text.lower().replace("'", "\'").replace('"', '\"'), "html.parser")
        cls.chat = "depremenkazbildirim"
        cls.notifies = notifies = cls.parser.select_one("tbody").select("tr")

        for notify in notifies:
            veri = notify.find("th").text
            veri.lower().replace("ı", "i").replace("İ", "I").replace("ş", "s").replace("ü", "u").replace("ö", "o").replace("ğ", "g").replace("ç", "c")
            il = veri.split("\n")[1].strip()
            ilce = notify.select_one("td").text.strip()
            adres = notify.text.split("adres :")[-1].strip()
            isim = veri.split("sim :")[1].strip()
            kaynak = veri.split("sim :")[1][veri.find("kaynak :"):].strip()

            telefon_eslesme = re.search("(\d{10})", notify.text)
            if telefon_eslesme:
                telefon = telefon_eslesme.groups()[0]
            else:
                telefon = "Bilinmiyor"
            isaretci = DepremBildirici(konum_il=il, konum_ilce=ilce, konum_mahalle=adres, kaynak=kaynak, telefon=telefon, isim=isim)
            cls.response =  Database().insert(konum_il=il, konum_ilce=ilce, konum_mahalle=adres, kaynak=kaynak, telefon=telefon, isim=isim)
            print(cls.formatter(cls, isaretci))
            cls.send_to_telegram(cls, TelegramClient(), isaretci, chat=cls.chat)
        return super().__new__(cls)
    def formatter(cls, cursor: DepremBildirici):
        format_text = f"""[**YENI BILDIRIM]**\n**İsim:** **{cursor.isim}\n**Il:** {cursor.konum_il}\n**Ilçe:** {cursor.konum_ilce}\n**Mahalle/Adres:** {cursor.konum_mahalle if cursor.konum_mahalle else "Belirsiz"}\n**Telefon:** [{cursor.telefon}](tel:{cursor.telefon})"""
        return format_text
    async def send_to_telegram(cls, bot: client.Client, cursor: DepremBildirici, chat: str | int = None):
        print("telegrama gönderdim")
        if chat: cls.chat = chat
        d = await bot.send_message(cls.chat, cls.formatter(cursor), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Son Depremleri Gör", url="https://t.me/DepremBildirimBot")]]))
        return print(d)