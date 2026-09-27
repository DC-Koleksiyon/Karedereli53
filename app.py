import streamlit as st
from supabase import create_client, Client
import os
from datetime import datetime
import base64
import pandas as pd

st.set_page_config(page_title="Stok & Takip Sistemi", page_icon="", layout="wide")

# --- KULLANICI GİRİŞ KONTROLÜ (RENKLİ & BENİ HATIRLA ÖZELLİKLİ) ---
def check_password():
    st.markdown("""
        <style>
            .stApp {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }
            .login-card {
                background: rgba(255, 255, 255, 0.95);
                padding: 40px;
                border-radius: 20px;
                box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
                backdrop-filter: blur(10px);
                max-width: 450px;
                margin: 0 auto;
            }
            .login-title {
                color: #2d3748;
                font-size: 28px;
                font-weight: 700;
                text-align: center;
                margin-bottom: 10px;
            }
            .login-subtitle {
                color: #718096;
                font-size: 14px;
                text-align: center;
                margin-bottom: 30px;
            }
            .stButton>button {
                width: 100%;
                background: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
                color: #fff;
                font-weight: 700;
                border: none;
                padding: 12px;
                border-radius: 10px;
                box-shadow: 0 4px 15px rgba(253, 160, 133, 0.4);
                transition: all 0.3s ease;
            }
            .stButton>button:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(253, 160, 133, 0.6);
            }
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

    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if not st.session_state["password_correct"]:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="login-card">', unsafe_allow_html=True)
            st.markdown('<p class="login-title">🚀 Stok & Takip Sistemi</p>', unsafe_allow_html=True)
            st.markdown('<p class="login-subtitle">Devam etmek için lütfen giriş yapın</p>', unsafe_allow_html=True)

            saved_user = st.session_state.get("remembered_user", "Sedat-Burak")

            username = st.text_input("Kullanıcı Adı", value=saved_user)
            password = st.text_input("Şifre", type="password")
            remember_me = st.checkbox("Beni Hatırla", value=True)

            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("Giriş Yap"):
                if username == "Sedat-Burak" and password == "Zeus5341":
                    st.session_state["password_correct"] = True
                    if remember_me:
                        st.session_state["remembered_user"] = username
                    else:
                        if "remembered_user" in st.session_state:
                            del st.session_state["remembered_user"]
                    st.success("Giriş başarılı! Yönlendiriliyorsunuz...")
                    st.rerun()
                else:
                    st.error("Kullanıcı adı veya şifre yanlış!")
            st.markdown("</div>", unsafe_allow_html=True)
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
    
    # Güncel Stok ve Stok Geçmişi menüleri yan yana (ardışık) olacak şekilde düzenlendi
    menu_listesi = [
        " 0. Ana Panel", " 1. Ürün Girişi", " 2. Satış İşlemleri", 
        " 3. Güncel Stok", " 4. Stok Geçmişi", " 5. Hepsi Burada", " 6. Web Sitesi",
        " 7. Dükkan & Elden", " 8. Müşteri Analizi", " 9. Tanımlamalar",
        " 10. Raporlar ve Özet", " 11. Aylık Detaylı Raporlar"
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
            if st.button(" 5. Hepsi Burada\n\n Pazaryeri Yönetimi", use_container_width=True, key="card_5"):
                st.session_state.aktif_menu = " 5. Hepsi Burada"
                st.rerun()
    
            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
            if st.button(" 7. Dükkan & Elden\n\n Mağaza Satışları", use_container_width=True, key="card_7"):
                st.session_state.aktif_menu = " 7. Dükkan & Elden"
                st.rerun()
    
            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
            if st.button(" 9. Tanımlamalar\n\n Kategori & Kanallar", use_container_width=True, key="card_9"):
                st.session_state.aktif_menu = " 9. Tanımlamalar"
                st.rerun()
    
            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
            if st.button(" 11. Aylık Detaylı Raporlar\n\n Tarih Aralığı Döküm", use_container_width=True, key="card_11"):
                st.session_state.aktif_menu = " 11. Aylık Detaylı Raporlar"
                st.rerun()
    
        with col_b:
            if st.button(" 2. Satış İşlemleri\n\n FIFO & Satış", use_container_width=True, key="card_2"):
                st.session_state.aktif_menu = " 2. Satış İşlemleri"
                st.rerun()
    
            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
            if st.button(" 4. Stok Geçmişi\n\n Ürün Hareketleri", use_container_width=True, key="card_4"):
                st.session_state.aktif_menu = " 4. Stok Geçmişi"
                st.rerun()
    
            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
            if st.button(" 6. Web Sitesi\n\n E-Ticaret Satışları", use_container_width=True, key="card_6"):
                st.session_state.aktif_menu = " 6. Web Sitesi"
                st.rerun()
    
            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
            if st.button(" 8. Müşteri Analizi\n\n Müşteri Liderlik", use_container_width=True, key="card_8"):
                st.session_state.aktif_menu = " 8. Müşteri Analizi"
                st.rerun()
    
            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
            if st.button(" 10. Raporlar ve Özet\n\n Detaylı Finansal Özet", use_container_width=True, key="card_10"):
                st.session_state.aktif_menu = " 10. Raporlar ve Özet"
                st.rerun()
    
    # --- 1. ÜRÜN GİRİŞİ ---
    elif menu == " 1. Ürün Girişi":
        st.header(" Ürün Girişi ve Mal Kabul Yönetimi")
        
        kat_res = supabase.table("tanimlar").select("deger").eq("tip", "kategori_marka").order("deger", desc=False).execute()
        kategori_marka_listesi = [row["deger"] for row in kat_res.data] if kat_res.data else []
        
        yer_res = supabase.table("tanimlar").select("deger").eq("tip", "alinan_yer").order("deger", desc=False).execute()
        alinan_yer_listesi = [row["deger"] for row in yer_res.data] if yer_res.data else []
        
        if not kategori_marka_listesi: kategori_marka_listesi = ["Önce Tanımlamalardan Ekle"]
        if not alinan_yer_listesi: alinan_yer_listesi = ["Önce Tanımlamalardan Ekle"]

        if "duzenlenen_kod" not in st.session_state: st.session_state.duzenlenen_kod = None

        if st.session_state.duzenlenen_kod:
            st.info(f" Şu an Ürün Kodu: **{st.session_state.duzenlenen_kod}** olan ürün güncelleniyor modunda.")
            if st.button(" Düzenlemeyi İptal Et"):
                st.session_state.duzenlenen_kod = None
                st.rerun()
            
            kayit_res = supabase.table("stok").select("*").eq("urun_kodu", st.session_state.duzenlenen_kod).order("id", desc=True).limit(1).execute()
            if kayit_res.data:
                k_item = kayit_res.data[0]
                with st.form("duzenleme_formu"):
                    d_barkod = st.text_input("Ürün Barkodu *", value=k_item.get("barkod") or "")
                    d_kod = st.text_input("Ürün Kodu *", value=k_item.get("urun_kodu") or "")
                    d_ad = st.text_input("Ürün Adı *", value=k_item.get("urun_adi") or "")
                    d_tarih = st.text_input("Giriş Tarihi (GG.AA.YYYY) *", value=k_item.get("tarih") or datetime.now().strftime("%d.%m.%Y"))
                    
                    kat_idx = kategori_marka_listesi.index(k_item.get("kategori_marka")) if k_item.get("kategori_marka") in kategori_marka_listesi else 0
                    d_kat = st.selectbox("Kategori & Marka *", kategori_marka_listesi, index=kat_idx)
                    
                    yer_idx = alinan_yer_listesi.index(k_item.get("alinan_yer")) if k_item.get("alinan_yer") in alinan_yer_listesi else 0
                    d_yer = st.selectbox("Alınan Yer / Tedarikçi *", alinan_yer_listesi, index=yer_idx)
                    
                    d_adet = st.number_input("Adet *", min_value=1, value=int(k_item.get("adet") or 1))
                    
                    eski_top_mal = para_metin_to_float(k_item.get("toplam_maliyet"))
                    eski_birim = eski_top_mal / int(k_item.get("adet") or 1) if int(k_item.get("adet") or 1) > 0 else 0.0
                    d_birim_fiyat = st.number_input("Birim Maliyet Fiyatı (TL) *", min_value=0.0, value=float(eski_birim), format="%.2f")
                    
                    if st.form_submit_button("Güncellemeyi Kaydet"):
                        if not d_barkod or not d_kod or not d_ad or d_birim_fiyat <= 0:
                            st.error("Lütfen tüm zorunlu alanları eksiksiz doldurun.")
                        else:
                            yeni_top_mal = d_birim_fiyat * d_adet
                            supabase.table("stok").update({
                                "barkod": d_barkod.strip(),
                                "urun_kodu": d_kod.strip(),
                                "urun_adi": d_ad.strip().title(),
                                "tarih": d_tarih.strip(),
                                "kategori_marka": d_kat,
                                "alinan_yer": d_yer,
                                "adet": d_adet,
                                "toplam_maliyet": para_formatla(yeni_top_mal)
                            }).eq("id", k_item.get("id")).execute()
                            st.success("Ürün başarıyla güncellendi!")
                            st.session_state.duzenlenen_kod = None
                            st.rerun()
        else:
            tab_yeni, tab_stok_ekle = st.tabs(["✨ 1. Sıfırdan Yeni Ürün Ekle", "📦 2. Kayıtlı Ürüne Mal Kabul / Stok Ekle"])
            
            with tab_yeni:
                st.subheader("Yeni Ürün Tanımlama ve İlk Giriş")
                with st.form("yeni_urun_form"):
                    col_ny1, col_ny2 = st.columns(2)
                    with col_ny1:
                        y_barkod = st.text_input("Ürün Barkodu * (Okuyucu Uyumlu)")
                        y_tarih = st.text_input("Giriş Tarihi (GG.AA.YYYY) *", value=datetime.now().strftime("%d.%m.%Y"))
                        y_kat = st.selectbox("Kategori & Marka Seçimi *", kategori_marka_listesi, key="y_kat_box")
                        y_adet = st.number_input("Ürün Adeti *", min_value=1, value=1, key="y_adet_num")
                    with col_ny2:
                        y_kod = st.text_input("Ürün Kodu *")
                        y_ad = st.text_input("Ürün Adı *")
                        y_yer = st.selectbox("Ürünün Alındığı Yer / Tedarikçi *", alinan_yer_listesi, key="y_yer_box")
                        y_birim_fiyat = st.number_input("Birim Maliyet Fiyatı (TL) *", min_value=0.0, format="%.2f", key="y_fiyat_num")
                        y_kdv = st.selectbox("KDV Durumu *", ["KDV'li", "KDV'siz"], key="y_kdv_box")
                    
                    y_dosya = st.file_uploader("Ürün Görseli Yükle (Opsiyonel)", type=["png", "jpg", "jpeg"], key="y_img_upl")
                    
                    if st.form_submit_button("Yeni Ürünü Kaydet"):
                        clean_barkod = y_barkod.strip()
                        clean_kod = y_kod.strip()
                        clean_ad = y_ad.strip().title()
                        
                        if not clean_barkod or not clean_kod or not clean_ad or y_birim_fiyat <= 0:
                            st.error("Lütfen zorunlu alanları eksiksiz doldurun!")
                        else:
                            kdvli_birim = y_birim_fiyat * 1.20 if y_kdv == "KDV'siz" else y_birim_fiyat
                            toplam_mal = kdvli_birim * y_adet
                            
                            r_yolu = ""
                            if y_dosya:
                                os.makedirs("uploads", exist_ok=True)
                                r_yolu = os.path.join("uploads", y_dosya.name)
                                with open(r_yolu, "wb") as f: f.write(y_dosya.getbuffer())
                                
                            supabase.table("stok").insert({
                                "tarih": y_tarih.strip(),
                                "urun_kodu": clean_kod,
                                "urun_adi": clean_ad,
                                "adet": int(y_adet),
                                "alinan_yer": y_yer,
                                "toplam_maliyet": para_formatla(toplam_mal),
                                "resim_yolu": r_yolu,
                                "kategori_marka": y_kat,
                                "barkod": clean_barkod
                            }).execute()
                            st.success("Yeni ürün başarıyla eklendi!")
                            st.rerun()

            with tab_stok_ekle:
                st.subheader("Daha Önce Kayıtlı Ürüne Ek Mal Kabul / Stok Girişi")
                st.write("Aşağıdaki arama kutusuna ürün adı, kodu veya barkod yazarak ürünü hızlıca bulabilirsiniz.")
                
                stk_tum_res = supabase.table("stok").select("urun_kodu, barkod, urun_adi, kategori_marka, resim_yolu").execute()
                kayitli_urunler = stk_tum_res.data if stk_tum_res.data else []
                
                if kayitli_urunler:
                    mal_kabul_arama = st.text_input("🔍 Ürün Arama (İsim, Kod veya Barkod):", placeholder="Örn: Mini GT, KOD123 veya Barkod...", key="mal_kabul_arama_input").strip().lower()
                    
                    filtrelenmis_urunler = []
                    gorulen_benzersiz = set()
                    for u in kayitli_urunler:
                        k = str(u.get("urun_kodu") or "").strip()
                        b = str(u.get("barkod") or "").strip()
                        ad = str(u.get("urun_adi") or "").strip()
                        kat = str(u.get("kategori_marka") or "").strip()
                        
                        benzersiz_anahtar = k if k else b
                        if benzersiz_anahtar in gorulen_benzersiz:
                            continue
                        
                        birlesik_metin = f"{ad} {k} {b} {kat}".lower()
                        if not mal_kabul_arama or mal_kabul_arama in birlesik_metin:
                            gorulen_benzersiz.add(benzersiz_anahtar)
                            filtrelenmis_urunler.append(u)
                    
                    if filtrelenmis_urunler:
                        urun_secenek_dict = {}
                        for u in filtrelenmis_urunler:
                            k = u.get("urun_kodu") or "-"
                            b = u.get("barkod") or "-"
                            ad = u.get("urun_adi") or "-"
                            etiket = f"{ad} | Kod: {k} | Barkod: {b}"
                            urun_secenek_dict[etiket] = u
                            
                        secilen_etiket = st.selectbox("Eşleşen Ürünler Arasından Seçin:", list(urun_secenek_dict.keys()), key="stok_ekle_secim_box")
                        secilen_veri = urun_secenek_dict[secilen_etiket]
                        
                        with st.form("mevcut_urun_stok_ekle_form"):
                            st.markdown(f"**Seçilen Ürün:** {secilen_veri.get('urun_adi')}")
                            st.markdown(f"**Mevcut Kod:** `{secilen_veri.get('urun_kodu')}` | **Barkod:** `{secilen_veri.get('barkod')}` | **Kategori:** `{secilen_veri.get('kategori_marka')}`")
                            
                            col_ek1, col_ek2 = st.columns(2)
                            with col_ek1:
                                ek_tarih = st.text_input("Giriş Tarihi (GG.AA.YYYY) *", value=datetime.now().strftime("%d.%m.%Y"))
                                ek_adet = st.number_input("Eklenecek Adet *", min_value=1, value=1)
                            with col_ek2:
                                ek_yer = st.selectbox("Tedarikçi / Alınan Yer *", alinan_yer_listesi, key="ek_yer_box")
                                ek_birim_fiyat = st.number_input("Birim Maliyet Fiyatı (TL) *", min_value=0.0, format="%.2f")
                                ek_kdv = st.selectbox("KDV Durumu *", ["KDV'li", "KDV'siz"], key="ek_kdv_box")
                                
                            if st.form_submit_button("Stok Girişini Tamamla"):
                                if ek_birim_fiyat <= 0 or ek_adet <= 0:
                                    st.error("Lütfen adet and birim fiyat giriniz.")
                                else:
                                    kdvli_b = ek_birim_fiyat * 1.20 if ek_kdv == "KDV'siz" else ek_birim_fiyat
                                    toplam_mal_ek = kdvli_b * ek_adet
                                    
                                    supabase.table("stok").insert({
                                        "tarih": ek_tarih.strip(),
                                        "urun_kodu": secilen_veri.get("urun_kodu"),
                                        "urun_adi": secilen_veri.get("urun_adi"),
                                        "adet": int(ek_adet),
                                        "alinan_yer": ek_yer,
                                        "toplam_maliyet": para_formatla(toplam_mal_ek),
                                        "resim_yolu": secilen_veri.get("resim_yolu", ""),
                                        "kategori_marka": secilen_veri.get("kategori_marka"),
                                        "barkod": secilen_veri.get("barkod")
                                    }).execute()
                                    st.success("Ürüne ek stok girişi başarıyla yapıldı!")
                                    st.rerun()
                    else:
                        st.warning("Aradığınız kriterlere uygun kayıtlı ürün bulunamadı.")
                else:
                    st.info("Sistemde kayıtlı ürün bulunmuyor. Önce 'Yeni Ürün Ekle' sekmesinden ürün tanımlamalısınız.")

    
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
                    st.session_state.duzenlenen_kod = secilen_islem_kod
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
    
    # --- 2. SATIŞ İŞLEMLERİ (FIFO MALIYET MANTIĞI İLE) ---
    elif menu == " 2. Satış İşlemleri":
        st.header(" Satış İşlemleri (FIFO / İlk Giren İlk Çıkar)")
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
            
        buton_satis_metni = " Satışı Güncelle" if st.session_state.satis_duzenle_id else " Satışı Gerçekleştir ve Kaydet (FIFO)"
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
                            basari_mesaji = " Satış FIFO mantığıyla başarıyla güncellendi!"
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
                            basari_mesaji = " Satış FIFO maliyet hesaplamasıyla gerçekleştirildi!"
    
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
        st.header(" Güncel Kalan Stok ve FIFO Maliyet Özeti")
        
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
            
            kalan_satis_dusu = toplam_satis_adet
            kalan_toplam_adet = 0
            kalan_toplam_maliyet = 0.0
            
            for p in partiler:
                p_adet = p.get('adet', 0)
                p_toplam_mal = para_metin_to_float(p.get('toplam_maliyet'))
                p_birim_mal = p_toplam_mal / p_adet if p_adet > 0 else 0.0
                
                if kalan_satis_dusu >= p_adet:
                    kalan_satis_dusu -= p_adet
                else:
                    bu_partide_kalan = p_adet - kalan_satis_dusu
                    kalan_satis_dusu = 0
                    kalan_toplam_adet += bu_partide_kalan
                    kalan_toplam_maliyet += bu_partide_kalan * p_birim_mal
            
            if kalan_toplam_adet <= 0:
                continue

            ortalama_birim_maliyet = kalan_toplam_maliyet / kalan_toplam_adet if kalan_toplam_adet > 0 else 0.0
            toplam_bagli_sermaye += kalan_toplam_maliyet
            
            en_eski_gun = 0
            ilk_parti = partiler[0]
            barkod = ilk_parti.get('barkod') or ""
            kod = ilk_parti.get('urun_kodu') or ""
            ad = ilk_parti.get('urun_adi')
            kategori = ilk_parti.get('kategori_marka') or "-"
            alinan_yer = ilk_parti.get('alinan_yer') or "-"
            
            try:
                g_tarih = datetime.strptime(ilk_parti.get('tarih', '').strip(), "%d.%m.%Y")
                en_eski_gun = max(0, (bugun - g_tarih).days)
            except: pass
    
            durum = " Kritik / Azalıyor" if kalan_toplam_adet <= kritik_esik else " Normal"
    
            if secilen_kategori_filtre != "Tümü" and kategori != secilen_kategori_filtre: continue
            arama_metni_birlesik = f"{ad} {kod} {barkod} {kategori} {alinan_yer}".lower()
            if stok_arama and stok_arama not in arama_metni_birlesik: continue
    
            islenmis_stoklar.append({
                "Ürün Adı": ad,
                "Kategori": kategori,
                "Alınan Yer": alinan_yer,
                "Kod": kod.strip() if kod else "-",
                "Barkod": barkod.strip() if barkod else "-",
                "Rafta Gün": en_eski_gun,
                "Kalan Adet": kalan_toplam_adet,
                "Birim Maliyet": para_formatla(ortalama_birim_maliyet),
                "Birim_Mal_Val": ortalama_birim_maliyet,
                "Sermaye_Val": kalan_toplam_maliyet,
                "Toplam Maliyet": para_formatla(kalan_toplam_maliyet),
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
            col_stk3.metric(" Kritik Ürün Sayısı", f"{kritik_sayisi} Çeşit")
            
            if secilen_kategori_filtre != "Tümü":
                filtrelenmis_toplam_adet = df_stok_liste['Kalan Adet'].sum()
                filtrelenmis_toplam_maliyet = df_stok_liste['Sermaye_Val'].sum()
                st.info(f" Seçilen **{secilen_kategori_filtre}** markası için toplam kalan adet: **{filtrelenmis_toplam_adet} Adet** | Toplam Maliyet: **{para_formatla(filtrelenmis_toplam_maliyet)}**")
    
            st.divider()
            st.dataframe(df_stok_liste[["Durum", "Ürün Adı", "Kategori", "Alınan Yer", "Kod", "Barkod", "Rafta Gün", "Kalan Adet", "Birim Maliyet", "Toplam Maliyet"]], use_container_width=True, hide_index=True)
        else:
            st.info(" Aradığınız kriterlere uygun güncel ve aktif stok bulunamadı.")
    
    # --- 4. STOK GEÇMİŞİ (Güncel Stok ile Yan Yana Segment) ---
    elif menu == " 4. Stok Geçmişi":
        st.header(" Ürün Bazlı Stok Hareket ve Satış Geçmişi")
        st.write("Bu bölümde seçtiğiniz bir ürünün hangi tarihte, kime, kaça alınıp kaça satıldığını ve tüm detaylı geçmişini inceleyebilirsiniz.")
        
        stok_Tum_res = supabase.table("stok").select("urun_kodu, barkod, urun_adi").execute()
        stok_kayitlari_tum = stok_Tum_res.data if stok_Tum_res.data else []
        
        if stok_kayitlari_tum:
            urun_secenek_dict = {}
            for st_item in stok_kayitlari_tum:
                u_kod = st_item.get("urun_kodu") or "-"
                u_barkod = st_item.get("barkod") or "-"
                u_ad = st_item.get("urun_adi") or "-"
                etiket = f"{u_ad} | Kod: {u_kod} | Barkod: {u_barkod}"
                urun_secenek_dict[etiket] = (u_kod, u_barkod)
                
            secilen_gecmis_urun = st.selectbox("Geçmişini İncelemek İstediğiniz Ürünü Seçin:", list(urun_secenek_dict.keys()), key="stok_gecmis_secim_box")
            
            if secilen_gecmis_urun:
                secilen_kod, secilen_barkod = urun_secenek_dict[secilen_gecmis_urun]
                
                st.divider()
                st.subheader(" Ürün Mal Kabul / Giriş Geçmişi")
                giris_gecmis_res = supabase.table("stok").select("*").or_(f"urun_kodu.eq.{secilen_kod},barkod.eq.{secilen_barkod}").order("id", desc=True).execute()
                giris_gecmis_data = giris_gecmis_res.data if giris_gecmis_res.data else []
                
                if giris_gecmis_data:
                    g_liste = []
                    for g in giris_gecmis_data:
                        g_adet = g.get("adet", 0)
                        g_top_mal = para_metin_to_float(g.get("toplam_maliyet"))
                        g_birim_mal = g_top_mal / g_adet if g_adet > 0 else 0.0
                        g_liste.append({
                            "Giriş Tarihi": g.get("tarih"),
                            "Tedarikçi": g.get("alinan_yer"),
                            "Kategori": g.get("kategori_marka"),
                            "Giriş Adeti": g_adet,
                            "Adet Başı Maliyet": para_formatla(g_birim_mal),
                            "Toplam Maliyet": para_formatla(g_top_mal)
                        })
                    st.dataframe(pd.DataFrame(g_liste), use_container_width=True, hide_index=True)
                else:
                    st.info("Bu ürüne ait mal kabul (giriş) kaydı bulunamadı.")
                
                st.divider()
                st.subheader(" Ürün Satış Geçmişi")
                satis_gecmis_res = supabase.table("satis").select("*").or_(f"barkod_kod.eq.{secilen_kod},barkod_kod.eq.{secilen_barkod}").order("id", desc=True).execute()
                satis_gecmis_data = satis_gecmis_res.data if satis_gecmis_res.data else []
                
                if satis_gecmis_data:
                    s_liste = []
                    for s in satis_gecmis_data:
                        s_adet = s.get("satis_adet", 0)
                        s_birim_fiyat = para_metin_to_float(s.get("birim_fiyat"))
                        s_top_tutar = para_metin_to_float(s.get("toplam_tutar"))
                        s_liste.append({
                            "Satış Tarihi": s.get("tarih"),
                            "Sipariş No": s.get("siparis_no"),
                            "Müşteri": s.get("musteri"),
                            "Satış Kanalı": s.get("satilan_yer"),
                            "Satış Adeti": s_adet,
                            "Birim Satış Fiyatı": para_formatla(s_birim_fiyat),
                            "Toplam Satış Tutarı": para_formatla(s_top_tutar)
                        })
                    st.dataframe(pd.DataFrame(s_liste), use_container_width=True, hide_index=True)
                else:
                    st.info("Bu ürüne ait satış kaydı bulunamadı.")
        else:
            st.info("Sistemde kayıtlı ürün bulunmuyor.")

    # --- 5. HEPSİ BURADA ---
    elif menu == " 5. Hepsi Burada":
        st.header(" Hepsi Burada Finans and Kar/Zarar Yönetimi")
        
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
    
    # --- 6. WEB SİTESİ ---
    elif menu == " 6. Web Sitesi":
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
    
    # --- 7. DÜKKAN & ELDEN ---
    elif menu == " 7. Dükkan & Elden":
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
    
    # --- 8. MÜŞTERİ ANALİZİ ---
    elif menu == " 8. Müşteri Analizi":
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
    
    # --- 9. TANIMLAMALAR ---
    elif menu == " 9. Tanımlamalar":
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
    
    # --- 10. RAPORLAR VE ÖZET ---
    elif menu == " 10. Raporlar ve Özet":
        st.header(" Detaylı Finansal Özet, Kârlılık ve Analiz Paneli")
        satis_df = pd.DataFrame(supabase.table("satis").select("*").execute().data)
        stok_df = pd.DataFrame(supabase.table("stok").select("*").execute().data)
        hb_df = pd.DataFrame(supabase.table("hepsi_burada").select("*").execute().data)
        web_df = pd.DataFrame(supabase.table("web_sitesi").select("*").execute().data)
        dukkan_df = pd.DataFrame(supabase.table("dukkan_elden").select("*").execute().data)
    
        if not satis_df.empty:
            satis_df['Tutar_Val'] = satis_df['toplam_tutar'].apply(para_metin_to_float)
            toplam_siparis = len(satis_df)
            toplam_satis_adet = satis_df['satis_adet'].sum()
            toplam_genel_ciro = satis_df['Tutar_Val'].sum()
            
            hb_tamam = hb_df[hb_df['giderler_girildi'] == 1] if not hb_df.empty else pd.DataFrame()
            web_tamam = web_df[web_df['giderler_girildi'] == 1] if not web_df.empty else pd.DataFrame()
            dukkan_tamam = dukkan_df[dukkan_df['giderler_girildi'] == 1] if not dukkan_df.empty else pd.DataFrame()
    
            hb_net = hb_tamam['net_kar_zarar'].sum() if not hb_tamam.empty else 0.0
            web_net = web_tamam['net_kar_zarar'].sum() if not web_tamam.empty else 0.0
            dukkan_net = dukkan_tamam['net_kar_zarar'].sum() if not dukkan_tamam.empty else 0.0
            toplam_net_kar = hb_net + web_net + dukkan_net
    
            col_r1, col_r2, col_r3, col_r4 = st.columns(4)
            col_r1.metric(" Toplam Sipariş", f"{toplam_siparis} Adet")
            col_r2.metric(" Satılan Ürün Adeti", f"{toplam_satis_adet} Adet")
            col_r3.metric(" Toplam Brüt Ciro", para_formatla(toplam_genel_ciro))
            col_r4.metric(" Toplam Net Kâr", para_formatla(toplam_net_kar))
    
            st.divider()
            st.subheader(" Satış Kanallarına Göre Performans ve Ciro Dağılımı")
            kanal_ozet = satis_df.groupby('satilan_yer').agg(
                Siparis_Sayisi=('satis_adet', 'count'),
                Toplam_Adet=('satis_adet', 'sum'),
                Toplam_Ciro=('Tutar_Val', 'sum')
            ).reset_index().sort_values(by='Toplam_Ciro', ascending=False)
            kanal_ozet['Toplam Ciro'] = kanal_ozet['Toplam_Ciro'].apply(para_formatla)
            st.dataframe(kanal_ozet.rename(columns={'satilan_yer': 'Satış Kanalı', 'Siparis_Sayisi': 'Sipariş Adedi', 'Toplam_Adet': 'Satılan Adet'})[['Satış Kanalı', 'Sipariş Adedi', 'Satılan Adet', 'Toplam Ciro']], use_container_width=True, hide_index=True)
    
            st.divider()
            st.subheader(" En Çok Satan Ürünler (Adet) ve En Çok Ciro Getiren Ürünler")
            
            if not stok_df.empty:
                stok_map_ad = {}
                stok_map_kat = {}
                for _, sr in stok_df.iterrows():
                    b = str(sr.get('barkod')).strip().lower()
                    k = str(sr.get('urun_kodu')).strip().lower()
                    ad = sr.get('urun_adi')
                    kat = sr.get('kategori_marka') or "-"
                    if b:
                        stok_map_ad[b] = ad
                        stok_map_kat[b] = kat
                    if k:
                        stok_map_ad[k] = ad
                        stok_map_kat[k] = kat
                
                satis_df['Urun_Adi_Genel'] = satis_df['barkod_kod'].apply(lambda x: stok_map_ad.get(str(x).strip().lower(), str(x)))
                satis_df['Kategori_Genel'] = satis_df['barkod_kod'].apply(lambda x: stok_map_kat.get(str(x).strip().lower(), "-"))
                
                urun_bazli = satis_df.groupby(['Urun_Adi_Genel', 'Kategori_Genel']).agg(
                    Toplam_Adet=('satis_adet', 'sum'),
                    Toplam_Ciro=('Tutar_Val', 'sum')
                ).reset_index()
    
                col_u1, col_u2 = st.columns(2)
                with col_u1:
                    st.markdown("#####  En Çok Satan Ürünler (Adet)")
                    en_cok_satanlar = urun_bazli.sort_values(by='Toplam_Adet', ascending=False).head(5).copy()
                    en_cok_satanlar['Toplam Ciro'] = en_cok_satanlar['Toplam_Ciro'].apply(para_formatla)
                    st.dataframe(en_cok_satanlar.rename(columns={'Urun_Adi_Genel': 'Ürün Adı', 'Kategori_Genel': 'Kategori', 'Toplam_Adet': 'Satılan Adet'})[['Ürün Adı', 'Kategori', 'Satılan Adet', 'Toplam Ciro']], use_container_width=True, hide_index=True)
    
                with col_u2:
                    st.markdown("#####  En Çok Ciro Getiren Ürünler")
                    en_cok_ciro_getirenler = urun_bazli.sort_values(by='Toplam_Ciro', ascending=False).head(5).copy()
                    en_cok_ciro_getirenler['Toplam Ciro'] = en_cok_ciro_getirenler['Toplam_Ciro'].apply(para_formatla)
                    st.dataframe(en_cok_ciro_getirenler.rename(columns={'Urun_Adi_Genel': 'Ürün Adı', 'Kategori_Genel': 'Kategori', 'Toplam_Adet': 'Satılan Adet'})[['Ürün Adı', 'Kategori', 'Satılan Adet', 'Toplam Ciro']], use_container_width=True, hide_index=True)
    
                st.divider()
                st.subheader(" Kategori / Marka Bazlı Satış Performansı")
                kat_bazli = satis_df.groupby('Kategori_Genel').agg(
                    Siparis_Sayisi=('satis_adet', 'count'),
                    Toplam_Adet=('satis_adet', 'sum'),
                    Toplam_Ciro=('Tutar_Val', 'sum')
                ).reset_index().sort_values(by='Toplam_Ciro', ascending=False)
                kat_bazli['Toplam Ciro'] = kat_bazli['Toplam_Ciro'].apply(para_formatla)
                st.dataframe(kat_bazli.rename(columns={'Kategori_Genel': 'Kategori / Marka', 'Siparis_Sayisi': 'Sipariş Adedi', 'Toplam_Adet': 'Satılan Ürün Adeti'})[['Kategori / Marka', 'Sipariş Adedi', 'Satılan Ürün Adeti', 'Toplam Ciro']], use_container_width=True, hide_index=True)
        else:
            st.info(" Rapor oluşturmak için henüz satış verisi bulunmuyor.")

    # --- 11. AYLIK DETAYLI RAPORLAR ---
    elif menu == " 11. Aylık Detaylı Raporlar":
        st.header(" Aylık Detaylı Raporlar ve Satır Satır Döküm")
        st.write("Bu bölümde, yapılan satışların ve tamamlanan giderlerin aylık bazda kırılımını; satış adeti, satış cirosu, maliyet ve net kâr/zarar olarak inceleyebilirsiniz.")
        
        satis_res = supabase.table("satis").select("*").execute()
        satis_verileri = satis_res.data if satis_res.data else []
        
        hb_res = supabase.table("hepsi_burada").select("*").execute()
        web_res = supabase.table("web_sitesi").select("*").execute()
        dukkan_res = supabase.table("dukkan_elden").select("*").execute()
        
        maliyet_sozlugu = {}
        for kanal_list in [hb_res.data, web_res.data, dukkan_res.data]:
            if kanal_list:
                for k_item in kanal_list:
                    s_no = str(k_item.get("siparis_no")).strip()
                    maliyet_degeri = float(k_item.get("maliyet") or 0.0)
                    net_kar_degeri = float(k_item.get("net_kar_zarar") or 0.0)
                    maliyet_sozlugu[s_no] = {
                        "maliyet": maliyet_degeri,
                        "net_kar": net_kar_degeri
                    }

        if satis_verileri:
            aylik_liste = []
            for s in satis_verileri:
                tarih_str = s.get("tarih")
                dt = pd.to_datetime(tarih_str, format="%d.%m.%Y", errors='coerce')
                if pd.notnull(dt):
                    yil_ay = dt.strftime("%Y-%m")
                    Ay_Adi = dt.strftime("%B %Y")
                else:
                    yil_ay = "Bilinmeyen"
                    Ay_Adi = "Bilinmeyen"
                
                s_no = str(s.get("siparis_no")).strip()
                satis_adet = int(s.get("satis_adet") or 0)
                satis_ciro = para_metin_to_float(s.get("toplam_tutar"))
                
                mal_bilgi = maliyet_sozlugu.get(s_no, {"maliyet": 0.0, "net_kar": 0.0})
                mal_tutar = mal_bilgi["maliyet"]
                kar_zarar = satis_ciro - mal_tutar
                if mal_bilgi["net_kar"] != 0.0:
                    kar_zarar = mal_bilgi["net_kar"]

                aylik_liste.append({
                    "Yil_Ay": yil_ay,
                    "Ay": Ay_Adi,
                    "Tarih": tarih_str,
                    "Sipariş No": s_no,
                    "Müşteri": s.get("musteri"),
                    "Satış Yeri": s.get("satilan_yer"),
                    "Satış Adeti": satis_adet,
                    "Satış Cirosu": satis_ciro,
                    "Malın Maliyeti": mal_tutar,
                    "Kâr / Zarar": kar_zarar
                })
            
            df_aylik_ham = pd.DataFrame(aylik_liste)
            
            if not df_aylik_ham.empty:
                st.subheader(" Ay Bazında Genel Özet Tablosu")
                df_grup_ay = df_aylik_ham.groupby(["Yil_Ay", "Ay"]).agg(
                    Toplam_Siparis=('Sipariş No', 'count'),
                    Toplam_Adet=('Satış Adeti', 'sum'),
                    Toplam_Ciro=('Satış Cirosu', 'sum'),
                    Toplam_Maliyet=('Malın Maliyeti', 'sum'),
                    Toplam_Kar=('Kâr / Zarar', 'sum')
                ).reset_index().sort_values(by="Yil_Ay", ascending=False)
                
                df_grup_ay["Satış Cirosu"] = df_grup_ay["Toplam_Ciro"].apply(para_formatla)
                df_grup_ay["Toplam Maliyet"] = df_grup_ay["Toplam_Maliyet"].apply(para_formatla)
                df_grup_ay["Net Kâr / Zarar"] = df_grup_ay["Toplam_Kar"].apply(para_formatla)
                
                goster_grup_df = df_grup_ay[["Ay", "Toplam_Siparis", "Toplam_Adet", "Satış Cirosu", "Toplam Maliyet", "Net Kâr / Zarar"]]
                st.dataframe(goster_grup_df.rename(columns={"Ay": "Dönem (Ay)", "Toplam_Siparis": "Sipariş Sayısı", "Toplam_Adet": "Satılan Adet"}), use_container_width=True, hide_index=True)
                
                st.divider()
                st.subheader(" Seçilen Aya Ait Satır Satır Detaylı Rapor")
                secilen_donem = st.selectbox("İncelemek İstediğiniz Ayı Seçin:", df_grup_ay["Ay"].tolist())
                
                df_secilen_ay = df_aylik_ham[df_aylik_ham["Ay"] == secilen_donem].copy()
                
                df_secilen_ay["Satış Cirosu"] = df_secilen_ay["Satış Cirosu"].apply(para_formatla)
                df_secilen_ay["Malın Maliyeti"] = df_secilen_ay["Malın Maliyeti"].apply(para_formatla)
                df_secilen_ay["Kâr / Zarar"] = df_secilen_ay["Kâr / Zarar"].apply(para_formatla)
                
                st.dataframe(df_secilen_ay[["Tarih", "Sipariş No", "Müşteri", "Satış Yeri", "Satış Adeti", "Satış Cirosu", "Malın Maliyeti", "Kâr / Zarar"]], use_container_width=True, hide_index=True)
            else:
                st.info("Aylık rapor oluşturulacak veri bulunamadı.")
        else:
            st.info("Henüz sisteme işlenmiş satış verisi bulunmuyor.")
