import discord
from discord.ext import commands
from discord import Embed
from discord import Color
import asyncio
from borsa_bot import *

intents = discord.Intents.all()

class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(command_prefix='!', intents=intents, *args, **kwargs)

bot = MyBot()

@bot.event
async def on_ready():
    print(f'Bot {bot.user} olarak giriş yaptı!')

@bot.event
async def on_command_error(ctx, error):
    print(f'Hata: {error}')

def BorsaFonksiyon():
    embed = Embed(
        title='Hisselerim',
        description=f"Veriler \n {TarihiCek()} \n*Veriler 15 dakika gecikmelidir.*",
        color=discord.Color.blue(),
    )
    veri = ToplamFiyatHesapla()
    embed.add_field(name="**Hisse  |  Fiyat  |  Lot  |  Toplam  |  Kar/Zarar**", value=veri[0], inline=True)
    embed.add_field(name="Toplam Bakiye", value=f"{veri[2]} ₺", inline=False)
    embed.add_field(name="Toplam Kâr/Zarar", value=f"{veri[1]} ₺", inline=False)
    return embed
        
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith('!borsa-baslat'):
        await message.channel.send("Borsa sistemi başladı!\nDakikada bir veriler gönderilecektir.")
        while True:
            await message.channel.send(embed=BorsaFonksiyon())
            await asyncio.sleep(300) #300 saniye = 5 dakika
    if message.content.startswith('!borsaekle'):
        # Argümanları al
        args = message.content.split()[1:]
        
        # Eğer en az 3 argüman yoksa hata mesajı gönder
        if len(args) < 3:
            await message.channel.send("En az 3 argüman gerekli.")
            return
        HisseEkle(args)
        await message.channel.send(f"Listeye eklendi. {args[0]} | {args[1]} Adet | Alış Fiyatı: {args[2]}")
        
        
     

bot.run('MTE5ODYxODMxMzc0MDI2NzYwMA.Gtv51v.LCxxkMD4fhzq5uMWfXJxg-LgABsKw3JnOuhw7Y')

