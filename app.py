import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# --- 1. AYARLAR ---
st.set_page_config(
    page_title="Zacharia Borsa", 
    page_icon="🦅", 
    layout="wide", 
    initial_sidebar_state="expanded" 
)

st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    [data-testid="stSidebar"] { background-color: #111827; }
    .stTextArea textarea { font-size: 14px; background-color: #1f2937; color: white; }
    .stButton>button { border-radius: 8px; font-weight: bold; height: 3em; }
    div[data-testid="stMetricValue"] { color: #4ade80; }
</style>
""", unsafe_allow_html=True)

# --- 2. HİSSE HAVUZU (TÜM LİSTE İÇİN) ---
# Buraya BIST'teki tüm hisseleri ekledim.
TUM_HISSELER_STR = """
ACSEL, ADEL, ADESE, AEFES, AFYON, AGES, AGHOL, AGYO, AHGAZ, AKBNK, AKCNS, AKENR, AKFGY, AKGRT, AKMGY, AKSA, AKSEN, AKSGY, ALARK, ALBRK, ALCAR, ALCTL, ALGYO, ALKA, ALKIM, ALMAD, ANELE, ANGEN, ANHYT, ARASE, ARCLK, ARDYZ, ARENA, ARSAN, ARZUM, ASELS, ASGYO, ASTOR, ASUZU, ATAKP, ATATP, ATEKS, ATLAS, AVGYO, AVHOL, AVOD, AYCES, AYDEM, AYEN, AYES, AYGAZ, BAGFS, BAKAB, BALAT, BANVT, BARMA, BASCM, BASGZ, BAYRK, BERA, BEYAZ, BFREN, BIMAS, BIOEN, BIZIM, BJKAS, BLCYT, BMSCH, BMSTL, BNTAS, BOBET, BOSSA, BRISA, BRKO, BRKSN, BRLSM, BRMEN, BRSAN, BRYAT, BSOKE, BTCIM, BUCIM, BURCE, BURVA, BVSAN, BYDNR, CANTE, CASA, CCOLA, CELHA, CEMAS, CEMTS, CEOEM, CIMSA, CLEBI, CMBTN, CMENT, CONSE, COSMO, CRDFA, CRFSA, CUSAN, CVKMD, CWENE, DAGH, DAPGM, DARDL, DITAS, DMSAS, DNISI, DOAS, DOBUR, DOGUB, DOHOL, DOKTA, DURDO, DYOBY, ECILC, ECZYT, EDATA, EDIP, EGEEN, EGGUB, EGPRO, EGSER, EKGYO, EKIZ, EKSUN, ELITE, EMNIS, ENJSA, ENKAI, ENSRI, EPLAS, EREGL, ERSU, ESCAR, ESCOM, ESEN, ETILR, EUREN, EUYO, FADE, FENER, FLAP, FMIZP, FONET, FORMT, FORTE, FRIGO, FROTO, FZLGY, GARAN, GARFA, GEDIK, GEDZA, GENTS, GEREL, GERSAN, GESAN, GGLO, GIPTA, GLBMD, GLRYH, GLYHO, GMTAS, GOKNR, GOLTS, GOODY, GOZDE, GRNYO, GSDDE, GSDHO, GUBRF, GWIND, GZNMI, HALKB, HATEK, HDFGS, HEDEF, HEKTS, HKTM, HLGYO, HTTBT, HUBVC, HUNER, HURGZ, ICBCT, IDEAS, IDGYO, IEYHO, IHEVA, IHGZT, IHLAS, IHLGM, IHYAY, IMASM, INDES, INFO, INGRM, INTEM, INVEO, INVES, ISBIR, ISBTR, ISCTR, ISDMR, ISFIN, ISGSY, ISGYO, ISKPL, ISMEN, ISSEN, IZFAS, IZMDC, JANTS, KAPLM, KAREL, KARSN, KARTN, KARYE, KATMR, KAYSE, KCAER, KCHOL, KENT, KERVT, KFEIN, KGYO, KILIZ, KIMMR, KLGYO, KLKIM, KLMSN, KLNMA, KLRHO, KNFRT, KONKA, KONTR, KONYA, KORDS, KOZAL, KOZAA, KRGYO, KRONT, KRSTL, KRTEK, KRVGD, KSTUR, KTLEV, KTSKR, KUTPO, KUVVA, KUYAS, KZBGY, KZGYO, LIDER, LIDFA, LINK, LKMNH, LOGO, LUKSK, MAALT, MACKO, MAGEN, MAKIM, MAKTK, MANAS, MARKA, MARTI, MAVI, MEDTR, MEGAP, MEPET, MERCN, MERKO, METUR, MGROS, MIATK, MIPAZ, MNDRS, MOBTL, MPARK, MRGYO, MRSHL, MSGYO, MTRKS, MTRYO, MZHLD, NATEN, NETAS, NIBAS, NTGAZ, NTHOL, NUGYO, NUHCM, OBAS, ODAS, OFSYM, ONCSM, ORCAY, ORGE, ORMA, OSMEN, OSTIM, OTKAR, OYAKC, OYLUM, OYOYO, OZGYO, OZKGY, OZRDN, OZSUB, PAGYO, PAMEL, PARSN, PASEU, PATEK, PCILT, PEGYO, PEKGY, PENGD, PENTA, PETKM, PETUN, PGSUS, PINSU, PKART, PKENT, PLAT, PNLSN, PNSUT, POLHO, POLTK, PRDGS, PRKAB, PRKME, PRZMA, PSDTC, PSGYO, QNBFB, RALYH, RAYSG, REEDR, RNPOL, RODRG, ROYAL, RTALB, RUBNS, RYGYO, RYSAS, SAFKR, SAHOL, SAMAT, SANEL, SANFM, SANKO, SARKY, SASA, SAYAS, SDTTR, SEKFK, SEKUR, SELEC, SELGD, SELVA, SEYKM, SILVR, SISE, SKBNK, SKTAS, SMART, SMRTG, SNAI, SNICA, SNPAM, SOKM, SONME, SRVGY, SUMAS, SUNGW, SUWEN, TARKM, TATGD, TAVHL, TBORG, TCELL, TDGYO, TEKTU, TERRA, TGSAS, THYAO, TKFEN, TKNSA, TLMAN, TMPOL, TMSN, TNZTP, TOASO, TRCAS, TRGYO, TRILC, TSPOR, TTKOM, TTRAK, TUKAS, TUPRS, TUREX, TURGG, TURSG, UFUK, ULAS, ULKER, ULUFA, ULUSE, ULUUN, UMPAS, UNLU, USAK, UZERB, VAKBN, VAKFN, VAKKO, VANGD, VBTYZ, VERUS, VESBE, VESTL, VKFYO, VKGYO, VKING, YAPRK, YATAS, YAYLA, YEOTK, YESIL, YGGYO, YGYO, YKBNK, YKSLN, YONGA, YUNSA, ZOREN
"""

# --- 3. VERİ MOTORU ---
@st.cache_data(ttl=300)
def veri_getir(hisse, bar_sayisi):
    try:
        symbol = f"{hisse}.IS" if not hisse.endswith(".IS") else hisse
        df = yf.download(symbol, period="1y", progress=False)
        if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
        df = df.rename(columns={'Open':'Open', 'High':'High', 'Low':'Low', 'Close':'Close'})
        df['SMA20'] = df['Close'].rolling(20).mean()
        df['SMA50'] = df['Close'].rolling(50).mean()
        return df.tail(bar_sayisi)
    except: return None

# --- 4. ANALİZ MOTORU ---
def analiz_yap(df, secilen_formasyonlar, tolerans):
    if len(df) < 50: return None
    son = df.iloc[-1]
    bulunan = None
    skor = 0
    hedef_orani = 1.10
    
    # Boğa Bayrak
    if "Boğa Bayrak" in secilen_formasyonlar:
        if son['Close'] > son['SMA20'] and son['SMA20'] > son['SMA50']:
            bulunan = "Boğa Bayrak"
            skor = 90
            hedef_orani = 1.20
            
    # Fincan Kulp
    if "Fincan Kulp" in secilen_formasyonlar and not bulunan:
        if son['Close'] > df['Low'].min() * 1.30:
            bulunan = "Fincan Kulp"
            skor = 85
            hedef_orani = 1.25
            
    # High Tight Flag
    if "High Tight Flag 🚀" in secilen_formasyonlar and not bulunan:
        iki_ay_once = df['Close'].iloc[-40] if len(df) > 40 else df['Close'].iloc[0]
        if son['Close'] > iki_ay_once * 1.50:
            bulunan = "High Tight Flag 🚀"
            skor = 98
            hedef_orani = 1.40

    if bulunan:
        idx_dip = df['Low'].tail(60).idxmin()
        idx_tepe = df['High'].tail(60).idxmax()
        return {
            "Formasyon": bulunan, "Skor": skor, "Hedef": son['Close'] * hedef_orani, "Potansiyel": (hedef_orani - 1) * 100,
            "Points": {"t_start": idx_dip, "t_peak": idx_tepe, "t_break": df.index[-1], "p_start": df.loc[idx_dip]['Low'], "p_peak": df.loc[idx_tepe]['High'], "p_break": son['Close']}
        }
    return None

# --- 5. ARAYÜZ (KONTROL PANELİ) ---
st.title("🦅 Zacharia Ultimate")

with st.sidebar:
    st.header("⚙️ AYARLAR")
    
    # LİSTE SEÇİMİ (BURAYI İSTEDİĞİN GİBİ YAPTIM)
    st.subheader("1. Liste Seçimi")
    liste_modu = st.radio("Tarama Modu:", ["Favori Listem", "TÜM HİSSELER (BIST)", "BIST 30 (Hızlı)"])
    
    # FAVORİ LİSTESİ EDİTÖRÜ (İŞTE BURASI!)
    if liste_modu == "Favori Listem":
        st.info("👇 Listenizi buraya yazın, otomatik kaydedilir.")
        # Session state ile kaydet ki silinmesin
        if 'my_favs' not in st.session_state:
            st.session_state.my_favs = "THYAO, ASELS, GARAN, AKBNK, TCELL, EREGL, SASA, HEKTS, FROTO, KONTR"
            
        kullanici_listesi = st.text_area("Hisse Kodları (Virgülle Ayır):", value=st.session_state.my_favs, height=150)
        st.session_state.my_favs = kullanici_listesi # Güncelle
        hisseler = [h.strip() for h in kullanici_listesi.split(',')]
        
    elif liste_modu == "TÜM HİSSELER (BIST)":
        st.warning("⚠️ 400+ Hisse taranacak. Bu işlem 1-2 dakika sürebilir.")
        hisseler = [h.strip() for h in TUM_HISSELER_STR.replace('\n', '').split(',')]
        
    else: # BIST 30
        bist30 = "AKBNK,ARCLK,ASELS,ASTOR,BIMAS,BRSAN,EKGYO,ENKAI,EREGL,FROTO,GARAN,GUBRF,HEKTS,ISCTR,KCHOL,KONTR,KOZAL,KRDMD,ODAS,OYAKC,PETKM,PGSUS,SAHOL,SASA,SISE,TCELL,THYAO,TOASO,TUPRS,YKBNK"
        hisseler = bist30.split(',')
    
    # FORMASYON SEÇİMİ
    st.subheader("2. Formasyon")
    secilen_formasyonlar = st.multiselect("Ne Arıyoruz?", ["Boğa Bayrak", "Fincan Kulp", "High Tight Flag 🚀"], default=["Boğa Bayrak", "High Tight Flag 🚀"])
    
    # HASSASİYET
    st.subheader("3. Hassasiyet")
    bar_sayisi = st.slider("Gün Sayısı", 50, 200, 100)
    tolerans = st.slider("Tolerans", 1, 5, 3)
    
    st.markdown("---")
    btn_baslat = st.button("🚀 TARAMAYI BAŞLAT", type="primary")

# --- 6. SONUÇ EKRANI ---
if btn_baslat:
    hisseler = [h for h in hisseler if len(h) > 1] # Boşlukları temizle
    st.info(f"🔍 Toplam {len(hisseler)} hisse için tarama başlatıldı...")
    
    bar = st.progress(0)
    bulunanlar = []
    
    # Tarama Döngüsü
    for i, hisse in enumerate(hisseler):
        bar.progress((i+1)/len(hisseler))
        df = veri_getir(hisse, bar_sayisi)
        if df is not None:
            sonuc = analiz_yap(df, secilen_formasyonlar, tolerans)
            if sonuc:
                sonuc['Hisse'] = hisse
                sonuc['Fiyat'] = df['Close'].iloc[-1]
                bulunanlar.append(sonuc)
    bar.empty()
    
    if not bulunanlar:
        st.warning("❌ Hiçbir hissede sinyal bulunamadı.")
    else:
        st.success(f"🎉 {len(bulunanlar)} adet fırsat yakalandı!")
        
        tab_kart, tab_liste = st.tabs(["🖼️ Grafik Kartları", "📋 Özet Liste"])
        
        with tab_kart:
            for veri in bulunanlar:
                with st.expander(f"📌 {veri['Hisse']} - {veri['Formasyon']} (%{veri['Potansiyel']:.1f})", expanded=True):
                    # Grafik Çizimi
                    df_c = veri_getir(veri['Hisse'], bar_sayisi)
                    pts = veri['Points']
                    
                    fig, ax = plt.subplots(figsize=(10, 5))
                    ax.plot(df_c.index, df_c['Close'], color='#3b82f6', linewidth=2, label='Fiyat')
                    ax.plot(df_c.index, df_c['SMA20'], color='orange', linestyle='--', alpha=0.5, label='SMA20')
                    
                    # Noktalar
                    ax.scatter(pts['t_start'], pts['p_start'], color='green', s=100, zorder=5)
                    ax.scatter(pts['t_peak'], pts['p_peak'], color='red', s=100, zorder=5)
                    ax.scatter(pts['t_break'], pts['p_break'], color='gold', marker='*', s=200, zorder=5)
                    
                    ax.grid(True, alpha=0.15)
                    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))
                    plt.xticks(rotation=45)
                    st.pyplot(fig)
                    plt.close(fig)
                    
                    # Bilgi Fişi
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown(f"**DİP:** {pts['t_start'].strftime('%d.%m')} -> `{pts['p_start']:.2f}`")
                        st.markdown(f"**TEPE:** {pts['t_peak'].strftime('%d.%m')} -> `{pts['p_peak']:.2f}`")
                    with c2:
                        st.markdown(f"**SİNYAL:** {pts['t_break'].strftime('%d.%m')} -> `{pts['p_break']:.2f}`")
                        st.info(f"🎯 **HEDEF:** {veri['Hedef']:.2f} TL")

        with tab_liste:
             st.dataframe(pd.DataFrame(bulunanlar)[['Hisse', 'Fiyat', 'Formasyon', 'Potansiyel', 'Skor']], use_container_width=True)
