from utils import YeniDepremler, DepremBildirici, Database, TelegramClient
from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton, Message
from pyrogram import filters, enums, client, idle
import tgcrypto

telegram = TelegramClient()
#depremler = YeniDepremler()

sehirler=["Adana", "Adıyaman", "Afyon", "Ağrı", "Amasya", "Ankara", "Antalya", "Artvin", "Aydın", "Balıkesir", "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur", "Bursa", "Çanakkale", "Çankırı", "Çorum", "Denizli", "Diyarbakır", "Edirne", "Elazığ", "Erzincan", "Erzurum", "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane", "Hakkari", "Hatay", "Isparta", "İçel (Mersin)", "İstanbul", "İzmir", "Kars", "Kastamonu", "Kayseri", "Kırklareli", "Kırşehir", "Kocaeli", "Konya", "Kütahya", "Malatya", "Manisa", "Kahramanmaraş", "Mardin", "Muğla", "Muş", "Nevşehir", "Niğde", "Ordu", "Rize", "Sakarya", "Samsun", "Siirt", "Sinop", "Sivas", "Tekirdağ", "Tokat", "Trabzon", "Tunceli", "Şanlıurfa", "Uşak", "Van", "Yozgat", "Zonguldak", "Aksaray", "Bayburt", "Karaman", "Kırıkkale", "Batman", "Şırnak", "Bartın", "Ardahan", "Iğdır", "Yalova", "Karabük", "Kilis", "Osmaniye", "Düzce"]

@telegram.on_message(filters.command("depremler") & filters.private)
async def yeni_depremler(client: client.Client, message: Message):
    return await message.reply("İl Seçin: ", reply_markup=ReplyKeyboardMarkup([[KeyboardButton(sehir)] for sehir in sehirler]))

@telegram.on_message(filters.regex("[A-ZŞĞÜÇÖİI][a-z]+") & filters.private)
async def tum_depremler(client: client.Client, message: Message):
    db = Database()
    datas = db.get(id=707743280, order_by_id=True)
    print(datas)
    if datas:
        for data in datas:
            await YeniDepremler.send_to_telegram(YeniDepremler, client, DepremBildirici(**data), chat=message.chat.id)

telegram.start()
idle()
