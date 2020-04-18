# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import messagebox
import sqlite3

vt=sqlite3.connect("ürün kaydı.mb")
cr=vt.cursor()
cr.execute("CREATE TABLE if not exists üyeler (kullanici_adi, adi, soyadi, sifre)")
cr.execute("CREATE TABLE IF NOT EXISTS ürünler (ürün_adi, adet, fiyat, durum)")

ürün_listesi={"Klavye":[10,15,"Ucuz"],"Ekran":[15,50,"Pahalı"],"Fare":[20,7,"Ucuz"],"Mikrofon":[15,14,"Ucuz"]}
cr.execute("insert into üyeler (kullanici_adi, adi, soyadi, sifre) values (?,?,?,?)", ("admin","Muzaffer", "VANLI", "123456"))
for i in ürün_listesi:
    hata_gösterme=0
    cr.execute("select ürün_adi from ürünler")
    yazdır=cr.fetchall()
    for yaz in yazdır:
        if(yaz[0]==i):
            hata_gösterme=1
            break
    if(hata_gösterme==0):
        ürün_adi=i
        adet=ürün_listesi[i][0]
        fiyat=ürün_listesi[i][1]
        durum=ürün_listesi[i][2]
        cr.execute("INSERT INTO ürünler (ürün_adi,adet,fiyat,durum) VALUES (?,?,?,?)",(ürün_adi,adet,fiyat,durum))
        vt.commit()

def ürün_listesi():
    pencere2=Toplevel()
    pencere2.resizable(width=FALSE, height=FALSE)
    başlık=pencere2.title("Ürün Listesi")

    Ürün_adi=Label(pencere2, text="Ürün Adı", width=7, font="Times 12 underline")
    Adeti=Label(pencere2, text="Stok", width=7, font="Times 12 underline")
    Fiyati=Label(pencere2, text="Fiyat", width=7, font="Times 12 underline")
    Durumu=Label(pencere2, text="Durum", width=7, font="Times 12 underline")

    Ürün_adi.grid(row=1, column=0)
    Adeti.grid(row=1, column=1)
    Fiyati.grid(row=1, column=2)
    Durumu.grid(row=1, column=3)
    x=2
    cr.execute("select * from ürünler")
    yazdir=cr.fetchall()
    for yaz in yazdir:
        Ürün_ad=Label(pencere2, text=yaz[0], width=7)
        Adet=Label(pencere2, text=yaz[1], width=7)
        Fiyat=Label(pencere2, text=yaz[2], width=7)
        Durum=Label(pencere2, text=yaz[3], width=7)

        Ürün_ad.grid(row=x, column=0)
        Adet.grid(row=x, column=1)
        Fiyat.grid(row=x, column=2)
        Durum.grid(row=x, column=3)
        x=x+1
    uyarı=Label(pencere2, text="Ürün Satın Almak İçin Giriş Yapın", font="Times 11 bold")
    uyarı.grid(columnspan=4)

    geri=Button(pencere2,text="Geri", width=15, command=pencere2.destroy)
    geri.grid(columnspan=4)

def üye_girişi():
    pencere2=Toplevel()
    pencere2.geometry("255x110+535+250")
    başlık=pencere2.title("Üye Girişi")

    kullanıcı_adi=Label(pencere2,text="Kullanıcı Adı")
    kullanıcı_adi.grid(row=0, column=0)

    adi=Entry(pencere2)
    adi.grid(row=0, column=1)

    kullanıcı_şifre=Label(pencere2,text="Şifre")
    kullanıcı_şifre.grid(row=1, column=0)

    şifre=Entry(pencere2)
    şifre.grid(row=1, column=1)

    def giriş():
        ad=adi.get()
        şfre=şifre.get()
        hata_gösterme=0
        cr.execute("SELECT kullanici_adi,adi,soyadi,sifre FROM üyeler where kullanici_adi=(?) and sifre=(?)", (ad,şfre))
        yazdir=cr.fetchall()
        for yaz in yazdir:
            if(yaz[0]=="admin" and yaz[3]=="123456"):
                hata_gösterme=1
                pencere.destroy()

                ekran1=Tk()
                ekran1.tk_setPalette("red")
                ekran1.geometry("255x90+520+245")
                ekran1.resizable(width=FALSE, height=FALSE)
                başlık=ekran1.title("Admin")

                def ekle():
                    ürün_ekle=Toplevel()
                    ürün_ekle.geometry("215x95+540+245")
                    ürün_ekle.resizable(width=FALSE, height=FALSE)
                    başlık=ürün_ekle.title("Ürün Ekle")

                    adı=Label(ürün_ekle, text="Ürün Adı: ")
                    adı.grid(row=0, column=0)

                    ürün_adı=Entry(ürün_ekle)
                    ürün_adı.grid(row=0, column=1)

                    ürün_adet=Label(ürün_ekle, text="Adet: ")
                    ürün_adet.grid(row=1, column=0)

                    ürün_adeti=Entry(ürün_ekle)
                    ürün_adeti.grid(row=1, column=1)

                    ürün_fiyat=Label(ürün_ekle, text="Fiyat: ")
                    ürün_fiyat.grid(row=2, column=0)

                    ürün_fiyatı=Entry(ürün_ekle)
                    ürün_fiyatı.grid(row=2, column=1)

                    def kaydeti():
                        ürün_adi=ürün_adı.get()
                        adet=ürün_adeti.get()
                        fiyat=int(ürün_fiyatı.get())
                        durum="Pahalı"
                        cr.execute("INSERT INTO ürünler (ürün_adi, adet, fiyat, durum) VALUES (?,?,?,?)",(ürün_adi,adet,fiyat,durum))
                        vt.commit()

                        cr.execute("update ürünler set durum=\"Pahalı\" where (fiyat>(select AVG(fiyat) from ürünler))")
                        vt.commit()

                        cr.execute("update ürünler set durum=\"Ucuz\" where (fiyat<(select AVG(fiyat) from ürünler))")
                        vt.commit()
                        comman=ürün_ekle.destroy()
                        eklenen_ürün=str(ürün_adi)+" Ürünlere Eklendi"
                        messagebox.showinfo("Eklendi",eklenen_ürün)

                    geri=Button(ürün_ekle, text="Geri", width=10, command=ürün_ekle.destroy)
                    geri.grid(row=3, column=0)

                    kaydet=Button(ürün_ekle, text="Kaydet", width=12, command=kaydeti)
                    kaydet.grid(row=3, column=1)

                def silme():
                    ürün_sil=Toplevel()
                    ürün_sil.geometry("150x200+565+200")
                    ürün_sil.resizable(width=FALSE, height=FALSE)
                    başlık=ürün_sil.title("Sil")

                    liste=Listbox(ürün_sil)
                    liste.grid(columnspan=2)

                    cr.execute("select ürün_adi from ürünler")
                    yazdır=cr.fetchall()
                    for yaz in yazdır:
                        liste.insert(END, yaz[0])

                    def sil():
                        seçilen=liste.selection_get()
                        cr.execute("delete from ürünler where ürün_adi=(?)",(seçilen,))
                        vt.commit()
                        command=ürün_sil.destroy()
                        seçilen_ürün=str(seçilen)+" Ürünlerden Silindi"
                        messagebox.showinfo("Silindi",seçilen_ürün)

                    geri=Button(ürün_sil, text="Geri", width=8, command=ürün_sil.destroy)
                    geri.grid(row=1, column=0)

                    sil=Button(ürün_sil, text="Sil", width=10, command=sil)
                    sil.grid(row=1, column=1)

                def güncelle():
                    ürün_güncelle=Toplevel()
                    ürün_güncelle.geometry("150x200+565+200")
                    başlık=ürün_güncelle.title("Seç")
                    ürün_güncelle.resizable(width=FALSE, height=FALSE)

                    liste=Listbox(ürün_güncelle)
                    liste.grid(columnspan=2)

                    cr.execute("select ürün_adi from ürünler")
                    yazdır=cr.fetchall()
                    for yaz in yazdır:
                        liste.insert(END, yaz[0])

                    def güncelleme():
                        ürün_seçenek=Toplevel()
                        ürün_seçenek.geometry("345x75+470+250")
                        başlık=ürün_seçenek.title("Güncelleme")
                        ürün_seçenek.resizable(width=FALSE, height=FALSE)

                        def değiştir_ad():
                            değiştirme=Toplevel()
                            değiştirme.geometry("285x75+510+250")
                            başlık=değiştirme.title("Ad Güncelle")
                            değiştirme.resizable(width=FALSE, height=FALSE)

                            seçilen=liste.selection_get()
                            seçilen_yazı=str(seçilen)+" Ürünün Yeni Adı"

                            yeni_ad=Label(değiştirme, text=seçilen_yazı)
                            yeni_ad.grid(row=0, column=0)

                            ad=Entry(değiştirme)
                            ad.grid(row=0, column=1)

                            boşluk=Label(değiştirme)
                            boşluk.grid(rowspan=1)

                            def kaydet():
                                adi=ad.get()

                                cr.execute("update ürünler set ürün_adi=(?) where ürün_adi=(?)",(adi,seçilen))
                                vt.commit()

                                command=değiştirme.destroy()
                                command=ürün_seçenek.destroy()
                                command=ürün_güncelle.destroy()

                                messagebox.showinfo("Güncelleme", "Ürün Güncellendi")

                            kaydet=Button(değiştirme, text="Kaydet", width=13, command=kaydet)
                            kaydet.grid(row=2, column=1)

                        def değiştir_adet():
                            değiştirme=Toplevel()
                            değiştirme.geometry("285x75+510+250")
                            başlık=değiştirme.title("Adet Güncelle")
                            değiştirme.resizable(width=FALSE, height=FALSE)

                            seçilen=liste.selection_get()
                            seçilen_yazı=str(seçilen)+" Ürünün Yeni Adeti"

                            yeni_ad=Label(değiştirme, text=seçilen_yazı)
                            yeni_ad.grid(row=0, column=0)

                            ad=Entry(değiştirme)
                            ad.grid(row=0, column=1)

                            cr.execute("select adet from ürünler where ürün_adi=(?)", (seçilen,))
                            sayı=cr.fetchall()
                            yazı="Mevcut Adet: "+str(sayı[0][0])
                            ürün_sayısı=Label(değiştirme, text=yazı)
                            ürün_sayısı.grid(row=1, column=0)

                            def kaydet():
                                adi=ad.get()

                                cr.execute("update ürünler set adet=(?) where adet=(select adet from ürünler where ürün_adi=(?))",(adi,seçilen))
                                vt.commit()

                                command=değiştirme.destroy()
                                command=ürün_seçenek.destroy()
                                command=ürün_güncelle.destroy()

                                messagebox.showinfo("Güncelleme", "Ürün Güncellendi")

                            kaydet=Button(değiştirme, text="Kaydet", width=13, command=kaydet)
                            kaydet.grid(row=2, column=1)

                        def değiştir_fiyat():
                            değiştirme=Toplevel()
                            değiştirme.geometry("285x75+510+250")
                            başlık=değiştirme.title("Fiyat Güncelle")
                            değiştirme.resizable(width=FALSE, height=FALSE)

                            seçilen=liste.selection_get()
                            seçilen_yazı=str(seçilen)+" Ürünün Yeni Fiyatı"

                            yeni_ad=Label(değiştirme, text=seçilen_yazı)
                            yeni_ad.grid(row=0, column=0)

                            ad=Entry(değiştirme)
                            ad.grid(row=0, column=1)

                            cr.execute("select fiyat from ürünler where ürün_adi=(?)", (seçilen,))
                            sayı=cr.fetchall()
                            yazı="Mevcut Fiyat: "+str(sayı[0][0])
                            ürün_sayısı=Label(değiştirme, text=yazı)
                            ürün_sayısı.grid(row=1, column=0)

                            def kaydet():
                                adi=ad.get()

                                cr.execute("update ürünler set fiyat=(?) where fiyat=(select fiyat from ürünler where ürün_adi=(?))",(adi,seçilen))
                                vt.commit()

                                cr.execute("update ürünler set durum=\"Pahalı\" where (fiyat>(select AVG(fiyat) from ürünler))")
                                vt.commit()

                                cr.execute("update ürünler set durum=\"Ucuz\" where (fiyat<(select AVG(fiyat) from ürünler))")
                                vt.commit()

                                command=değiştirme.destroy()
                                command=ürün_seçenek.destroy()
                                command=ürün_güncelle.destroy()

                                messagebox.showinfo("Güncelleme", "Ürün Güncellendi")

                            kaydet=Button(değiştirme, text="Kaydet", width=13, command=kaydet)
                            kaydet.grid(row=2, column=1)

                        ad_değiştir=Button(ürün_seçenek, text="Adını Düzenle", width=15, command=değiştir_ad)
                        ad_değiştir.grid(row=0, column=0)

                        adet_değiştir=Button(ürün_seçenek, text="Adetini Düzenle", width=15, command=değiştir_adet)
                        adet_değiştir.grid(row=0, column=1)

                        fiyat_değiştir=Button(ürün_seçenek, text="Fiyatını Düzenle", width=15, command=değiştir_fiyat)
                        fiyat_değiştir.grid(row=0, column=2)

                        boşluk=Label(ürün_seçenek)
                        boşluk.grid(rowspan=1)

                        geri=Button(ürün_seçenek, text="Geri", width=14, command=ürün_seçenek.destroy)
                        geri.grid(row=2, column=1)


                    geri=Button(ürün_güncelle, text="Geri", width=8, command=ürün_güncelle.destroy)
                    geri.grid(row=1, column=0)

                    değiştir=Button(ürün_güncelle, text="Güncelle", width=10, command=güncelleme)
                    değiştir.grid(row=1, column=1)

                def ürün_listele():
                    ürün_listeleme=Toplevel()
                    başlık=ürün_listeleme.title("Ürün Listele")
                    ürün_listeleme.resizable(width=FALSE, height=FALSE)

                    Ürün_adi=Label(ürün_listeleme, text="Ürün Adı", width=7, font="Times 12 underline")
                    Adeti=Label(ürün_listeleme, text="Stok", width=7, font="Times 12 underline")
                    Fiyati=Label(ürün_listeleme, text="Fiyat", width=7, font="Times 12 underline")
                    Durumu=Label(ürün_listeleme, text="Durum", width=7, font="Times 12 underline")

                    Ürün_adi.grid(row=1, column=0)
                    Adeti.grid(row=1, column=1)
                    Fiyati.grid(row=1, column=2)
                    Durumu.grid(row=1, column=3)
                    x=2
                    cr.execute("select * from ürünler")
                    yazdir=cr.fetchall()
                    for yaz in yazdir:
                        Ürün_ad=Label(ürün_listeleme, text=yaz[0], width=7)
                        Adet=Label(ürün_listeleme, text=yaz[1], width=7)
                        Fiyat=Label(ürün_listeleme, text=yaz[2], width=7)
                        Durum=Label(ürün_listeleme, text=yaz[3], width=7)

                        Ürün_ad.grid(row=x, column=0)
                        Adet.grid(row=x, column=1)
                        Fiyat.grid(row=x, column=2)
                        Durum.grid(row=x, column=3)
                        x=x+1

                    geri=Button(ürün_listeleme,text="Geri", width=12, command=ürün_listeleme.destroy)
                    geri.grid(columnspan=5)

                ürün=Button(ekran1, text="Ürün Ekle", width=9, font="Times 11", command=ekle)
                ürün.grid(row=0, column=0)

                sil=Button(ekran1, text="Ürün Sil", width=9, font="Times 11", command=silme)
                sil.grid(row=0, column=1)

                ürün_güncelle=Button(ekran1, text="Güncelle", width=9, font="Times 11", command=güncelle)
                ürün_güncelle.grid(row=0, column=2)

                boşluk=Label(ekran1)
                boşluk.grid(rowspan=1)

                önizle=Button(ekran1, text="Önizle", width=9, font="Times 11 underline", command=ürün_listele)
                önizle.grid(row=2, column=0)

                kapat=Button(ekran1, text="Kapat", width=8, font="Times 11 bold", command=ekran1.quit)
                kapat.grid(row=2, column=2)


            elif(yaz[0]==ad and yaz[3]==şfre):
                hata_gösterme=1
                pencere.destroy()

                ekran=Tk()
                ekran.geometry("328x75+500+250")
                ekran.resizable(width=FALSE, height=FALSE)
                başlık=ekran.title("Proje Ödevi")

                yazı="Hoşgeldiniz Sayın "+str(yaz[1])+" "+str(yaz[2])
                mesaj=Label(ekran, text=yazı)
                mesaj.grid(columnspan=3)

                def ürün_satın_al():
                    liste_pencere=Toplevel()
                    liste_pencere.geometry("185x200+560+200")
                    başlık=liste_pencere.title("Satın Al")
                    liste_pencere.resizable(width=FALSE, height=FALSE)

                    liste=Listbox(liste_pencere)
                    liste.grid(columnspan=2)

                    cr.execute("select ürün_adi from ürünler")
                    yazdır=cr.fetchall()
                    for yaz in yazdır:
                        liste.insert(END, yaz[0])

                    def sec():
                        satın_al=Toplevel()
                        satın_al.geometry("270x80+530+250")
                        secilen=liste.selection_get()
                        başlık=satın_al.title(secilen)
                        satın_al.resizable(width=FALSE, height=FALSE)

                        cr.execute("select adet, fiyat from ürünler where ürün_adi=(?)",(secilen,))
                        yazdır=cr.fetchall()
                        for yaz in yazdır:
                            adet_gösterge=Label(satın_al,text="Adet: ")
                            adet_gösterge.grid(row=0, column=0)

                            adet_girdi=Entry(satın_al)
                            adet_girdi.grid(row=0, column=1)

                            yazı="/ "+str(yaz[0])+" Tane"
                            gösterge=Label(satın_al, text=yazı)
                            gösterge.grid(row=0, column=3)

                            yazı2="Tanesi: "+str(yaz[1])+" TL"
                            gösterge2=Label(satın_al, text=yazı2)
                            gösterge2.grid(columnspan=3)

                            def al():
                                adet_sayı=adet_girdi.get()
                                if(int(adet_sayı)>int(yaz[0])):
                                    command=satın_al.destroy()
                                    command=liste_pencere.destroy()
                                    hata_yazısı="Elimizde "+str(adet_sayı)+" Tane "+str(secilen)+" bulunmamaktatır"
                                    messagebox.showerror("Hata",hata_yazısı)

                                else:
                                    cr.execute("update ürünler set adet=adet-(?) where ürün_adi=(?)", (adet_sayı,secilen))
                                    vt.commit()

                                    cr.execute("select adet from ürünler")
                                    sayı=cr.fetchall()

                                    command=satın_al.destroy()
                                    command=liste_pencere.destroy()
                                    alıntı_yazı=str(adet_sayı)+" Tane "+str(secilen)+" Aldınız"
                                    messagebox.showinfo("Tebrikler", alıntı_yazı)

                                    cr.execute("select adet from ürünler where ürün_adi=(?)",(secilen,))
                                    yazdır=cr.fetchall()
                                    if(yazdır[0][0]==0):
                                        cr.execute("delete from ürünler where ürün_adi=(?)", (secilen,))
                                        vt.commit()

                            ürün_al=Button(satın_al, text="Satın Al", width=12, command=al)
                            ürün_al.grid(row=3, column=1)

                            geri=Button(satın_al, text="Geri", width=10, command=satın_al.destroy)
                            geri.grid(row=3, column=0)

                    geri=Button(liste_pencere,text="Geri", width=12, command=liste_pencere.destroy)
                    geri.grid(row=1, column=0)

                    sec=Button(liste_pencere, text="Seç", width=10, command=sec)
                    sec.grid(row=1, column=1)

                def ürün_listele():
                    ürün_listeleme=Toplevel()
                    başlık=ürün_listeleme.title("Ürün Listele")
                    ürün_listeleme.resizable(width=FALSE, height=FALSE)
                    Ürün_adi=Label(ürün_listeleme, text="Ürün Adı", width=7, font="Times 12 underline")
                    Adeti=Label(ürün_listeleme, text="Stok", width=7, font="Times 12 underline")
                    Fiyati=Label(ürün_listeleme, text="Fiyat", width=7, font="Times 12 underline")
                    Durumu=Label(ürün_listeleme, text="Durum", width=7, font="Times 12 underline")

                    Ürün_adi.grid(row=1, column=0)
                    Adeti.grid(row=1, column=1)
                    Fiyati.grid(row=1, column=2)
                    Durumu.grid(row=1, column=3)
                    x=2
                    cr.execute("select * from ürünler")
                    yazdir=cr.fetchall()
                    for yaz in yazdir:
                        Ürün_ad=Label(ürün_listeleme, text=yaz[0], width=7)
                        Adet=Label(ürün_listeleme, text=yaz[1], width=7)
                        Fiyat=Label(ürün_listeleme, text=yaz[2], width=7)
                        Durum=Label(ürün_listeleme, text=yaz[3], width=7)

                        Ürün_ad.grid(row=x, column=0)
                        Adet.grid(row=x, column=1)
                        Fiyat.grid(row=x, column=2)
                        Durum.grid(row=x, column=3)
                        x=x+1

                    geri=Button(ürün_listeleme,text="Geri", width=12, command=ürün_listeleme.destroy)
                    geri.grid(columnspan=5)

                ürün_listesi=Button(ekran, text="Ürün Listesi", width=22, command=ürün_listele)
                ürün_listesi.grid(row=1, column=0)

                ürün_satın_al=Button(ekran, text="Ürün Satın Al", command=ürün_satın_al, width=22)
                ürün_satın_al.grid(row=1, column=1)

                kapat=Button(ekran, text="Kapat", width=17, command=ekran.quit)
                kapat.grid(columnspan=3)

        if(hata_gösterme==0):
            pencere2.destroy()
            messagebox.showerror("Hata", "Kullanıcı Adı veya Şifre Yanlış")

    def kayıd():
        pencere3=Toplevel()
        pencere3.geometry("235x125+545+235")
        başlık=pencere3.title("Kayıt")

        kullanıcı_adi=Label(pencere3,text="Kullanıcı Adı")
        kullanıcı_adi.grid(row=0, column=0)

        girdi_kullanıcı_adi=Entry(pencere3)
        girdi_kullanıcı_adi.grid(row=0, column=1)

        adi=Label(pencere3,text="Ad")
        adi.grid(row=1, column=0)

        girdi_adi=Entry(pencere3)
        girdi_adi.grid(row=1, column=1)

        soyadi=Label(pencere3,text="Soyad")
        soyadi.grid(row=2, column=0)

        girdi_soyadi=Entry(pencere3)
        girdi_soyadi.grid(row=2, column=1)

        şifre_yazı=Label(pencere3,text="Şifre")
        şifre_yazı.grid(row=3, column=0)

        şifre=Entry(pencere3)
        şifre.grid(row=3, column=1)

        def kaydet():
            nick=girdi_kullanıcı_adi.get()
            ad=girdi_adi.get()
            soyad=girdi_soyadi.get()
            şfre=şifre.get()
            hata_gösterme=0

            cr.execute("SELECT kullanici_adi FROM üyeler")
            vt.commit()
            yazdir=cr.fetchall()
            for yaz in yazdir:
                if(nick==yaz[0]):
                    hata_gösterme=1

            if(hata_gösterme==0):
                cr.execute("insert into üyeler (kullanici_adi, adi, soyadi, sifre) values (?,?,?,?)",(nick, ad, soyad, şfre))
                vt.commit()
                command=pencere2.destroy()
                command=pencere3.destroy()
                if(hata_gösterme==0):
                    messagebox.showinfo("Kayıt","Kaydedildi.")

            elif(hata_gösterme==1):
                command=pencere2.destroy()
                command=pencere3.destroy()
                messagebox.showerror("Hata","Bu Kullanıcı Adi Kullanılmaktadır.")

        geri=Button(pencere3,text="Geri", width=12, command=pencere3.destroy)
        geri.grid(row=4, column=0)

        kaydet=Button(pencere3, text="Kaydet", width=15, command=kaydet)
        kaydet.grid(row=4, column=1)

    def unuttum():
        pencere3=Toplevel()
        pencere3.geometry("225x65+545+265")
        başlık=pencere3.title("Unuttum")

        kullanıcı_adi=Label(pencere3,text="Kullanıcı Adı")
        kullanıcı_adi.grid(row=0, column=0)

        girdi_kullanıcı_adi=Entry(pencere3)
        girdi_kullanıcı_adi.grid(row=0, column=1)

        def göster():
            adi=girdi_kullanıcı_adi.get()
            hatayı_gösterme=0
            cr.execute("SELECT sifre FROM üyeler where kullanici_adi=(?)", (adi,))
            yazdir=cr.fetchall()
            for yaz in yazdir:
                command=pencere2.destroy()
                command=pencere3.destroy()
                if(yaz[0]!="123456"):
                    messagebox.showinfo("Şifreniz",yaz)
                    hatayı_gösterme=1
                else:
                    hatayı_gösterme=2

            if(hatayı_gösterme==2):
                messagebox.showerror("Hata","Bu Kullanıcının Şifresini Göremezsiniz.")
                hatayı_gösterme=1

            elif(hatayı_gösterme==0):
                command=pencere2.destroy()
                command=pencere3.destroy()
                messagebox.showerror("Hata","Kullanıcı Bulunamadı")

        geri=Button(pencere3,text="Geri", width=12, command=pencere3.destroy)
        geri.grid(row=1, column=0)

        göster=Button(pencere3,text="Gönder", width=15, command=göster)
        göster.grid(row=1, column=1)

    giriş=Button(pencere2, text="Giriş", width=22, command=giriş)
    giriş.grid(columnspan=2)

    unuttum=Button(pencere2, text="Şifremi Unuttum", width=15, command=unuttum)
    unuttum.grid(row=3, column=1)

    kayıt_ol=Button(pencere2, text="Kayıt Ol", width=15, command=kayıd)
    kayıt_ol.grid(row=3, column=0)

pencere = Tk()
pencere.geometry("335x75+500+250")
#pencere.tk_setPalette("dark blue") #renk ayarı buradan oluyor----------------------------------------------------------
pencere.resizable(width=FALSE, height=FALSE)
başlık=pencere.title("Proje Ödevi")

ürün_listesi=Button(pencere, text="Ürün Listesi", width=25, command=ürün_listesi)
ürün_listesi.grid(row=0, column=0)

üye_girişi=Button(pencere, text="Giriş Yap", width=20, command=üye_girişi)
üye_girişi.grid(row=0, column=1)

uyarı=Label(pencere, text="Ürün Satın Almak İçin Giriş Yapın", font="Times 11 bold")
uyarı.grid(columnspan=2)

mainloop()