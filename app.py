import streamlit as st
from supabase import create_client, Client
import os
from datetime import datetime
import base64
import pandas as pd

st.set_page_config(page_title="Stok & Takip Sistemi", page_icon="", layout="wide")

# --- KULLANICI GİRİŞ KONTROLÜ ---
def check_password():
    def password_entered():
        if (
            st.session_state.get("username", "") == "Sedat-Burak"
            and st.session_state.get("password", "") == "Zeus5341"
        ):
            st.session_state["password_correct"] = True
            if "password" in st.session_state: del st.session_state["password"]  
            if "username" in st.session_state: del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state or not st.session_state["password_correct"]:
        # Giriş Ekranı Görseli ve Tasarımı
        col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
        with col_l2:
            st.markdown("<h2 style='text-align: center;'>Stok & Takip Sistemi Girişi</h2>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: gray;'>Lütfen kullanıcı adı ve şifrenizle giriş yapın.</p>", unsafe_allow_html=True)
            
            # Giriş ekranı için şık bir görsel (varsa gösterilir, yoksa şık bir ikon/banner alanı)
            st.markdown("""
                <div style='display: flex; justify-content: center; margin-bottom: 20px;'>
                    <div style='background: linear-gradient(135deg, #00b09b, #96c93d); padding: 20px; border-radius: 50px; width: 80px; height: 80px; display: flex; align-items: center; justify-content: center; color: white; font-size: 32px; font-weight: bold; box-shadow: 0 10px 20px rgba(0,0,0,0.2);'>
                        📦
                    </div>
                </div>
            """, unsafe_allow_html=True)

            st.text_input("Kullanıcı Adı", key="username")
            st.text_input("Şifre", type="password", key="password")
            st.checkbox("Beni Hatırla", key="beni_hatirla")
            
            if st.button("Giriş Yap", use_container_width=True, type="primary"):
                password_entered()
                st.rerun()

            if "password_correct" in st.session_state and not st.session_state["password_correct"]:
                st.error("Kullanıcı adı veya şifre yanlış.")
        return False
    else:
        return True

if check_password():
    
    @st.cache_resource
    def init_supabase():
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)

    supabase = init_supabase()

    st.markdown("""
        <style>
        div[data-testid="stDataEditor"] div.dvn-scroller, div[data-testid="stDataFrame"] div.dvn-scroller {
            max-width: 100%;
        }
        table {
            width: 100% !important;
            border-collapse: collapse !important;
        }
        th {
            font-size: 15px !important;
            padding: 16px 18px !important;
            background-color: rgba(150, 150, 150, 0.15) !important;
            text-align: left !important;
        }
        td {
            font-size: 15px !important;
            padding: 22px 18px !important;
            vertical-align: middle !important;
            height: 85px !important;
        }
        .zoom-img {
            width: 60px;
            height: 60px;
            object-fit: cover;
            border-radius: 8px;
            transition: transform 0.3s cubic-bezier(0.2, 0.8, 0.2, 1);
            cursor: pointer;
            display: block;
        }
        .zoom-img:hover {
            transform: scale(5) translateX(25px);
            z-index: 99999;
            position: relative;
            box-shadow: 0 20px 40px rgba(0,0,0,0.5);
        }
        
        section[data-testid="stSidebar"] div.stButton > button {
            width: 100%;
            text-align: left;
            margin-bottom: 3px;
            border-radius: 8px;
            border: 1px solid rgba(255,255,255,0.1);
            font-weight: 600;
            padding: 7px 12px;
            font-size: 13.5px;
        }
        
        div[data-testid="column"] div.stButton > button {
            width: 100% !important;
            height: 120px !important;
            font-size: 19px !important;
            font-weight: 700 !important;
            border-radius: 16px !important;
            border: none !important;
            box-shadow: 0 6px 18px rgba(0,0,0,0.35) !important;
            color: white !important;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        div[data-testid="column"] div.stButton > button:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.5) !important;
        }
        
        div[data-testid="column"]:nth-of-type(1) div[data-testid="stButton"]:nth-of-type(1) button { background: linear-gradient(135deg, #00b09b, #96c93d) !important; }
        div[data-testid="column"]:nth-of-type(1) div[data-testid="stButton"]:nth-of-type(2) button { background: linear-gradient(135deg, #11998e, #38ef7d) !important; }
        div[data-testid="column"]:nth-of-type(1) div[data-testid="stButton"]:nth-of-type(3) button { background: linear-gradient(135deg, #f2994a, #f2c94c) !important; }
        div[data-testid="column"]:nth-of-type(1) div[data-testid="stButton"]:nth-of-type(4) button { background: linear-gradient(135deg, #8e2de2, #4a00e0) !important; }
        div[data-testid="column"]:nth-of-type(1) div[data-testid="stButton"]:nth-of-type(5) button { background: linear-gradient(135deg, #0ba360, #3cba92) !important; }
    
        div[data-testid="column"]:nth-of-type(2) div[data-testid="stButton"]:nth-of-type(1) button { background: linear-gradient(135deg, #2193b0, #6dd5ed) !important; }
        div[data-testid="column"]:nth-of-type(2) div[data-testid="stButton"]:nth-of-type(2) button { background: linear-gradient(135deg, #eb3349, #f45c43) !important; }
        div[data-testid="column"]:nth-of-type(2) div[data-testid="stButton"]:nth-of-type(3) button { background: linear-gradient(135deg, #56ab2f, #a8e063) !important; }
        div[data-testid="column"]:nth-of-type(2) div[data-testid="stButton"]:nth-of-type(4) button { background: linear-gradient(135deg, #4ca1af, #c4e0e5) !important; color: #1e293b !important; }
        div[data-testid="column"]:nth-of-type(2) div[data-testid="stButton"]:nth-of-type(5) button { background: linear-gradient(135deg, #512b58, #8f43ee) !important; }
        </style>
    """, unsafe_allow_html=True)
    
    def para_formatla(miktar):
        try:
            val = float(miktar)
            return f"{val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") + " TL"
        except:
            return "0,00 TL"
    
    def para_metin_to_float(metin):
        if not metin or str(metin).lower() == "none":
            return 0.0
        s = str(metin).replace(" TL", "").replace("TL", "").strip()
        if "," in s and "." in s:
            s = s.replace(".", "").replace(",", ".")
        elif "," in s:
            s = s.replace(",", ".")
        try:
            return float(s)
        except:
            return 0.0
    
    def image_to_base64(image_path):
        if image_path and os.path.exists(image_path):
            with open(image_path, "rb") as image_file:
                encoded = base64.b64encode(image_file.read()).decode()
                return f"data:image/jpeg;base64,{encoded}"
        return ""
    
    def veritabani_kontrol():
        res = supabase.table("tanimlar").select("*").eq("tip", "satilan_yer").execute()
        if not res.data:
            for yer in ["Hepsi Burada", "Web Sitesi", "Dükkan & Elden"]:
                supabase.table("tanimlar").insert({"tip": "satilan_yer", "deger": yer}).execute()
    
    veritabani_kontrol()
    
    menu_listesi = [
        " 0. Ana Panel", " 1. Ürün Girişi", " 2. Satış İşlemleri", 
        " 3. Güncel Stok", " 4. Hepsi Burada", " 5. Web Sitesi",
        " 6. Dükkan & Elden", " 7. Müşteri Analizi", " 8. Tanımlamalar",
        " 9. Raporlar ve Özet", " 10. Aylık Detaylı Raporlar"
    ]
    
    if "aktif_menu" not in st.session_state:
        st.session_state.aktif_menu = menu_listesi[0]
    
    st.sidebar.title(" Menüler")
    
    for m in menu_listesi:
        if st.sidebar.button(m, key=f"btn_{m}", type="primary" if st.session_state.aktif_menu == m else "secondary"):
            st.session_state.aktif_menu = m
            st.rerun()
    
    menu = st.session_state.aktif_menu
    
    # --- 0. ANA PANEL (DASHBOARD) ---
    if menu == " 0. Ana Panel":
        st.title(" Ana Panel - Hızlı Erişim")
        st.write("Sisteme hoş geldiniz! İstediğiniz bölüme geçmek için aşağıdaki renkli ve büyük butonlara tıklayabilirsiniz.")
        st.divider()
    
        col_a, col_b = st.columns(2)
    
        with col_a:
            if st.button(" 1. Ürün Girişi\n\n Yeni Mal Kabul", use_container_width=True, key="card_1"):
                st.session_state.aktif_menu = " 1. Ürün Girişi"
                st.rerun()
            
            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
            if st.button(" 3. Güncel Stok\n\n Kalan Ürünler", use_container_width=True, key="card_3"):
                st.session_state.aktif_menu = " 3. Güncel Stok"
                st.rerun()
    
            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
            if st.button(" 5. Web Sitesi\n\n E-Ticaret Satışları", use_container_width=True, key="card_5"):
                st.session_state.aktif_menu = " 5. Web Sitesi"
                st.rerun()
    
            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
            if st.button(" 7. Müşteri Analizi\n\n Müşteri Liderlik", use_container_width=True, key="card_7"):
                st.session_state.aktif_menu = " 7. Müşteri Analizi"
                st.rerun()
    
            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
            if st.button(" 9. Raporlar ve Özet\n\n Detaylı Finansal Özet", use_container_width=True, key="card_9"):
                st.session_state.aktif_menu = " 9. Raporlar ve Özet"
                st.rerun()
    
        with col_b:
            if st.button(" 2. Satış İşlemleri\n\n FIFO & Satış", use_container_width=True, key="card_2"):
                st.session_state.aktif_menu = " 2. Satış İşlemleri"
                st.rerun()
    
            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
            if st.button(" 4. Hepsi Burada\n\n Pazaryeri Yönetimi", use_container_width=True, key="card_4"):
                st.session_state.aktif_menu = " 4. Hepsi Burada"
                st.rerun()
    
            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
            if st.button(" 6. Dükkan & Elden\n\n Mağaza Satışları", use_container_width=True, key="card_6"):
                st.session_state.aktif_menu = " 6. Dükkan & Elden"
                st.rerun()
    
            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
            if st.button(" 8. Tanımlamalar\n\n Kategori & Kanallar", use_container_width=True, key="card_8"):
                st.session_state.aktif_menu = " 8. Tanımlamalar"
                st.rerun()
    
            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
            if st.button(" 10. Aylık Detaylı Raporlar\n\n Tarih Aralığı Döküm", use_container_width=True, key="card_10"):
                st.session_state.aktif_menu = " 10. Aylık Detaylı Raporlar"
                st.rerun()
    
    # --- 1. ÜRÜN GİRİŞİ ---
    elif menu == " 1. Ürün Girişi":
        st.header(" Ürün Girişi")
        if "giris_barkod" not in st.session_state: st.session_state.giris_barkod = ""
        if "giris_kod" not in st.session_state: st.session_state.giris_kod = ""
        if "giris_ad" not in st.session_state: st.session_state.giris_ad = ""
        if "giris_kat" not in st.session_state: st.session_state.giris_kat = ""
        if "giris_resim" not in st.session_state: st.session_state.giris_resim = ""
        if "duzenlenen_kod" not in st.session_state: st.session_state.duzenlenen_kod = None
    
        kat_res = supabase.table("tanimlar").select("deger").eq("tip", "kategori_marka").order("deger", desc=False).execute()
        kategori_marka_listesi = [row["deger"] for row in kat_res.data] if kat_res.data else []
        
        yer_res = supabase.table("tanimlar").select("deger").eq("tip", "alinan_yer").order("deger", desc=False).execute()
        alinan_yer_listesi = [row["deger"] for row in yer_res.data] if yer_res.data else []
        
        if not kategori_marka_listesi: kategori_marka_listesi = ["Önce Tanımlamalardan Ekle"]
        if not alinan_yer_listesi: alinan_yer_listesi = ["Önce Tanımlamalardan Ekle"]
    
        def urun_giris_barkod_degisti():
            b_val = st.session_state.get("input_giris_barkod", "").strip()
            st.session_state.giris_barkod = b_val
            if b_val:
                bul_res = supabase.table("stok").select("urun_kodu, urun_adi, kategori_marka, resim_yolu").eq("barkod", b_val).order("id", desc=True).limit(1).execute()
                if bul_res.data:
                    bulunan = bul_res.data[0]
                    st.session_state.giris_kod = bulunan.get("urun_kodu") or ""
                    st.session_state.giris_ad = bulunan.get("urun_adi") or ""
                    st.session_state.giris_kat = bulunan.get("kategori_marka") or ""
                    st.session_state.giris_resim = bulunan.get("resim_yolu") or ""
    
        def urun_giris_kod_degisti():
            k_val = st.session_state.get("input_giris_kod", "").strip()
            st.session_state.giris_kod = k_val
            if k_val:
                bul_res = supabase.table("stok").select("barkod, urun_adi, kategori_marka, resim_yolu").eq("urun_kodu", k_val).order("id", desc=True).limit(1).execute()
                if bul_res.data:
                    bulunan = bul_res.data[0]
                    st.session_state.giris_barkod = bulunan.get("barkod") or ""
                    st.session_state.giris_ad = bulunan.get("urun_adi") or ""
                    st.session_state.giris_kat = bulunan.get("kategori_marka") or ""
                    st.session_state.giris_resim = bulunan.get("resim_yolu") or ""
    
        if st.session_state.duzenlenen_kod:
            st.info(f" Şu an Ürün Kodu: **{st.session_state.duzenlenen_kod}** olan ürün güncelleniyor modunda.")
            if st.button(" Düzenlemeyi İptal Et"):
                st.session_state.duzenlenen_kod = None
                st.session_state.giris_barkod = ""
                st.session_state.giris_kod = ""
                st.session_state.giris_ad = ""
                st.session_state.giris_kat = ""
                st.session_state.giris_resim = ""
                st.rerun()
    
        col_k1, col_k2 = st.columns(2)
        with col_k1:
            st.text_input("Ürün Barkodu * (Barkod Okuyucu Uyumlu)", key="input_giris_barkod", on_change=urun_giris_barkod_degisti, value=st.session_state.giris_barkod)
        with col_k2:
            st.text_input("Ürün Kodu *", key="input_giris_kod", on_change=urun_giris_kod_degisti, value=st.session_state.giris_kod)
    
        col1, col2 = st.columns(2)
        with col1:
            tarih = st.text_input("Ürün Giriş Tarihi (GG.AA.YYYY) *", value=datetime.now().strftime("%d.%m.%Y"), key="giris_tarih")
            kat_secim_Index = 0
            if st.session_state.giris_kat in kategori_marka_listesi:
                kat_secim_Index = kategori_marka_listesi.index(st.session_state.giris_kat)
            secilen_kat_marka = st.selectbox("Kategori & Marka Seçimi *", kategori_marka_listesi, index=kat_secim_Index, key="giris_kategori")
            secilen_alinan_yer = st.selectbox("Ürünün Alındığı Yer / Tedarikçi *", alinan_yer_listesi, key="giris_alinan_yer")
            adet = st.number_input("Ürün Adeti *", min_value=1, value=1, key="giris_adet")
        with col2:
            ham_urun_adi = st.text_input("Ürün Adı *", value=st.session_state.giris_ad, key="giris_urun_adi")
            birim_fiyat = st.number_input("Birim Fiyatı (TL) *", min_value=0.0, format="%.2f", key="giris_birim_fiyat")
            st.caption(f" Girilen Birim Fiyat: **{para_formatla(birim_fiyat)}**")
            kdv_durumu = st.selectbox("KDV Durumu *", ["KDV'li", "KDV'siz"], key="giris_kdv")
            
        if st.session_state.giris_resim and os.path.exists(st.session_state.giris_resim):
            st.image(st.session_state.giris_resim, width=100, caption="Kayıtlı Ürün Görseli")
            
        resim_dosyasi = st.file_uploader("Ürün Görseli Yükle (Opsiyonel)", type=["png", "jpg", "jpeg"], key="giris_resim_yukle")
        
        buton_metni = " Ürünü Güncelle" if st.session_state.duzenlenen_kod else " Hesapla ve Listeye Ekle"
        if st.button(buton_metni, type="primary"):
            urun_adi = ham_urun_adi.strip().title()
            g_barkod = st.session_state.get("input_giris_barkod", "").strip()
            g_kod = st.session_state.get("input_giris_kod", "").strip()
            
            if not tarih or not g_barkod or not g_kod or not urun_adi or birim_fiyat <= 0:
                st.error(" Eksik alanlar var!")
            else:
                kdvli_birim = birim_fiyat * 1.20 if kdv_durumu == "KDV'siz" else birim_fiyat
                toplam_maliyet = kdvli_birim * adet
                resim_yolu = st.session_state.giris_resim
                if resim_dosyasi:
                    os.makedirs("uploads", exist_ok=True)
                    resim_yolu = os.path.join("uploads", resim_dosyasi.name)
                    with open(resim_yolu, "wb") as f: f.write(resim_dosyasi.getbuffer())
                
                veri_dict = {
                    "tarih": tarih,
                    "urun_kodu": g_kod,
                    "urun_adi": urun_adi,
                    "adet": int(adet),
                    "alinan_yer": secilen_alinan_yer,
                    "toplam_maliyet": para_formatla(toplam_maliyet),
                    "resim_yolu": resim_yolu,
                    "kategori_marka": secilen_kat_marka,
                    "barkod": g_barkod
                }

                if st.session_state.duzenlenen_kod:
                    supabase.table("stok").update(veri_dict).eq("urun_kodu", st.session_state.duzenlenen_kod).execute()
                    st.session_state.duzenlenen_kod = None
                    basari_mesaji = " Ürün başarıyla güncellendi!"
                else:
                    supabase.table("stok").insert(veri_dict).execute()
                    basari_mesaji = " Ürün başarıyla eklendi!"
                    
                st.success(basari_mesaji)
                st.session_state.giris_barkod = ""
                st.session_state.giris_kod = ""
                st.session_state.giris_ad = ""
                st.session_state.giris_kat = ""
                st.session_state.giris_resim = ""
                st.rerun()
    
        st.divider()
        st.subheader(" Düzenlenecek veya Silinecek Ürünü Arayın")
        arama_metni = st.text_input("Aramak İstediğiniz Ürün Kodunu veya Barkodunu Yazın:", placeholder="Örn: KOD123 veya Barkod...", key="urun_giris_arama_input").strip()
    
        secilen_islem_kod = None
        if arama_metni:
            bulunan_sonuclar = []
            q_res = supabase.table("stok").select("urun_kodu, barkod, id").or_(f"urun_kodu.ilike.%{arama_metni}%,barkod.ilike.%{arama_metni}%,urun_adi.ilike.%{arama_metni}%").order("id", desc=True).limit(15).execute()
            if q_res.data:
                gorulen_kodlar = set()
                for r in q_res.data:
                    kodu = r.get("urun_kodu")
                    if kodu and kodu not in gorulen_kodlar:
                        gorulen_kodlar.add(kodu)
                        detay_res = supabase.table("stok").select("urun_kodu, barkod, urun_adi").eq("urun_kodu", kodu).limit(1).execute()
                        if detay_res.data:
                            bulunan_sonuclar.append(detay_res.data[0])

            if bulunan_sonuclar:
                secenekler_dict = {f"{r['urun_kodu']} | Barkod: {r.get('barkod') or '-'} | {r['urun_adi']}": r['urun_kodu'] for r in bulunan_sonuclar}
                secilen_etiket = st.selectbox("Eşleşen Ürünler Arasından Seçin:", list(secenekler_dict.keys()), key="bulunan_urunler_box")
                secilen_islem_kod = secenekler_dict[secilen_etiket]
            else:
                st.warning(" Aradığınız kriterlere uygun ürün bulunamadı.")
        else:
            st.info(" Ürün düzenlemek veya silmek için arama kutusuna kod veya barkod yazın.")
    
        if secilen_islem_kod:
            islem_col1, islem_col2 = st.columns(2)
            with islem_col1:
                if st.button(" Seçileni Düzenle", use_container_width=True):
                    kayit_res = supabase.table("stok").select("barkod, urun_kodu, urun_adi, kategori_marka, resim_yolu").eq("urun_kodu", secilen_islem_kod).order("id", desc=True).limit(1).execute()
                    if kayit_res.data:
                        secilen_kayit = kayit_res.data[0]
                        st.session_state.duzenlenen_kod = secilen_islem_kod
                        st.session_state.giris_barkod = secilen_kayit.get("barkod") or ""
                        st.session_state.giris_kod = secilen_kayit.get("urun_kodu") or ""
                        st.session_state.giris_ad = secilen_kayit.get("urun_adi") or ""
                        st.session_state.giris_kat = secilen_kayit.get("kategori_marka") or ""
                        st.session_state.giris_resim = secilen_kayit.get("resim_yolu") or ""
                        st.rerun()
            with islem_col2:
                if st.button(" Seçileni Sil", type="primary", use_container_width=True):
                    supabase.table("stok").delete().eq("urun_kodu", secilen_islem_kod).execute()
                    st.success(f" Ürün Kodu: {secilen_islem_kod} olan ürün(ler) silindi!")
                    st.rerun()
    
        st.divider()
        st.subheader(" Kayıtlı Ürünler Listesi ve Tarih Filtresi")
        
        stok_Tum_res = supabase.table("stok").select("tarih").execute()
        tum_stk_tarihler = []
        if stok_Tum_res.data:
            for r in stok_Tum_res.data:
                dt_parse = pd.to_datetime(r.get("tarih"), format="%d.%m.%Y", errors='coerce')
                if pd.notnull(dt_parse): tum_stk_tarihler.append(dt_parse.date())
        
        if tum_stk_tarihler:
            min_stk_t = min(tum_stk_tarihler)
            max_stk_t = max(tum_stk_tarihler)
            col_tf1, col_tf2 = st.columns(2)
            with col_tf1: giris_bas_tarih = st.date_input("Ürün Giriş Başlangıç Tarihi", value=min_stk_t, min_value=min_stk_t, max_value=max_stk_t, key="giris_bas_tarih_filtre")
            with col_tf2: giris_bit_tarih = st.date_input("Ürün Giriş Bitiş Tarihi", value=max_stk_t, min_value=min_stk_t, max_value=max_stk_t, key="giris_bit_tarih_filtre")
        else:
            giris_bas_tarih, giris_bit_tarih = None, None

        sira_col1, sira_col2 = st.columns(2)
        with sira_col1:
            siralama_kriteri = st.selectbox(
                " Sıralama Kriteri Seçin:",
                ["Ekleme Sırası (ID)", "Tarih", "Ürün Kodu", "Barkod", "Ürün Adı", "Adet", "Toplam Maliyet"],
                key="giris_siralama_kriteri"
            )
        with sira_col2:
            siralama_yonu = st.radio(
                " Sıralama Yönü:",
                ["Azalan / Yeniden Eskiye ", "Artan / Eskiden Yeniye "],
                horizontal=True,
                key="giris_siralama_yonu"
            )
    
        stok_res = supabase.table("stok").select("*").execute()
        tum_urunler = stok_res.data if stok_res.data else []
    
        if tum_urunler:
            tablo_verisi = []
            for r in tum_urunler:
                resim_html = ""
                r_yolu = r.get("resim_yolu")
                if r_yolu and os.path.exists(r_yolu):
                    b64_img = image_to_base64(r_yolu)
                    if b64_img: resim_html = f'<img src="{b64_img}" class="zoom-img">'
                
                maliyet_num = para_metin_to_float(r.get("toplam_maliyet"))
                tarih_str = str(r.get("tarih")).strip()
                tarih_dt = None
                try:
                    tarih_dt = datetime.strptime(tarih_str, "%d.%m.%Y")
                except: pass
    
                if giris_bas_tarih and giris_bit_tarih and tarih_dt:
                    if not (giris_bas_tarih <= tarih_dt.date() <= giris_bit_tarih):
                        continue

                tablo_verisi.append({
                    "ID": r.get("id"),
                    "Görsel": resim_html if resim_html else " Yok",
                    "Tarih": tarih_str,
                    "Tarih_dt": tarih_dt,
                    "Ürün Kodu": r.get("urun_kodu") or "-",
                    "Barkod": r.get("barkod") or "-",
                    "Ürün Adı": r.get("urun_adi"),
                    "Kategori": r.get("kategori_marka"),
                    "Alınan Yer": r.get("alinan_yer"),
                    "Adet": r.get("adet"),
                    "Toplam Maliyet": para_formatla(maliyet_num),
                    "Maliyet_Num": maliyet_num
                })
            
            if tablo_verisi:
                df_urunler = pd.DataFrame(tablo_verisi)
                ascending = True if "Artan" in siralama_yonu else False
        
                if siralama_kriteri == "Ekleme Sırası (ID)": df_urunler = df_urunler.sort_values(by="ID", ascending=ascending)
                elif siralama_kriteri == "Tarih": df_urunler = df_urunler.sort_values(by="Tarih_dt", ascending=ascending)
                elif siralama_kriteri == "Ürün Kodu": df_urunler = df_urunler.sort_values(by="Ürün Kodu", ascending=ascending)
                elif siralama_kriteri == "Barkod": df_urunler = df_urunler.sort_values(by="Barkod", ascending=ascending)
                elif siralama_kriteri == "Ürün Adı": df_urunler = df_urunler.sort_values(by="Ürün Adı", ascending=ascending)
                elif siralama_kriteri == "Adet": df_urunler = df_urunler.sort_values(by="Adet", ascending=ascending)
                elif siralama_kriteri == "Toplam Maliyet": df_urunler = df_urunler.sort_values(by="Maliyet_Num", ascending=ascending)
        
                gosterim_df = df_urunler[["Görsel", "Tarih", "Ürün Kodu", "Barkod", "Ürün Adı", "Kategori", "Alınan Yer", "Adet", "Toplam Maliyet"]]
                st.write(gosterim_df.to_html(escape=False, index=False), unsafe_allow_html=True)
            else:
                st.info("Seçilen tarih aralığında ürün giriş kaydı bulunamadı.")
        else:
            st.info(" Henüz eklenmiş ürün yok.")
    
    # --- 2. SATIŞ İŞLEMLERİ ---
    elif menu == " 2. Satış İşlemleri":
        st.header(" Satış İşlemleri")
        if "satis_duzenle_id" not in st.session_state: st.session_state.satis_duzenle_id = None
        if "satis_barkod" not in st.session_state: st.session_state.satis_barkod = ""
        if "satis_kod" not in st.session_state: st.session_state.satis_kod = ""
    
        kanal_res = supabase.table("tanimlar").select("deger").eq("tip", "satilan_yer").order("deger", desc=False).execute()
        satilan_yer_listesi = [row["deger"] for row in kanal_res.data] if kanal_res.data else []
        if not satilan_yer_listesi: satilan_yer_listesi = ["Önce Tanımlamalardan Ekle"]
    
        d_tarih = datetime.now().strftime("%d.%m.%Y")
        d_siparis = ""
        d_adet = 1
        d_fiyat = 0.0
        d_musteri = ""
        d_yer = satilan_yer_listesi[0] if satilan_yer_listesi else ""
        
        if st.session_state.satis_duzenle_id:
            s_res = supabase.table("satis").select("*").eq("id", st.session_state.satis_duzenle_id).execute()
            if s_res.data:
                s_kayit = s_res.data[0]
                d_tarih, d_siparis, d_barkod_kod_val, d_adet, f_str, d_musteri, d_yer = (
                    s_kayit.get("tarih"), s_kayit.get("siparis_no"), s_kayit.get("barkod_kod"), 
                    s_kayit.get("satis_adet"), s_kayit.get("birim_fiyat"), s_kayit.get("musteri"), s_kayit.get("satilan_yer")
                )
                if not st.session_state.satis_barkod and not st.session_state.satis_kod:
                    stk_bul_res = supabase.table("stok").select("barkod, urun_kodu").or_(f"barkod.eq.{d_barkod_kod_val},urun_kodu.eq.{d_barkod_kod_val}").limit(1).execute()
                    if stk_bul_res.data:
                        bul_b_k = stk_bul_res.data[0]
                        st.session_state.satis_barkod = bul_b_k.get("barkod") or ""
                        st.session_state.satis_kod = bul_b_k.get("urun_kodu") or ""
                    else:
                        st.session_state.satis_barkod = d_barkod_kod_val
                d_fiyat = para_metin_to_float(f_str)
    
        def satis_barkod_degisti():
            b_val = st.session_state.get("input_satis_barkod", "").strip()
            st.session_state.satis_barkod = b_val
            if b_val:
                bul_res = supabase.table("stok").select("urun_kodu").eq("barkod", b_val).order("id", desc=True).limit(1).execute()
                if bul_res.data and bul_res.data[0].get("urun_kodu"): 
                    st.session_state.satis_kod = bul_res.data[0].get("urun_kodu")
    
        def satis_kod_degisti():
            k_val = st.session_state.get("input_satis_kod", "").strip()
            st.session_state.satis_kod = k_val
            if k_val:
                bul_res = supabase.table("stok").select("barkod").eq("urun_kodu", k_val).order("id", desc=True).limit(1).execute()
                if bul_res.data and bul_res.data[0].get("barkod"): 
                    st.session_state.satis_barkod = bul_res.data[0].get("barkod")
    
        if st.session_state.satis_duzenle_id:
            st.info(f" Şu an Sipariş No: **{d_siparis}** olan satış güncelleniyor.")
            if st.button(" Satış Düzenlemeyi İptal Et"):
                st.session_state.satis_duzenle_id = None
                st.session_state.satis_barkod = ""
                st.session_state.satis_kod = ""
                st.rerun()
    
        col_s1, col_s2 = st.columns(2)
        with col_s1: st.text_input("Ürün Barkodu * (Barkod Okuyucu Uyumlu)", key="input_satis_barkod", on_change=satis_barkod_degisti, value=st.session_state.satis_barkod)
        with col_s2: st.text_input("Ürün Kodu *", key="input_satis_kod", on_change=satis_kod_degisti, value=st.session_state.satis_kod)
    
        col1, col2 = st.columns(2)
        with col1:
            s_tarih = st.text_input("Satış Tarihi (GG.AA.YYYY) *", value=d_tarih, key="satis_tarih")
            satis_adet = st.number_input("Satış Adeti *", min_value=1, value=int(d_adet), key="satis_adet")
            satis_fiyati = st.number_input("Birim Satış Fiyatı (TL) *", min_value=0.0, value=float(d_fiyat), format="%.2f", key="satis_birim_fiyat")
            st.caption(f" Girilen Satış Fiyatı: **{para_formatla(satis_fiyati)}**")
        with col2:
            ham_musteri = st.text_input("Müşteri Adı *", value=d_musteri, key="satis_musteri")
            kanal_idx = satilan_yer_listesi.index(d_yer) if d_yer in satilan_yer_listesi else 0
            satilan_yer = st.selectbox("Satış Yeri / Kanal *", satilan_yer_listesi, index=kanal_idx, key="satis_kanal")
            siparis_no = st.text_input("Sipariş No veya Fiş No *", value=d_siparis, key="satis_siparis_no")
            
        buton_satis_metni = " Satışı Güncelle" if st.session_state.satis_duzenle_id else " Satışı Gerçekleştir ve Kaydet"
        if st.button(buton_satis_metni, type="primary"):
            s_barkod_val = st.session_state.get("input_satis_barkod", "").strip()
            s_kod_val = st.session_state.get("input_satis_kod", "").strip()
    
            if not s_tarih or (not s_barkod_val and not s_kod_val) or not ham_musteri or not siparis_no or satis_fiyati <= 0:
                st.error(" Eksik alanlar var!")
            else:
                if s_barkod_val:
                    stok_res = supabase.table("stok").select("*").ilike("barkod", s_barkod_val).order("id", desc=False).execute()
                    sorgulanan_anahtar = s_barkod_val
                else:
                    stok_res = supabase.table("stok").select("*").ilike("urun_kodu", s_kod_val).order("id", desc=False).execute()
                    sorgulanan_anahtar = s_kod_val
    
                stok_girisleri = stok_res.data if stok_res.data else []
                if not stok_girisleri:
                    st.error(" Hata: Girdiğiniz kriterlere uygun sisteme kayıtlı bir Ürün Girişi bulunamadı!")
                else:
                    toplam_giris = sum([row.get("adet", 0) for row in stok_girisleri])
                    aranan_kod_barkod = sorgulanan_anahtar.lower()
                    
                    satislar_res = supabase.table("satis").select("satis_adet, barkod_kod, id").execute()
                    diger_satislar = 0
                    if satislar_res.data:
                        for sat in satislar_res.data:
                            if str(sat.get("barkod_kod")).strip().lower() == aranan_kod_barkod:
                                if st.session_state.satis_duzenle_id and sat.get("id") == st.session_state.satis_duzenle_id:
                                    continue
                                diger_satislar += sat.get("satis_adet", 0)

                    kalan_stok = toplam_giris - diger_satislar
                    
                    if satis_adet > kalan_stok:
                        st.error(f" Yetersiz Stok! Depoda kalan güncel stok: **{kalan_stok} Adet**.")
                    else:
                        onceki_satislar = diger_satislar
                        gecerli_satis_baslangic = onceki_satislar
                        gecerli_satis_bitis = onceki_satislar + satis_adet
                        
                        kumulatif_giris = 0
                        toplam_maliyet_fifo = 0.0
                        for row in stok_girisleri:
                            g_adet = row.get("adet", 0)
                            g_mal_val = para_metin_to_float(row.get("toplam_maliyet"))
                            birim_mal = g_mal_val / g_adet if g_adet > 0 else 0.0
                            
                            parti_baslangic = kumulatif_giris
                            parti_bitis = kumulatif_giris + g_adet
                            kumulatif_giris = parti_bitis
                            
                            kesisen_baslangic = max(parti_baslangic, gecerli_satis_baslangic)
                            kesisen_bitis = min(parti_bitis, gecerli_satis_bitis)
                            
                            if kesisen_bitis > kesisen_baslangic:
                                kesisen_adet = kesisen_bitis - kesisen_baslangic
                                toplam_maliyet_fifo += kesisen_adet * birim_mal
    
                        toplam_tutar = satis_adet * satis_fiyati
                        musteri_temiz = ham_musteri.strip().title()
                        bulunan_ilk = stok_girisleri[0]
                        u_adi = bulunan_ilk.get("urun_adi")
                        u_kod = bulunan_ilk.get("urun_kodu") or s_kod_val
                        kayit_barkod_kod = s_barkod_val if s_barkod_val else s_kod_val

                        satis_dict_data = {
                            "tarih": s_tarih,
                            "siparis_no": siparis_no,
                            "barkod_kod": kayit_barkod_kod,
                            "satis_adet": int(satis_adet),
                            "birim_fiyat": para_formatla(satis_fiyati),
                            "musteri": musteri_temiz,
                            "satilan_yer": satilan_yer,
                            "toplam_tutar": para_formatla(toplam_tutar)
                        }

                        kanal_kontrol = satilan_yer.replace(" ", "").lower()
                        
                        if st.session_state.satis_duzenle_id:
                            supabase.table("satis").update(satis_dict_data).eq("id", st.session_state.satis_duzenle_id).execute()
                            
                            for tbl in ["hepsi_burada", "web_sitesi", "dukkan_elden"]:
                                supabase.table(tbl).delete().eq("siparis_no", d_siparis).eq("musteri", d_musteri).execute()

                            kanal_tablosu = None
                            if "hepsiburada" in kanal_kontrol: kanal_tablosu = "hepsi_burada"
                            elif "websitesi" in kanal_kontrol or "web" in kanal_kontrol: kanal_tablosu = "web_sitesi"
                            elif "dukkan" in kanal_kontrol or "elden" in kanal_kontrol: kanal_tablosu = "dukkan_elden"

                            if kanal_tablosu:
                                sub_data = {
                                    "tarih": s_tarih, "siparis_no": siparis_no, "urun_kodu": u_kod, 
                                    "urun_adi": u_adi, "musteri": musteri_temiz, "adet": int(satis_adet), 
                                    "maliyet": toplam_maliyet_fifo, "satis_tutari": toplam_tutar, "giderler_girildi": 0
                                }
                                supabase.table(kanal_tablosu).insert(sub_data).execute()

                            st.session_state.satis_duzenle_id = None
                            basari_mesaji = " Satış başarıyla güncellendi!"
                        else:
                            supabase.table("satis").insert(satis_dict_data).execute()
                            
                            kanal_tablosu = None
                            if "hepsiburada" in kanal_kontrol: kanal_tablosu = "hepsi_burada"
                            elif "websitesi" in kanal_kontrol or "web" in kanal_kontrol: kanal_tablosu = "web_sitesi"
                            elif "dukkan" in kanal_kontrol or "elden" in kanal_kontrol: kanal_tablosu = "dukkan_elden"

                            if kanal_tablosu:
                                sub_data = {
                                    "tarih": s_tarih, "siparis_no": siparis_no, "urun_kodu": u_kod, 
                                    "urun_adi": u_adi, "musteri": musteri_temiz, "adet": int(satis_adet), 
                                    "maliyet": toplam_maliyet_fifo, "satis_tutari": toplam_tutar, "giderler_girildi": 0
                                }
                                supabase.table(kanal_tablosu).insert(sub_data).execute()
                            basari_mesaji = " Satış başarıyla gerçekleştirildi!"
    
                        st.success(basari_mesaji)
                        st.session_state.satis_barkod = ""
                        st.session_state.satis_kod = ""
                        st.rerun()
    
        st.divider()
        st.subheader(" Düzenlenecek veya Silinecek Satışı Arayın")
        satis_arama_metni = st.text_input("Aramak İstediğiniz Sipariş No, Müşteri Adı veya Barkod/Kodu Yazın:", placeholder="Örn: Sipariş No, Müşteri...", key="satis_arama_input").strip()
    
        secilen_satis_id = None
        if satis_arama_metni:
            s_ara_res = supabase.table("satis").select("id, tarih, siparis_no, musteri, barkod_kod, satis_adet, toplam_tutar").or_(f"siparis_no.ilike.%{satis_arama_metni}%,musteri.ilike.%{satis_arama_metni}%,barkod_kod.ilike.%{satis_arama_metni}%").order("id", desc=True).limit(15).execute()
            bulunan_satislar = s_ara_res.data if s_ara_res.data else []
    
            if bulunan_satislar:
                satis_secenekleri_dict = {f"Sipariş No: {s['siparis_no']} | Müşteri: {s['musteri']} | Barkod/Kod: {s['barkod_kod']} | Tarih: {s['tarih']}": s['id'] for s in bulunan_satislar}
                secilen_satis_etiket = st.selectbox("Eşleşen Satışlar Arasından Seçin:", list(satis_secenekleri_dict.keys()), key="bulunan_satislar_box")
                secilen_satis_id = satis_secenekleri_dict[secilen_satis_etiket]
            else:
                st.warning(" Aradığınız kriterlere uygun satış kaydı bulunamadı.")
        else:
            st.info(" Satış düzenlemek veya silmek için arama kutusunu kullanın.")
    
        if secilen_satis_id:
            col_islem1, col_islem2 = st.columns(2)
            with col_islem1:
                if st.button(" Seçilen Satışı Düzenle", use_container_width=True):
                    st.session_state.satis_duzenle_id = secilen_satis_id
                    st.session_state.satis_barkod = ""
                    st.session_state.satis_kod = ""
                    st.rerun()
            with col_islem2:
                if st.button(" Seçilen Satışı Sil", type="primary", use_container_width=True):
                    sil_res = supabase.table("satis").select("siparis_no, musteri, satilan_yer").eq("id", secilen_satis_id).execute()
                    if sil_res.data:
                        s_sip, s_mus, s_yer = sil_res.data[0].get("siparis_no"), sil_res.data[0].get("musteri"), sil_res.data[0].get("satilan_yer")
                        supabase.table("satis").delete().eq("id", secilen_satis_id).execute()
                        kanal_kontrol = s_yer.replace(" ", "").lower()
                        for tbl in ["hepsi_burada", "web_sitesi", "dukkan_elden"]:
                            supabase.table(tbl).delete().eq("siparis_no", s_sip).eq("musteri", s_mus).execute()
                        st.success(" Seçilen satış kaydı silindi!")
                        st.rerun()
    
        st.divider()
        st.subheader(" Geçmiş Satışlar ve Tarih Filtresi")
        
        satis_Tum_res = supabase.table("satis").select("tarih").execute()
        tum_sat_tarihler = []
        if satis_Tum_res.data:
            for r in satis_Tum_res.data:
                dt_parse = pd.to_datetime(r.get("tarih"), format="%d.%m.%Y", errors='coerce')
                if pd.notnull(dt_parse): tum_sat_tarihler.append(dt_parse.date())

        if tum_sat_tarihler:
            min_sat_t = min(tum_sat_tarihler)
            max_sat_t = max(tum_sat_tarihler)
            col_stf1, col_stf2 = st.columns(2)
            with col_stf1: satis_bas_tarih = st.date_input("Satış Başlangıç Tarihi", value=min_sat_t, min_value=min_sat_t, max_value=max_sat_t, key="satis_bas_tarih_filtre")
            with col_stf2: satis_bit_tarih = st.date_input("Satış Bitiş Tarihi", value=max_sat_t, min_value=min_sat_t, max_value=max_sat_t, key="satis_bit_tarih_filtre")
        else:
            satis_bas_tarih, satis_bit_tarih = None, None

        satis_son_res = supabase.table("satis").select("*").order("id", desc=True).execute()
        satis_kayitlari = satis_son_res.data if satis_son_res.data else []
        
        if satis_kayitlari:
            gecmis_verisi = []
            for s in satis_kayitlari:
                s_id, s_tarih_str, s_siparis, s_barkod_kod, s_adet, s_fiyat, s_musteri, s_yer, s_tutar = (
                    s.get("id"), s.get("tarih"), s.get("siparis_no"), s.get("barkod_kod"), 
                    s.get("satis_adet"), s.get("birim_fiyat"), s.get("musteri"), s.get("satilan_yer"), s.get("toplam_tutar")
                )
                
                dt_s = pd.to_datetime(s_tarih_str, format="%d.%m.%Y", errors='coerce')
                if satis_bas_tarih and satis_bit_tarih and pd.notnull(dt_s):
                    if not (satis_bas_tarih <= dt_s.date() <= satis_bit_tarih):
                        continue

                stk_bul_res = supabase.table("stok").select("barkod, urun_kodu").or_(f"barkod.eq.{s_barkod_kod},urun_kodu.eq.{s_barkod_kod}").limit(1).execute()
                stk_bul = stk_bul_res.data[0] if stk_bul_res.data else None
                
                gercek_barkod = stk_bul.get("barkod") if stk_bul and stk_bul.get("barkod") else s_barkod_kod
                gercek_kod = stk_bul.get("urun_kodu") if stk_bul and stk_bul.get("urun_kodu") else "-"
                
                gecmis_verisi.append({
                    "Tarih": s_tarih_str,
                    "Sipariş No": s_siparis,
                    "Ürün Kodu": gercek_kod,
                    "Barkod": gercek_barkod,
                    "Adet": s_adet,
                    "Birim Fiyat": para_formatla(para_metin_to_float(s_fiyat)),
                    "Müşteri": s_musteri,
                    "Satış Yeri": s_yer,
                    "Toplam Tutar": para_formatla(para_metin_to_float(s_tutar))
                })
            
            if gecmis_verisi:
                st.dataframe(pd.DataFrame(gecmis_verisi), use_container_width=True, hide_index=True)
            else:
                st.info("Seçilen tarih aralığında satış kaydı bulunamadı.")
        else:
            st.info(" Kayıt bulunamadı.")
    
    # --- 3. GÜNCEL STOK ---
    elif menu == " 3. Güncel Stok":
        st.header(" Güncel Kalan Stok ve Finansal Özet")
        
        stok_rows_res = supabase.table("stok").select("*").order("id", desc=False).execute()
        stok_rows = pd.DataFrame(stok_rows_res.data) if stok_rows_res.data else pd.DataFrame()
        
        satis_rows_res = supabase.table("satis").select("barkod_kod, satis_adet").execute()
        satis_rows = pd.DataFrame(satis_rows_res.data) if satis_rows_res.data else pd.DataFrame()
        
        kat_res = supabase.table("tanimlar").select("deger").eq("tip", "kategori_marka").order("deger", desc=False).execute()
        kategori_listesi = ["Tümü"] + [row["deger"] for row in kat_res.data] if kat_res.data else ["Tümü"]
    
        bugun = datetime.now()
        satis_dict = {}
        if not satis_rows.empty:
            for _, row in satis_rows.iterrows():
                sk = str(row['barkod_kod']).strip().lower()
                satis_dict[sk] = satis_dict.get(sk, 0) + row['satis_adet']
    
        partiler_gruplu = {}
        if not stok_rows.empty:
            for _, r in stok_rows.iterrows():
                barkod, kod = r.get('barkod') or "", r.get('urun_kodu') or ""
                b_key = barkod.strip().lower()
                k_key = kod.strip().lower()
                anahtar = k_key if k_key else b_key
                if anahtar not in partiler_gruplu: partiler_gruplu[anahtar] = []
                partiler_gruplu[anahtar].append(r)
    
        st.subheader(" Stok Filtreleme & Kritik Seviye Ayarları")
        c_f1, c_f2, c_f3, c_f4 = st.columns([2, 2, 2, 1])
        with c_f1: stok_arama = st.text_input(" Stok / Barkod Arama:", placeholder="Barkod okutun veya arama yapın...", key="stok_arama_input").strip().lower()
        with c_f2: secilen_kategori_filtre = st.selectbox(" Kategori / Marka Filtresi:", kategori_listesi)
        with c_f3: stok_siralama = st.selectbox(" Sıralama Kriteri:", ["Kritik Stok / Azalan Adet ", "Rafta Bekleme Günü (En Eski) ", "Bağlı Sermaye (En Yüksek) ", "Ürün Adı (A-Z) ", "Kalan Adet (En Yüksek) "])
        with c_f4: kritik_esik = st.number_input(" Kritik Stok Eşiği:", min_value=0, value=3, step=1)
    
        islenmis_stoklar = []
        toplam_bagli_sermaye = 0.0
    
        for anahtar, partiler in partiler_gruplu.items():
            toplam_satis_adet = satis_dict.get(anahtar, 0)
            for r in partiler:
                barkod, kod, ad, kategori, alinan_yer, parti_adet, giris_tarihi_str, t_maliyet = (
                    r.get('barkod') or "", r.get('urun_kodu') or "", r.get('urun_adi'), 
                    r.get('kategori_marka') or "-", r.get('alinan_yer') or "-", r.get('adet', 0), 
                    r.get('tarih'), r.get('toplam_maliyet')
                )
                mal_val = para_metin_to_float(t_maliyet)
                birim_maliyet = mal_val / parti_adet if parti_adet > 0 else 0.0
    
                if toplam_satis_adet >= parti_adet:
                    kalan_parti_adet = 0
                    toplam_satis_adet -= parti_adet
                else:
                    kalan_parti_adet = parti_adet - toplam_satis_adet
                    toplam_satis_adet = 0
    
                sermaye_val = kalan_parti_adet * birim_maliyet
                toplam_bagli_sermaye += sermaye_val
                gun_farki = 0
                try:
                    g_tarih = datetime.strptime(giris_tarihi_str.strip(), "%d.%m.%Y")
                    gun_farki = max(0, (bugun - g_tarih).days)
                except: pass
    
                durum = " Tükendi" if kalan_parti_adet <= 0 else (" Kritik / Azalıyor" if kalan_parti_adet <= kritik_esik else " Normal")
    
                if secilen_kategori_filtre != "Tümü" and kategori != secilen_kategori_filtre: continue
                arama_metni_birlesik = f"{ad} {kod} {barkod} {kategori} {alinan_yer}".lower()
                if stok_arama and stok_arama not in arama_metni_birlesik: continue
    
                islenmis_stoklar.append({
                    "Ürün Adı": ad,
                    "Kategori": kategori,
                    "Alınan Yer": alinan_yer,
                    "Kod": kod.strip() if kod else "-",
                    "Barkod": barkod.strip() if barkod else "-",
                    "Rafta Gün": gun_farki,
                    "Kalan Adet": kalan_parti_adet,
                    "Sermaye_Val": sermaye_val,
                    "Bağlı Sermaye": para_formatla(sermaye_val),
                    "Durum": durum
                })
    
        df_stok_liste = pd.DataFrame(islenmis_stoklar)
        if not df_stok_liste.empty:
            if stok_siralama == "Kritik Stok / Azalan Adet ": df_stok_liste = df_stok_liste.sort_values(by="Kalan Adet", ascending=True)
            elif stok_siralama == "Rafta Bekleme Günü (En Eski) ": df_stok_liste = df_stok_liste.sort_values(by="Rafta Gün", ascending=False)
            elif stok_siralama == "Bağlı Sermaye (En Yüksek) ": df_stok_liste = df_stok_liste.sort_values(by="Sermaye_Val", ascending=False)
            elif stok_siralama == "Ürün Adı (A-Z) ": df_stok_liste = df_stok_liste.sort_values(by="Ürün Adı", ascending=True)
            elif stok_siralama == "Kalan Adet (En Yüksek) ": df_stok_liste = df_stok_liste.sort_values(by="Kalan Adet", ascending=False)
    
            col_stk1, col_stk2, col_stk3 = st.columns(3)
            col_stk1.metric(" Toplam Kalan Ürün Adeti", f"{df_stok_liste['Kalan Adet'].sum()} Adet")
            col_stk2.metric(" Toplam Bağlı Sermaye", para_formatla(toplam_bagli_sermaye))
            kritik_sayisi = len(df_stok_liste[df_stok_liste['Kalan Adet'] <= kritik_esik])
            col_stk3.metric(" Kritik/Tükenen Ürün Sayısı", f"{kritik_sayisi} Çeşit")
            
            if secilen_kategori_filtre != "Tümü":
                filtrelenmis_toplam_adet = df_stok_liste['Kalan Adet'].sum()
                filtrelenmis_toplam_maliyet = df_stok_liste['Sermaye_Val'].sum()
                st.info(f" Seçilen **{secilen_kategori_filtre}** markası için toplam kalan adet: **{filtrelenmis_toplam_adet} Adet** | Toplam Maliyet: **{para_formatla(filtrelenmis_toplam_maliyet)}**")
    
            st.divider()
            st.dataframe(df_stok_liste[["Durum", "Ürün Adı", "Kategori", "Alınan Yer", "Kod", "Barkod", "Rafta Gün", "Kalan Adet", "Bağlı Sermaye"]], use_container_width=True, hide_index=True)
        else:
            st.info(" Aradığınız kriterlere uygun güncel stok bulunamadı.")
    
    # --- 4. HEPSİ BURADA ---
    elif menu == " 4. Hepsi Burada":
        st.header(" Hepsi Burada Finans ve Kar/Zarar Yönetimi")
        
        if "hb_duzenle_id" not in st.session_state:
            st.session_state.hb_duzenle_id = None

        hb_res = supabase.table("hepsi_burada").select("*").order("id", desc=True).execute()
        hb_df = pd.DataFrame(hb_res.data) if hb_res.data else pd.DataFrame()
    
        if not hb_df.empty:
            hb_df['tarih_dt'] = pd.to_datetime(hb_df['tarih'], format="%d.%m.%Y", errors='coerce')
            tum_hb_tarihler = hb_df['tarih_dt'].dropna().dt.date.tolist()
            
            if tum_hb_tarihler:
                min_hb_t = min(tum_hb_tarihler)
                max_hb_t = max(tum_hb_tarihler)
                st.subheader(" Tarih Aralığı Filtresi")
                col_hbt1, col_hbt2 = st.columns(2)
                with col_hbt1: hb_bas_tarih = st.date_input("Başlangıç Tarihi", value=min_hb_t, min_value=min_hb_t, max_value=max_hb_t, key="hb_bas_tarih_filtre")
                with col_hbt2: hb_bit_tarih = st.date_input("Bitiş Tarihi", value=max_hb_t, min_value=min_hb_t, max_value=max_hb_t, key="hb_bit_tarih_filtre")
                
                hb_df = hb_df[(hb_df['tarih_dt'].dt.date >= hb_bas_tarih) & (hb_df['tarih_dt'].dt.date <= hb_bit_tarih)].copy()
                st.divider()

        if not hb_df.empty:
            bekleyen_df = hb_df[hb_df["giderler_girildi"] == 0].copy()
            tamamlanan_df = hb_df[hb_df["giderler_girildi"] == 1].copy()
            
            col_m1, col_m2, col_m3, col_m4 = st.columns(4)
            col_m1.metric(" Toplam Sipariş", f"{len(hb_df)} Adet")
            col_m2.metric(" Gideri Bekleyen", f"{len(bekleyen_df)} Adet")
            col_m3.metric(" Tamamlanan Ciro", para_formatla(tamamlanan_df['satis_tutari'].sum() if not tamamlanan_df.empty else 0.0))
            col_m4.metric(" Net Kâr / Zarar", para_formatla(tamamlanan_df['net_kar_zarar'].sum() if not tamamlanan_df.empty else 0.0))
            
            st.divider()
            hb_arama = st.text_input(" Hepsi Burada Sipariş veya Müşteri Ara:", placeholder="Sipariş No, Müşteri veya Ürün Adı...", key="hb_arama_input").strip().lower()
            if hb_arama:
                bekleyen_df = bekleyen_df[bekleyen_df['siparis_no'].astype(str).str.lower().str.contains(hb_arama) | bekleyen_df['musteri'].astype(str).str.lower().str.contains(hb_arama) | bekleyen_df['urun_adi'].astype(str).str.lower().str.contains(hb_arama)]
                tamamlanan_df = tamamlanan_df[tamamlanan_df['siparis_no'].astype(str).str.lower().str.contains(hb_arama) | tamamlanan_df['musteri'].astype(str).str.lower().str.contains(hb_arama) | tamamlanan_df['urun_adi'].astype(str).str.lower().str.contains(hb_arama)]
    
            tab_hb1, tab_hb2 = st.tabs([" Gider Girişi Bekleyenler", " Gideri Tamamlananlar & Geçmiş"])
    
            with tab_hb1:
                if not bekleyen_df.empty:
                    st.subheader(" Gider ve Kesinti Girişi Bekleyen Siparişler")
                    c_bs1, c_bs2 = st.columns(2)
                    with c_bs1: bekleyen_sira = st.selectbox(" Sırala:", ["Ekleme Sırası (ID)", "Tarih (En Yeni)", "Satış Tutarı (En Yüksek)"], key="bekleyen_sira_secim")
                    with c_bs2: st.caption(" Bekleyen sipariş listesini sıralayın.")
    
                    if bekleyen_sira == "Tarih (En Yeni)": bekleyen_df = bekleyen_df.sort_values(by="tarih_dt", ascending=False)
                    elif bekleyen_sira == "Satış Tutarı (En Yüksek)": bekleyen_df = bekleyen_df.sort_values(by="satis_tutari", ascending=False)
                    else: bekleyen_df = bekleyen_df.sort_values(by="id", ascending=False)
    
                    with st.expander(" Tüm Bekleyenlere Varsayılan Oranlı Toplu Gider Uygula"):
                        with st.form("toplu_gider_form"):
                            c_top1, c_top2, c_top3 = st.columns(3)
                            with c_top1: vars_kom_yuzde = st.number_input("Komisyon Oranı (%)", min_value=0.0, value=15.0, step=0.5)
                            with c_top2: vars_kargo = st.number_input("Kargo Bedeli (TL)", min_value=0.0, value=45.0, step=5.0)
                            with c_top3: vars_hizmet = st.number_input("Hizmet Bedeli (TL)", min_value=0.0, value=8.5, step=0.5)
                                
                            if st.form_submit_button(" Tüm Bekleyenlere Uygula ve Kaydet"):
                                for _, b_row in bekleyen_df.iterrows():
                                    s_tut = b_row['satis_tutari']
                                    kom = s_tut * (vars_kom_yuzde / 100.0)
                                    net_o = s_tut - kom - vars_kargo - vars_hizmet
                                    net_k = net_o - b_row['maliyet']
                                    supabase.table("hepsi_burada").update({
                                        "gelen_odeme": net_o, "komisyon": kom, "kargo": vars_kargo, 
                                        "hizmet_bedeli": vars_hizmet, "net_kar_zarar": net_k, "giderler_girildi": 1
                                    }).eq("id", b_row['id']).execute()
                                st.success(" Tüm bekleyen siparişlere varsayılan giderler uygulandı!")
                                st.rerun()
    
                    st.divider()
                    hb_bekleyen_tablo = []
                    for _, b_row in bekleyen_df.iterrows():
                        hb_bekleyen_tablo.append({
                            "Tarih": b_row['tarih'], "Sipariş No": b_row['siparis_no'], "Müşteri": b_row['musteri'],
                            "Ürün Adı": b_row['urun_adi'], "Adet": b_row['adet'], "Maliyet": para_formatla(b_row['maliyet']), "Satış Tutarı": para_formatla(b_row['satis_tutari'])
                        })
                    st.dataframe(pd.DataFrame(hb_bekleyen_tablo), use_container_width=True, hide_index=True)
    
                    st.divider()
                    bekleyen_arama_input = st.text_input(" Gideri Girilecek Siparişi Arayın:", placeholder="Sipariş No veya Müşteri...", key="hb_bekleyen_arama_input").strip()
                    secilen_bekleyen_id = None
                    if bekleyen_arama_input:
                        filt_bekleyen = bekleyen_df[bekleyen_df['siparis_no'].astype(str).str.lower().str.contains(bekleyen_arama_input.lower()) | bekleyen_df['musteri'].astype(str).str.lower().str.contains(bekleyen_arama_input.lower())]
                        if not filt_bekleyen.empty:
                            secenekler_dict = {f"Sipariş No: {r['siparis_no']} | Müşteri: {r['musteri']} | Ürün: {r['urun_adi']}": r['id'] for _, r in filt_bekleyen.iterrows()}
                            secilen_etiket = st.selectbox("Eşleşen Siparişler Arasından Seçin:", list(secenekler_dict.keys()), key="hb_bulunan_bekleyen_box")
                            secilen_bekleyen_id = secenekler_dict[secilen_etiket]
                        else: st.warning(" Eşleşen sipariş bulunamadı.")
                    else: st.info(" Gider girmek için arama kutusuna sipariş no veya müşteri adı yazın.")
    
                    if secilen_bekleyen_id:
                        row = bekleyen_df[bekleyen_df['id'] == secilen_bekleyen_id].iloc[0]
                        with st.form(key=f"hb_form_{row['id']}"):
                            f_col1, f_col2, f_col3 = st.columns(3)
                            with f_col1:
                                gelen_odeme = st.number_input("H.B.'dan Gelen Net Ödeme (TL)", min_value=0.0, value=float(row['gelen_odeme']), format="%.2f", key=f"hb_gelen_{row['id']}")
                                kampanya = st.number_input("Kampanya / Kupon Desteği (TL)", min_value=0.0, value=float(row['kampanya']), format="%.2f", key=f"hb_kamp_{row['id']}")
                                komisyon = st.number_input("Komisyon Bedeli (TL)", min_value=0.0, value=float(row['komisyon']), format="%.2f", key=f"hb_kom_{row['id']}")
                            with f_col2:
                                stopaj = st.number_input("Stopaj Kesintisi (TL)", min_value=0.0, value=float(row['stopaj']), format="%.2f", key=f"hb_stop_{row['id']}")
                                kargo = st.number_input("Kargo Bedeli (TL)", min_value=0.0, value=float(row['kargo']), format="%.2f", key=f"hb_karg_{row['id']}")
                                hizmet_bedeli = st.number_input("Hizmet Bedeli (TL)", min_value=0.0, value=float(row['hizmet_bedeli']), format="%.2f", key=f"hb_hiz_{row['id']}")
                            with f_col3:
                                tahsilat_yonetim = st.number_input("Tahsilat Yönetim Bedeli (TL)", min_value=0.0, value=float(row['tahsilat_yonetim']), format="%.2f", key=f"hb_tah_{row['id']}")
                                st.markdown(f"**Ürün Maliyeti:** {para_formatla(row['maliyet'])}")
                                st.markdown(f"**Satış Tutarı:** {para_formatla(row['satis_tutari'])}")
    
                            if st.form_submit_button(" Hesapla ve Kaydet"):
                                toplam_diger = komisyon + stopaj + kargo + hizmet_bedeli + tahsilat_yonetim
                                net_kar = gelen_odeme + kampanya - row['maliyet'] - toplam_diger
                                supabase.table("hepsi_burada").update({
                                    "gelen_odeme": gelen_odeme, "kampanya": kampanya, "komisyon": komisyon, 
                                    "stopaj": stopaj, "kargo": kargo, "hizmet_bedeli": hizmet_bedeli, 
                                    "tahsilat_yonetim": tahsilat_yonetim, "net_kar_zarar": net_kar, "giderler_girildi": 1
                                }).eq("id", row['id']).execute()
                                st.success(" Giderler kaydedildi!")
                                st.rerun()
                else: st.info(" Gider bekleyen sipariş bulunmuyor.")
    
            with tab_hb2:
                if not tamamlanan_df.empty:
                    st.subheader(" Gider ve Finans Detayları Tamamlanmış Siparişler")
                    
                    if st.session_state.hb_duzenle_id:
                        duzenlenen_kayit_res = tamamlanan_df[tamamlanan_df['id'] == st.session_state.hb_duzenle_id]
                        if not duzenlenen_kayit_res.empty:
                            d_row = duzenlenen_kayit_res.iloc[0]
                            st.info(f" Sipariş No: **{d_row['siparis_no']}** ({d_row['musteri']}) için giderleri düzenliyorsunuz:")
                            with st.form(key=f"hb_duzenle_form_{d_row['id']}"):
                                f_col1, f_col2, f_col3 = st.columns(3)
                                with f_col1:
                                    d_gelen = st.number_input("H.B.'dan Gelen Net Ödeme (TL)", min_value=0.0, value=float(d_row['gelen_odeme']), format="%.2f")
                                    d_kamp = st.number_input("Kampanya / Kupon Desteği (TL)", min_value=0.0, value=float(d_row['kampanya']), format="%.2f")
                                    d_kom = st.number_input("Komisyon Bedeli (TL)", min_value=0.0, value=float(d_row['komisyon']), format="%.2f")
                                with f_col2:
                                    d_stop = st.number_input("Stopaj Kesintisi (TL)", min_value=0.0, value=float(d_row['stopaj']), format="%.2f")
                                    d_karg = st.number_input("Kargo Bedeli (TL)", min_value=0.0, value=float(d_row['kargo']), format="%.2f")
                                    d_hiz = st.number_input("Hizmet Bedeli (TL)", min_value=0.0, value=float(d_row['hizmet_bedeli']), format="%.2f")
                                with f_col3:
                                    d_tah = st.number_input("Tahsilat Yönetim Bedeli (TL)", min_value=0.0, value=float(d_row['tahsilat_yonetim']), format="%.2f")
                                    st.markdown(f"**Ürün Maliyeti:** {para_formatla(d_row['maliyet'])}")
                                    st.markdown(f"**Satış Tutarı:** {para_formatla(d_row['satis_tutari'])}")
        
                                col_btn1, col_btn2 = st.columns(2)
                                with col_btn1:
                                    if st.form_submit_button(" Güncellemeyi Kaydet"):
                                        toplam_diger_d = d_kom + d_stop + d_karg + d_hiz + d_tah
                                        net_kar_d = d_gelen + d_kamp - d_row['maliyet'] - toplam_diger_d
                                        supabase.table("hepsi_burada").update({
                                            "gelen_odeme": d_gelen, "kampanya": d_kamp, "komisyon": d_kom, 
                                            "stopaj": d_stop, "kargo": d_karg, "hizmet_bedeli": d_hiz, 
                                            "tahsilat_yonetim": d_tah, "net_kar_zarar": net_kar_d, "giderler_girildi": 1
                                        }).eq("id", d_row['id']).execute()
                                        st.session_state.hb_duzenle_id = None
                                        st.success(" Giderler güncellendi!")
                                        st.rerun()
                                with col_btn2:
                                    if st.form_submit_button(" İptal Et"):
                                        st.session_state.hb_duzenle_id = None
                                        st.rerun()
                            st.divider()

                    b_cols = st.columns([1.1, 1.2, 1.3, 1.8, 0.6, 1.2, 1.4, 1.3, 1.3, 1.4, 0.8])
                    b_cols[0].markdown("**Tarih**")
                    b_cols[1].markdown("**Sipariş No**")
                    b_cols[2].markdown("**Müşteri**")
                    b_cols[3].markdown("**Ürün Adı**")
                    b_cols[4].markdown("**Adet**")
                    b_cols[5].markdown("**Maliyet**")
                    b_cols[6].markdown("**Satış Tutarı**")
                    b_cols[7].markdown("**Gelen Ödeme**")
                    b_cols[8].markdown("**Net Kâr**")
                    b_cols[10].markdown("**İşlem**")
                    st.divider()

                    for _, t_row in tamamlanan_df.iterrows():
                        cols = st.columns([1.1, 1.2, 1.3, 1.8, 0.6, 1.2, 1.4, 1.3, 1.3, 1.4, 0.8])
                        cols[0].write(t_row['tarih'])
                        cols[1].write(str(t_row['siparis_no']))
                        cols[2].write(str(t_row['musteri']))
                        cols[3].write(str(t_row['urun_adi']))
                        cols[4].write(str(t_row['adet']))
                        cols[5].write(para_formatla(t_row['maliyet']))
                        cols[6].write(para_formatla(t_row['satis_tutari']))
                        cols[7].write(para_formatla(t_row['gelen_odeme']))
                        cols[8].write(para_formatla(t_row['net_kar_zarar']))
                        
                        if cols[10].button(" Düzenle", key=f"hb_duzenle_btn_{t_row['id']}"):
                            st.session_state.hb_duzenle_id = t_row['id']
                            st.rerun()
                else: st.info(" Tamamlanmış Hepsi Burada sipariş kaydı bulunmuyor.")
        else: st.info(" Hepsi Burada satış kaydı bulunmuyor.")
    
    # --- 5. WEB SİTESİ ---
    elif menu == " 5. Web Sitesi":
        st.header(" Web Sitesi Finans ve Kar/Zarar Yönetimi")
        
        if "web_duzenle_id" not in st.session_state:
            st.session_state.web_duzenle_id = None

        web_res = supabase.table("web_sitesi").select("*").order("id", desc=True).execute()
        web_df = pd.DataFrame(web_res.data) if web_res.data else pd.DataFrame()
    
        if not web_df.empty:
            web_df['tarih_dt'] = pd.to_datetime(web_df['tarih'], format="%d.%m.%Y", errors='coerce')
            tum_web_tarihler = web_df['tarih_dt'].dropna().dt.date.tolist()
            
            if tum_web_tarihler:
                min_w_t = min(tum_web_tarihler)
                max_w_t = max(tum_web_tarihler)
                st.subheader(" Tarih Aralığı Filtresi")
                col_wt1, col_wt2 = st.columns(2)
                with col_wt1: web_bas_tarih = st.date_input("Başlangıç Tarihi", value=min_w_t, min_value=min_w_t, max_value=max_w_t, key="web_bas_tarih_filtre")
                with col_wt2: web_bit_tarih = st.date_input("Bitiş Tarihi", value=max_w_t, min_value=min_w_t, max_value=max_w_t, key="web_bit_tarih_filtre")
                
                web_df = web_df[(web_df['tarih_dt'].dt.date >= web_bas_tarih) & (web_df['tarih_dt'].dt.date <= web_bit_tarih)].copy()
                st.divider()

        if not web_df.empty:
            bekleyen_web = web_df[web_df["giderler_girildi"] == 0].copy()
            tamamlanan_web = web_df[web_df["giderler_girildi"] == 1].copy()
    
            col_w1, col_w2, col_w3, col_w4 = st.columns(4)
            col_w1.metric(" Toplam Sipariş", f"{len(web_df)} Adet")
            col_w2.metric(" Gideri Bekleyen", f"{len(bekleyen_web)} Adet")
            col_w3.metric(" Tamamlanan Ciro", para_formatla(tamamlanan_web['satis_tutari'].sum() if not tamamlanan_web.empty else 0.0))
            col_w4.metric(" Net Kâr / Zarar", para_formatla(tamamlanan_web['net_kar_zarar'].sum() if not tamamlanan_web.empty else 0.0))
    
            st.divider()
            tab_w1, tab_w2 = st.tabs([" Gider Girişi Bekleyenler", " Gideri Tamamlananlar & Geçmiş"])
    
            with tab_w1:
                if not bekleyen_web.empty:
                    web_bekleyen_tablo = []
                    for _, b_row in bekleyen_web.iterrows():
                        web_bekleyen_tablo.append({
                            "Tarih": b_row['tarih'], "Sipariş No": b_row['siparis_no'], "Müşteri": b_row['musteri'],
                            "Ürün Adı": b_row['urun_adi'], "Adet": b_row['adet'], "Maliyet": para_formatla(b_row['maliyet']), "Satış Tutarı": para_formatla(b_row['satis_tutari'])
                        })
                    st.dataframe(pd.DataFrame(web_bekleyen_tablo), use_container_width=True, hide_index=True)
    
                    st.divider()
                    web_arama_input = st.text_input(" Gideri Girilecek Web Siparişini Arayın:", placeholder="Sipariş No veya Müşteri...", key="web_bekleyen_arama_input").strip()
                    secilen_web_bekleyen_id = None
                    if web_arama_input:
                        filt_w_bekleyen = bekleyen_web[bekleyen_web['siparis_no'].astype(str).str.lower().str.contains(web_arama_input.lower()) | bekleyen_web['musteri'].astype(str).str.lower().str.contains(web_arama_input.lower())]
                        if not filt_w_bekleyen.empty:
                            w_secenekler_dict = {f"Sipariş No: {r['siparis_no']} | Müşteri: {r['musteri']}": r['id'] for _, r in filt_w_bekleyen.iterrows()}
                            w_secilen_etiket = st.selectbox("Eşleşen Siparişler Arasından Seçin:", list(w_secenekler_dict.keys()), key="web_bulunan_bekleyen_box")
                            secilen_web_bekleyen_id = w_secenekler_dict[w_secilen_etiket]
    
                    if secilen_web_bekleyen_id:
                        row = bekleyen_web[bekleyen_web['id'] == secilen_web_bekleyen_id].iloc[0]
                        with st.form(key=f"web_form_{row['id']}"):
                            w_col1, w_col2 = st.columns(2)
                            with w_col1:
                                val_pos = float(row['pos_kesintisi']) if row['pos_kesintisi'] is not None else 0.0
                                val_kargo = float(row['kargo']) if row['kargo'] is not None else 0.0
                                pos_kesintisi = st.number_input("POS Komisyonu (TL)", min_value=0.0, value=val_pos, format="%.2f", key=f"web_pos_{row['id']}")
                                kargo = st.number_input("Kargo Gideri (TL)", min_value=0.0, value=val_kargo, format="%.2f", key=f"web_kargo_{row['id']}")
                            with w_col2:
                                st.markdown(f"**Maliyet:** {para_formatla(row['maliyet'])} | **Ciro:** {para_formatla(row['satis_tutari'])}")
    
                            if st.form_submit_button(" Hesapla ve Kaydet"):
                                net_kar = row['satis_tutari'] - row['maliyet'] - pos_kesintisi - kargo
                                supabase.table("web_sitesi").update({
                                    "pos_kesintisi": pos_kesintisi, "kargo": kargo, 
                                    "net_kar_zarar": net_kar, "giderler_girildi": 1
                                }).eq("id", row['id']).execute()
                                st.success(" Web giderleri kaydedildi!")
                                st.rerun()
                else: st.info(" Gider bekleyen web siparişi yok.")
    
            with tab_w2:
                if not tamamlanan_web.empty:
                    if st.session_state.web_duzenle_id:
                        duzenlenen_w_res = tamamlanan_web[tamamlanan_web['id'] == st.session_state.web_duzenle_id]
                        if not duzenlenen_w_res.empty:
                            dw_row = duzenlenen_w_res.iloc[0]
                            st.info(f" Sipariş No: **{dw_row['siparis_no']}** ({dw_row['musteri']}) için web giderlerini düzenliyorsunuz:")
                            with st.form(key=f"web_duzenle_form_{dw_row['id']}"):
                                dw_col1, dw_col2 = st.columns(2)
                                with dw_col1:
                                    d_w_pos = st.number_input("POS Komisyonu (TL)", min_value=0.0, value=float(dw_row['pos_kesintisi'] or 0.0), format="%.2f")
                                    d_w_karg = st.number_input("Kargo Gideri (TL)", min_value=0.0, value=float(dw_row['kargo'] or 0.0), format="%.2f")
                                with dw_col2:
                                    st.markdown(f"**Ürün Maliyeti:** {para_formatla(dw_row['maliyet'])}")
                                    st.markdown(f"**Satış Tutarı:** {para_formatla(dw_row['satis_tutari'])}")
        
                                col_wbtn1, col_wbtn2 = st.columns(2)
                                with col_wbtn1:
                                    if st.form_submit_button(" Web Güncellemeyi Kaydet"):
                                        net_kar_dw = dw_row['satis_tutari'] - dw_row['maliyet'] - d_w_pos - d_w_karg
                                        supabase.table("web_sitesi").update({
                                            "pos_kesintisi": d_w_pos, "kargo": d_w_karg, 
                                            "net_kar_zarar": net_kar_dw, "giderler_girildi": 1
                                        }).eq("id", dw_row['id']).execute()
                                        st.session_state.web_duzenle_id = None
                                        st.success(" Web giderleri güncellendi!")
                                        st.rerun()
                                with col_wbtn2:
                                    if st.form_submit_button(" İptal Et"):
                                        st.session_state.web_duzenle_id = None
                                        st.rerun()
                            st.divider()

                    bw_cols = st.columns([1.1, 1.2, 1.3, 1.8, 0.6, 1.2, 1.4, 1.3, 1.3, 1.4, 0.8])
                    bw_cols[0].markdown("**Tarih**")
                    bw_cols[1].markdown("**Sipariş No**")
                    bw_cols[2].markdown("**Müşteri**")
                    bw_cols[3].markdown("**Ürün Adı**")
                    bw_cols[4].markdown("**Adet**")
                    bw_cols[5].markdown("**Maliyet**")
                    bw_cols[6].markdown("**Satış Tutarı**")
                    bw_cols[7].markdown("**POS Kom.**")
                    bw_cols[8].markdown("**Kargo**")
                    bw_cols[9].markdown("**Net Kâr**")
                    bw_cols[10].markdown("**İşlem**")
                    st.divider()

                    for _, t_row in tamamlanan_web.iterrows():
                        cols = st.columns([1.1, 1.2, 1.3, 1.8, 0.6, 1.2, 1.4, 1.3, 1.3, 1.4, 0.8])
                        cols[0].write(t_row['tarih'])
                        cols[1].write(str(t_row['siparis_no']))
                        cols[2].write(str(t_row['musteri']))
                        cols[3].write(str(t_row['urun_adi']))
                        cols[4].write(str(t_row['adet']))
                        cols[5].write(para_formatla(t_row['maliyet']))
                        cols[6].write(para_formatla(t_row['satis_tutari']))
                        cols[7].write(para_formatla(t_row['pos_kesintisi'] or 0))
                        cols[8].write(para_formatla(t_row['kargo'] or 0))
                        cols[9].write(para_formatla(t_row['net_kar_zarar']))
                        
                        if cols[10].button(" Düzenle", key=f"web_duzenle_btn_{t_row['id']}"):
                            st.session_state.web_duzenle_id = t_row['id']
                            st.rerun()
                else: st.info(" Tamamlanmış web siparişi yok.")
        else: st.info(" Web sitesi satış kaydı bulunmuyor.")
    
    # --- 6. DÜKKAN & ELDEN ---
    elif menu == " 6. Dükkan & Elden":
        st.header(" Dükkan & Elden Satış Yönetimi")
        
        if "dukkan_duzenle_id" not in st.session_state:
            st.session_state.dukkan_duzenle_id = None

        dukkan_res = supabase.table("dukkan_elden").select("*").order("id", desc=True).execute()
        dukkan_df = pd.DataFrame(dukkan_res.data) if dukkan_res.data else pd.DataFrame()
    
        if not dukkan_df.empty:
            dukkan_df['tarih_dt'] = pd.to_datetime(dukkan_df['tarih'], format="%d.%m.%Y", errors='coerce')
            tum_dukkan_tarihler = dukkan_df['tarih_dt'].dropna().dt.date.tolist()
            
            if tum_dukkan_tarihler:
                min_d_t = min(tum_dukkan_tarihler)
                max_d_t = max(tum_dukkan_tarihler)
                st.subheader(" Tarih Aralığı Filtresi")
                col_dt1, col_dt2 = st.columns(2)
                with col_dt1: dukkan_bas_tarih = st.date_input("Başlangıç Tarihi", value=min_d_t, min_value=min_d_t, max_value=max_d_t, key="dukkan_bas_tarih_filtre")
                with col_dt2: dukkan_bit_tarih = st.date_input("Bitiş Tarihi", value=max_d_t, min_value=min_d_t, max_value=max_d_t, key="dukkan_bit_tarih_filtre")
                
                dukkan_df = dukkan_df[(dukkan_df['tarih_dt'].dt.date >= dukkan_bas_tarih) & (dukkan_df['tarih_dt'].dt.date <= dukkan_bit_tarih)].copy()
                st.divider()

        if not dukkan_df.empty:
            bekleyen_d = dukkan_df[dukkan_df["giderler_girildi"] == 0].copy()
            tamamlanan_d = dukkan_df[dukkan_df["giderler_girildi"] == 1].copy()
    
            col_d1, col_d2, col_d3, col_d4 = st.columns(4)
            col_d1.metric(" Toplam Satış", f"{len(dukkan_df)} Adet")
            col_d2.metric(" Gideri Bekleyen", f"{len(bekleyen_d)} Adet")
            col_d3.metric(" Tamamlanan Ciro", para_formatla(tamamlanan_d['satis_tutari'].sum() if not tamamlanan_d.empty else 0.0))
            col_d4.metric(" Net Kâr / Zarar", para_formatla(tamamlanan_d['net_kar_zarar'].sum() if not tamamlanan_d.empty else 0.0))
    
            st.divider()
            tab_d1, tab_d2 = st.tabs([" Gider Girişi Bekleyenler", " Gideri Tamamlananlar & Geçmiş"])
    
            with tab_d1:
                if not bekleyen_d.empty:
                    dukkan_bekleyen_tablo = []
                    for _, b_row in bekleyen_d.iterrows():
                        dukkan_bekleyen_tablo.append({
                            "Tarih": b_row['tarih'], "Fiş No": b_row['siparis_no'], "Müşteri": b_row['musteri'],
                            "Ürün Adı": b_row['urun_adi'], "Adet": b_row['adet'], "Maliyet": para_formatla(b_row['maliyet']), "Satış Tutarı": para_formatla(b_row['satis_tutari'])
                        })
                    st.dataframe(pd.DataFrame(dukkan_bekleyen_tablo), use_container_width=True, hide_index=True)
    
                    st.divider()
                    dukkan_arama_input = st.text_input(" Gideri Girilecek Satışı Arayın:", placeholder="Fiş No veya Müşteri...", key="dukkan_bekleyen_arama_input").strip()
                    secilen_dukkan_bekleyen_id = None
                    if dukkan_arama_input:
                        filt_d_bekleyen = bekleyen_d[bekleyen_d['siparis_no'].astype(str).str.lower().str.contains(dukkan_arama_input.lower()) | bekleyen_d['musteri'].astype(str).str.lower().str.contains(dukkan_arama_input.lower())]
                        if not filt_d_bekleyen.empty:
                            d_secenekler_dict = {f"Fiş No: {r['siparis_no']} | Müşteri: {r['musteri']}": r['id'] for _, r in filt_d_bekleyen.iterrows()}
                            d_secilen_etiket = st.selectbox("Eşleşen Satışlar Arasından Seçin:", list(d_secenekler_dict.keys()), key="dukkan_bulunan_bekleyen_box")
                            secilen_dukkan_bekleyen_id = d_secenekler_dict[d_secilen_etiket]
    
                    if secilen_dukkan_bekleyen_id:
                        row = bekleyen_d[bekleyen_d['id'] == secilen_dukkan_bekleyen_id].iloc[0]
                        with st.form(key=f"dukkan_form_{row['id']}"):
                            val_dukkan_pos = float(row['pos_kesintisi']) if row['pos_kesintisi'] is not None else 0.0
                            pos_kesintisi = st.number_input("POS Kesintisi (TL - Nakit ise 0)", min_value=0.0, value=val_dukkan_pos, format="%.2f", key=f"dukkan_pos_{row['id']}")
                            if st.form_submit_button(" Hesapla ve Kaydet"):
                                net_kar = row['satis_tutari'] - row['maliyet'] - pos_kesintisi
                                supabase.table("dukkan_elden").update({
                                    "pos_kesintisi": pos_kesintisi, "net_kar_zarar": net_kar, "giderler_girildi": 1
                                }).eq("id", row['id']).execute()
                                st.success(" Dükkan satışı güncellendi!")
                                st.rerun()
                else: st.info(" Bekleyen dükkan satışı yok.")
    
            with tab_d2:
                if not tamamlanan_d.empty:
                    if st.session_state.dukkan_duzenle_id:
                        duzenlenen_duk_res = tamamlanan_d[tamamlanan_d['id'] == st.session_state.dukkan_duzenle_id]
                        if not duzenlenen_duk_res.empty:
                            dd_row = duzenlenen_duk_res.iloc[0]
                            st.info(f" Fiş No: **{dd_row['siparis_no']}** ({dd_row['musteri']}) için dükkan/elden giderini düzenliyorsunuz:")
                            with st.form(key=f"dukkan_duzenle_form_{dd_row['id']}"):
                                dd_pos = st.number_input("POS Kesintisi (TL)", min_value=0.0, value=float(dd_row['pos_kesintisi'] or 0.0), format="%.2f")
                                
                                col_dbtn1, col_dbtn2 = st.columns(2)
                                with col_dbtn1:
                                    if st.form_submit_button(" Dükkan Güncellemeyi Kaydet"):
                                        net_kar_dd = dd_row['satis_tutari'] - dd_row['maliyet'] - dd_pos
                                        supabase.table("dukkan_elden").update({
                                            "pos_kesintisi": dd_pos, 
                                            "net_kar_zarar": net_kar_dd, "giderler_girildi": 1
                                        }).eq("id", dd_row['id']).execute()
                                        st.session_state.dukkan_duzenle_id = None
                                        st.success(" Dükkan gideri güncellendi!")
                                        st.rerun()
                                with col_dbtn2:
                                    if st.form_submit_button(" İptal Et"):
                                        st.session_state.dukkan_duzenle_id = None
                                        st.rerun()
                            st.divider()

                    bd_cols = st.columns([1.1, 1.2, 1.3, 1.8, 0.6, 1.2, 1.4, 1.3, 1.4, 0.8])
                    bd_cols[0].markdown("**Tarih**")
                    bd_cols[1].markdown("**Fiş No**")
                    bd_cols[2].markdown("**Müşteri**")
                    bd_cols[3].markdown("**Ürün Adı**")
                    bd_cols[4].markdown("**Adet**")
                    bd_cols[5].markdown("**Maliyet**")
                    bd_cols[6].markdown("**Satış Tutarı**")
                    bd_cols[7].markdown("**POS Kesintisi**")
                    bd_cols[8].markdown("**Net Kâr**")
                    bd_cols[9].markdown("**İşlem**")
                    st.divider()

                    for _, t_row in tamamlanan_d.iterrows():
                        cols = st.columns([1.1, 1.2, 1.3, 1.8, 0.6, 1.2, 1.4, 1.3, 1.4, 0.8])
                        cols[0].write(t_row['tarih'])
                        cols[1].write(str(t_row['siparis_no']))
                        cols[2].write(str(t_row['musteri']))
                        cols[3].write(str(t_row['urun_adi']))
                        cols[4].write(str(t_row['adet']))
                        cols[5].write(para_formatla(t_row['maliyet']))
                        cols[6].write(para_formatla(t_row['satis_tutari']))
                        cols[7].write(para_formatla(t_row['pos_kesintisi'] or 0))
                        cols[8].write(para_formatla(t_row['net_kar_zarar']))
                        
                        if cols[9].button(" Düzenle", key=f"dukkan_duzenle_btn_{t_row['id']}"):
                            st.session_state.dukkan_duzenle_id = t_row['id']
                            st.rerun()
                else: st.info(" Tamamlanmış dükkan satışı yok.")
        else: st.info(" Dükkan satış kaydı bulunmuyor.")
    
    # --- 7. MÜŞTERİ ANALİZİ ---
    elif menu == " 7. Müşteri Analizi":
        st.header(" Müşteri Analizi, Liderlik Tablosu ve Sipariş Geçmişi Arama")
        s_res = supabase.table("satis").select("*").order("id", desc=True).execute()
        satis_df = pd.DataFrame(s_res.data) if s_res.data else pd.DataFrame()
    
        if not satis_df.empty:
            satis_df['Tutar_Val'] = satis_df['toplam_tutar'].apply(para_metin_to_float)
            m_ozet = satis_df.groupby('musteri').agg(
                Toplam_Siparis=('satis_adet', 'count'),
                Toplam_Adet=('satis_adet', 'sum'),
                Toplam_Harcama=('Tutar_Val', 'sum')
            ).reset_index()
    
            col_mu1, col_mu2, col_mu3 = st.columns(3)
            col_mu1.metric(" Toplam Müşteri Sayısı", f"{len(m_ozet)} Kişi")
            col_mu2.metric(" Toplam Satış Adeti", f"{satis_df['satis_adet'].sum()} Adet")
            col_mu3.metric(" Toplam Müşteri Cirosu", para_formatla(m_ozet['Toplam_Harcama'].sum()))
    
            st.divider()
            
            st.subheader(" Müşteri Sipariş Geçmişi Arama")
            musteri_listesi = sorted(satis_df['musteri'].dropna().unique().tolist())
            secilen_musteri_ara = st.selectbox("Geçmişini Görmek İstediğiniz Müşteriyi Seçin veya Arayın:", ["Seçiniz..."] + musteri_listesi, key="musteri_gecmis_secim")
            
            if secilen_musteri_ara and secilen_musteri_ara != "Seçiniz...":
                mus_satislar = satis_df[satis_df['musteri'] == secilen_musteri_ara].copy()
                st.markdown(f"#### **{secilen_musteri_ara}** Adlı Müşterinin Sipariş Geçmişi")
                
                mus_detay_liste = []
                for _, ms in mus_satislar.iterrows():
                    b_kod = ms.get('barkod_kod')
                    stk_bul_res = supabase.table("stok").select("urun_adi, barkod, urun_kodu").or_(f"barkod.eq.{b_kod},urun_kodu.eq.{b_kod}").limit(1).execute()
                    u_adi = b_kod
                    if stk_bul_res.data:
                        u_adi = stk_bul_res.data[0].get('urun_adi') or b_kod
                        
                    mus_detay_liste.append({
                        "Tarih": ms.get('tarih'),
                        "Sipariş No": ms.get('siparis_no'),
                        "Ürün / Kod": u_adi,
                        "Adet": ms.get('satis_adet'),
                        "Birim Fiyat": para_formatla(para_metin_to_float(ms.get('birim_fiyat'))),
                        "Satış Yeri": ms.get('satilan_yer'),
                        "Toplam Tutar": para_formatla(para_metin_to_float(ms.get('toplam_tutar')))
                    })
                st.dataframe(pd.DataFrame(mus_detay_liste), use_container_width=True, hide_index=True)
            
            st.divider()
            c_lider1, c_lider2 = st.columns(2)
            with c_lider1:
                st.subheader(" En Çok Alışveriş Yapanlar (Ciro)")
                en_cok_harcayanlar = m_ozet.sort_values(by='Toplam_Harcama', ascending=False).head(5).copy()
                en_cok_harcayanlar['Toplam Harcama'] = en_cok_harcayanlar['Toplam_Harcama'].apply(para_formatla)
                st.dataframe(en_cok_harcayanlar.rename(columns={'musteri': 'Müşteri', 'Toplam_Siparis': 'Sipariş', 'Toplam_Adet': 'Adet'})[['Müşteri', 'Sipariş', 'Toplam Harcama']], use_container_width=True, hide_index=True)
            with c_lider2:
                st.subheader(" En Çok Ürün Alanlar (Adet)")
                en_cok_alanlar = m_ozet.sort_values(by='Toplam_Adet', ascending=False).head(5).copy()
                en_cok_alanlar['Toplam Harcama'] = en_cok_alanlar['Toplam_Harcama'].apply(para_formatla)
                st.dataframe(
                    en_cok_alanlar.rename(
                        columns={
                            'musteri': 'Müşteri',
                            'Toplam_Siparis': 'Sipariş',
                            'Toplam_Adet': 'Toplam Adet',
                        }
                    )[['Müşteri', 'Sipariş', 'Toplam Adet', 'Toplam Harcama']],
                    use_container_width=True,
                    hide_index=True,
                )
    
            st.divider()
            st.subheader(" Tüm Müşteriler Genel Özeti")
            m_ozet_full = m_ozet.sort_values(by='Toplam_Harcama', ascending=False).copy()
            m_ozet_full['Toplam Harcama'] = m_ozet_full['Toplam_Harcama'].apply(para_formatla)
            st.dataframe(m_ozet_full.rename(columns={'musteri': 'Müşteri', 'Toplam_Siparis': 'Toplam Sipariş', 'Toplam_Adet': 'Toplam Ürün Adeti'})[['Müşteri', 'Toplam Sipariş', 'Toplam Ürün Adeti', 'Toplam Harcama']], use_container_width=True, hide_index=True)
        else: st.info(" Müşteri verisi bulunmuyor.")
    
    # --- 8. TANIMLAMALAR ---
    elif menu == " 8. Tanımlamalar":
        st.header(" Sistem Tanımlamaları")
        tab1, tab2, tab3 = st.tabs([" Kategori & Marka", " Satış Yeri / Kanal", " Tedarikçi"])
        with tab1:
            with st.form("kategori_form"):
                yeni_kat = st.text_input("Yeni Kategori / Marka Adı")
                if st.form_submit_button(" Kategori Ekle"):
                    if yeni_kat:
                        supabase.table("tanimlar").insert({"tip": "kategori_marka", "deger": yeni_kat.strip().title()}).execute()
                        st.success(" Eklendi!")
                        st.rerun()
            kat_t_res = supabase.table("tanimlar").select("deger").eq("tip", "kategori_marka").order("deger", desc=False).execute()
            st.dataframe(pd.DataFrame(kat_t_res.data).rename(columns={"deger": "Kategori Adı"}) if kat_t_res.data else pd.DataFrame(columns=["Kategori Adı"]), use_container_width=True, hide_index=True)
    
        with tab2:
            with st.form("kanal_form"):
                yeni_yer = st.text_input("Yeni Satış Kanalı Adı")
                if st.form_submit_button(" Kanal Ekle"):
                    if yeni_yer:
                        supabase.table("tanimlar").insert({"tip": "satilan_yer", "deger": yeni_yer.strip().title()}).execute()
                        st.success(" Eklendi!")
                        st.rerun()
            kan_t_res = supabase.table("tanimlar").select("deger").eq("tip", "satilan_yer").order("deger", desc=False).execute()
            st.dataframe(pd.DataFrame(kan_t_res.data).rename(columns={"deger": "Kanal Adı"}) if kan_t_res.data else pd.DataFrame(columns=["Kanal Adı"]), use_container_width=True, hide_index=True)
    
        with tab3:
            with st.form("tedarikci_form"):
                yeni_ted = st.text_input("Yeni Tedarikçi Adı")
                if st.form_submit_button(" Tedarikçi Ekle"):
                    if yeni_ted:
                        supabase.table("tanimlar").insert({"tip": "alinan_yer", "deger": yeni_ted.strip().title()}).execute()
                        st.success(" Eklendi!")
                        st.rerun()
            ted_t_res = supabase.table("tanimlar").select("deger").eq("tip", "alinan_yer").order("deger", desc=False).execute()
            st.dataframe(pd.DataFrame(ted_t_res.data).rename(columns={"deger": "Tedarikçi Adı"}) if ted_t_res.data else pd.DataFrame(columns=["Tedarikçi Adı"]), use_container_width=True, hide_index=True)
    
    # --- 9. RAPORLAR VE ÖZET ---
    elif menu == " 9. Raporlar ve Özet":
        st.header(" Detaylı Finansal Özet ve Analiz Paneli")
        satis_df = pd.DataFrame(supabase.table("satis").select("*").execute().data)
        hb_df = pd.DataFrame(supabase.table("hepsi_burada").select("*").execute().data)
        web_df = pd.DataFrame(supabase.table("web_sitesi").select("*").execute().data)
        dukkan_df = pd.DataFrame(supabase.table("dukkan_elden").select("*").execute().data)

        if not satis_df.empty:
            satis_df['Tutar_Val'] = satis_df['toplam_tutar'].apply(para_metin_to_float)
            toplam_satis_tutar = satis_df['Tutar_Val'].sum()
            
            toplam_hb_kar = hb_df['net_kar_zarar'].sum() if not hb_df.empty and 'net_kar_zarar' in hb_df.columns else 0.0
            toplam_web_kar = web_df['net_kar_zarar'].sum() if not web_df.empty and 'net_kar_zarar' in web_df.columns else 0.0
            toplam_dukkan_kar = dukkan_df['net_kar_zarar'].sum() if not dukkan_df.empty and 'net_kar_zarar' in dukkan_df.columns else 0.0
            genel_net_kar = toplam_hb_kar + toplam_web_kar + toplam_dukkan_kar

            col_r1, col_r2, col_r3 = st.columns(3)
            col_r1.metric(" Toplam Satış Cirosu", para_formatla(toplam_satis_tutar))
            col_r2.metric(" Toplam Sipariş Sayısı", f"{len(satis_df)} Adet")
            col_r3.metric(" Genel Net Kâr", para_formatla(genel_net_kar))

            st.divider()
            st.subheader(" Kanal Bazlı Finansal Özet Tablosu")
             kanal_ozet_data = [
                {"Kanal": "Hepsi Burada", "Sipariş Sayısı": len(hb_df), "Toplam Ciro": para_formatla(hb_df['satis_tutari'].sum() if not hb_df.empty and 'satis_tutari' in hb_df.columns else 0.0), "Net Kâr/Zarar": para_formatla(toplam_hb_kar)},
                {"Kanal": "Web Sitesi", "Sipariş Sayısı": len(web_df), "Toplam Ciro": para_formatla(web_df['satis_tutari'].sum() if not web_df.empty and 'satis_tutari' in web_df.columns else 0.0), "Net Kâr/Zarar": para_formatla(toplam_web_kar)},
                {"Kanal": "Dükkan & Elden", "Sipariş Sayısı": len(dukkan_df), "Toplam Ciro": para_formatla(dukkan_df['satis_tutari'].sum() if not dukkan_df.empty and 'satis_tutari' in dukkan_df.columns else 0.0), "Net Kâr/Zarar": para_formatla(toplam_dukkan_kar)}
            ]
            st.dataframe(pd.DataFrame(kanal_ozet_data), use_container_width=True, hide_index=True)
        else:
            st.info(" Rapor oluşturmak için yeterli satış verisi bulunmuyor.")

    # --- 10. AYLIK DETAYLI RAPORLAR ---
    elif menu == " 10. Aylık Detaylı Raporlar":
        st.header(" Aylık ve Dönemsel Detaylı Raporlar")
        satis_df = pd.DataFrame(supabase.table("satis").select("*").execute().data)
        
        if not satis_df.empty:
            satis_df['tarih_dt'] = pd.to_datetime(satis_df['tarih'], format="%d.%m.%Y", errors='coerce')
            satis_df['Ay_Yil'] = satis_df['tarih_dt'].dt.strftime('%m.%Y')
            
            aylar = sorted(satis_df['Ay_Yil'].dropna().unique().tolist(), reverse=True)
            if aylar:
                secilen_ay = st.selectbox("Rapor İstediğiniz Ay (Ay.Yıl):", aylar)
                filt_ay_df = satis_df[satis_df['Ay_Yil'] == secilen_ay].copy()
                
                filt_ay_df['Tutar_Val'] = filt_ay_df['toplam_tutar'].apply(para_metin_to_float)
                
                col_ay1, col_ay2 = st.columns(2)
                col_ay1.metric(" Seçilen Ay Toplam Satış Adeti", f"{filt_ay_df['satis_adet'].sum()} Adet")
                col_ay2.metric(" Seçilen Ay Toplam Ciro", para_formatla(filt_ay_df['Tutar_Val'].sum()))
                
                st.divider()
                st.subheader(f" {secilen_ay} Dönemi Satış Listesi")
                
                rapor_liste = []
                for _, r in filt_ay_df.iterrows():
                    rapor_liste.append({
                        "Tarih": r.get('tarih'),
                        "Sipariş No": r.get('siparis_no'),
                        "Müşteri": r.get('musteri'),
                        "Barkod/Kod": r.get('barkod_kod'),
                        "Adet": r.get('satis_adet'),
                        "Birim Fiyat": para_formatla(para_metin_to_float(r.get('birim_fiyat'))),
                        "Satış Yeri": r.get('satilan_yer'),
                        "Toplam Tutar": para_formatla(r.get('Tutar_Val'))
                    })
                st.dataframe(pd.DataFrame(rapor_liste), use_container_width=True, hide_index=True)
            else:
                st.info(" Tarih formatına uygun satış kaydı bulunamadı.")
        else:
            st.info(" Detaylı rapor oluşturulacak satış verisi yok.")
