import requests
from bs4 import BeautifulSoup
import json
import sqlite3 as sql
import datetime
import locale

vt = sql.connect("db.sql")
im = vt.cursor()
im.execute("CREATE TABLE IF NOT EXISTS hisselerim ('hisse_kodu','lot','alis_fiyati')")
locale.setlocale(locale.LC_ALL, '')

def TarihiCek():
    now = datetime.datetime.now()
    return datetime.datetime.strftime(now, '%d %B %Y Saat: %H:%M')

def JsonImport(filename):
    with open(filename, 'r', encoding='utf-8') as dosya:
        sirketler = json.load(dosya)
    return sirketler

sirketler = JsonImport("sirketler_new.json")

def FiyatSorgula(sirketkodu):
    for veri in sirketler:
        if veri["kod"] == sirketkodu:
            return veri["kod"]


def ToplamFiyatHesapla():
    im.execute("""SELECT COUNT(*) FROM hisselerim""")
    sutunsayac = im.fetchone()[0]
    im.execute("SELECT * FROM hisselerim")
    toplamMaliyet = 0
    toplam = 0
    list = []
    text = ""
    for i in range(sutunsayac):
        veri = im.fetchone()
        url = f'https://www.google.com/finance/quote/{FiyatSorgula(veri[0])}:IST'
        print(FiyatSorgula(veri[0]))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        verix = soup.find('div', class_="YMlKec fxKbKc")
        fiyat = verix.text[1::].split(',')
        veri2 = float('.'.join(fiyat))
        yenifiyat = veri2*int(veri[1])
        maliyet = float(veri[1])*float(veri[2])
        kar_zarar = yenifiyat-maliyet
        kar_zarar_text1 = ""
        if kar_zarar > 0:
            kar_zarar_text1 = "+"+str(round(kar_zarar,2))
        else:
            kar_zarar_text1 = str(round(kar_zarar,2))
        a = [veri[0],veri[1],veri[2],round(maliyet,2),veri2,round(yenifiyat,3),f"{kar_zarar_text1} ₺"]
        list.append(a)
        toplamMaliyet += round(float(veri[1])*float(veri[2]),2)
        toplam += veri2*int(veri[1])
        text += f"**{veri[0]:<6}** -> {veri2:<6} | {veri[1]:<6} adet | {round(yenifiyat,3):<10}  | {kar_zarar_text1:<10} ₺\n"
    print(f"Veriler işlendi! {TarihiCek()}")
    toplam_kar_zarar = toplam-toplamMaliyet
    return text,round(toplam_kar_zarar,2),round(toplam,2)


def HisseEkle(list):
    hisse_kod = list[0]
    lot = int(list[1])
    alis_fiyati = float(list[2])
    im.execute("SELECT COUNT(*) FROM hisselerim")
    sutunsayi = im.fetchone()[0] 
    im.execute("SELECT hisse_kodu FROM hisselerim ")
    hisseler = []
    for i in range(sutunsayi):
        x = im.fetchone()[0]
        hisseler.append(x)
    print(hisseler) 
    if hisse_kod in hisseler:
        im.execute("SELECT COUNT(*) FROM hisselerim WHERE hisse_kodu = ?",(hisse_kod,))
        sutunsayi1 = im.fetchone()[0]
        im.execute("SELECT alis_fiyati FROM hisselerim WHERE hisse_kodu = ?",(hisse_kod,))
        alis_fiyatlari = []
        for i in range(sutunsayi1):
            y = float(im.fetchone()[0])
            alis_fiyatlari.append(y)
        print(alis_fiyatlari)
        if alis_fiyati in alis_fiyatlari:
            im.execute(f"SELECT lot FROM hisselerim WHERE hisse_kodu = ? OR alis_fiyati = ?",(hisse_kod,alis_fiyati,))
            yeni_lot = lot + int(im.fetchone()[0])
            print(yeni_lot)
            im.execute("UPDATE hisselerim SET lot = ? WHERE hisse_kodu = ? OR alis_fiyati = ?",(yeni_lot,hisse_kod,alis_fiyati))
            vt.commit()
        else:
            im.execute("INSERT INTO hisselerim VALUES (?,?,?)",(hisse_kod,lot,alis_fiyati))
            vt.commit()
    else:
        im.execute("INSERT INTO hisselerim VALUES (?,?,?)",(hisse_kod,lot,alis_fiyati))
        vt.commit()

        

    
