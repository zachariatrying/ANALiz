import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# --- 1. AYARLAR ---
st.set_page_config(
    page_title="ZACHAİRA MOBILE V16", 
    page_icon="📱", 
    layout="wide", 
    initial_sidebar_state="expanded" 
)

# Mobil Uyumlu Temiz CSS
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .stExpander { background-color: #1f2937; border-radius: 8px; border: 1px solid #374151; }
    div[data-testid="stMetricValue"] { color: #4ade80; font-size: 1.2rem; }
    .stDataFrame { font-size: 0.9rem; }
</style>
""", unsafe_allow_html=True)

# --- 2. HİSSE LİSTESİ (TÜMÜ) ---
TUM_HISSELER_STR = """
A1CAP, ACSEL, ADEL, ADESE, ADGYO, AEFES, AFYON, AGES, AGHOL, AGROT, AGYO, AHGAZ, AHSGY, AKBNK, AKCNS, AKENR, AKFGY, AKGRT, AKMGY, AKSA, AKSEN, AKSGY, AKSUE, AKYHO, ALARK, ALBRK, ALCAR, ALCTL, ALFAS, ALGYO, ALKA, ALKIM, ALMAD, ALTNY, ANELE, ANGEN, ANHYT, ANSGR, ARASE, ARCLK, ARDYZ, ARENA, ARSAN, ARZUM, ASELS, ASGYO, ASTOR, ASUZU, ATAKP, ATATP, ATEKS, ATLAS, ATPSY, AVGYO, AVHOL, AVOD, AVTUR, AYCES, AYDEM, AYEN, AYES, AYGAZ, AZTEK, BAGFS, BAKAB, BALAT, BANVT, BARMA, BASCM, BASGZ, BAYRK, BEGYO, BERA, BERK, BESLR, BEYAZ, BFREN, BIENY, BIGCH, BIMAS, BINBN, BINHO, BIOEN, BIZIM, BJKAS, BLCYT, BMSCH, BMSTL, BNTAS, BOBET, BORLS, BOSSA, BRISA, BRKO, BRKSN, BRKVY, BRLSM, BRMEN, BRSAN, BRYAT, BSOKE, BTCIM, BUCIM, BURCE, BURVA, BVSAN, BYDNR, CANTE, CASA, CATES, CCOLA, CELHA, CEMAS, CEMTS, CEOEM, CIMSA, CLEBI, CMBTN, CMENT, CONSE, COSMO, CRDFA, CRFSA, CUSAN, CVKMD, CWENE, DAGH, DAPGM, DARDL, DAREN, DENGE, DERHL, DERIM, DESA, DESPC, DEVA, DGATE, DGGYO, DGNMO, DIRIT, DITAS, DMSAS, DNISI, DOAS, DOBUR, DOGUB, DOHOL, DOKTA, DOYLE, DURDO, DYOBY, DZGYO, EBEBK, ECILC, ECZYT, EDATA, EDIP, EGEEN, EGGUB, EGPRO, EGSER, EKGYO, EKIZ, EKSUN, ELITE, EMNIS, ENJSA, ENKAI, ENSRI, ENTRA, EPLAS, EREGL, ERSU, ESCAR, ESCOM, ESEN, ETILR, ETYAT, EUHOL, EUREN, EUYO, FADE, FENER, FLAP, FMIZP, FONET, FORMT, FORTE, FRIGO, FROTO, FZLGY, GARAN, GARFA, GEDIK, GEDZA, GENTS, GEREL, GERSAN, GESAN, GGLO, GIPTA, GLBMD, GLRYH, GLYHO, GMTAS, GOKNR, GOLTS, GOODY, GOZDE, GPNTP, GRNYO, GRSEL, GSDDE, GSDHO, GUBRF, GUNDG, GWIND, GZNMI, HALKB, HATEK, HATSN, HDFGS, HEDEF, HEKTS, HKTM, HLGYO, HRKET, HTTBT, HUBVC, HUNER, HURGZ, ICBCT, IDEAS, IDGYO, IEYHO, IHEVA, IHGZT, IHLAS, IHLGM, IHYAY, IMASM, INDES, INFO, INGRM, INTEM, INVEO, INVES, IPEKE, ISATR, ISBIR, ISBTR, ISCTR, ISDMR, ISFIN, ISGSY, ISGYO, ISKPL, ISKUR, ISMEN, ISSEN, ISYAT, IZFAS, IZMDC, IZENR, JANTS, KAPLM, KAREL, KARSN, KARTN, KARYE, KATMR, KAYSE, KBORU, KCAER, KCHOL, KENT, KERVN, KERVT, KFEIN, KGYO, KILIZ, KIMMR, KLGYO, KLKIM, KLMSN, KLNMA, KLRHO, KLSYN, KMPUR, KNFRT, KOCMT, KONKA, KONTR, KONYA, KOPOL, KORDS, KOTON, KOZAL, KOZAA, KRGYO, KRONT, KRPLS, KRSTL, KRTEK, KRVGD, KSTUR, KTLEV, KTSKR, KUTPO, KUVVA, KUYAS, KZBGY, KZGYO, LIDER, LIDFA, LILAK, LINK, LKMNH, LMKDC, LOGO, LUKSK, MAALT, MACKO, MAGEN, MAKIM, MAKTK, MANAS, MARBL, MARKA, MARTI, MAVI, MEDTR, MEGAP, MEKAG, MENTD, MEPET, MERCN, MERIT, MERKO, METRO, METUR, MGROS, MIATK, MHRGY, MIPAZ, MKRS, MNDRS, MOBTL, MPARK, MRGYO, MRSHL, MSGYO, MTRKS, MTRYO, MZHLD, NATEN, NETAS, NIBAS, NTGAZ, NTHOL, NUGYO, NUHCM, OBAMS, OBAS, ODAS, ODINE, OFSYM, ONCSM, ORCAY, ORGE, ORMA, OSMEN, OSTIM, OTKAR, OYAKC, OYLUM, OYOYO, OZGYO, OZKGY, OZRDN, OZSUB, PAGYO, PAMEL, PARSN, PASEU, PATEK, PCILT, PEGYO, PEKGY, PENGD, PENTA, PETKM, PETUN, PGSUS, PINSU, PKART, PKENT, PLAT, PNLSN, PNSUT, POLHO, POLTK, PRDGS, PRKAB, PRKME, PRZMA, PSDTC, PSGYO, QNBFB, QUAGR, RALYH, RAYSG, REEDR, RGYAS, RNPOL, RODRG, ROYAL, RTALB, RUBNS, RYGYO, RYSAS, SAFKR, SAHOL, SAMAT, SANEL, SANFM, SANKO, SARKY, SASA, SAYAS, SDTTR, SEGYO, SEKFK, SEKUR, SELEC, SELGD, SELVA, SEYKM, SILVR, SISE, SKBNK, SKTAS, SMART, SMRTG, SNAI, SNICA, SNPAM, SODSN, SOKE, SOKM, SONME, SRVGY, SUMAS, SUNGW, SURGY, SUWEN, TABGD, TARKM, TATGD, TAVHL, TBORG, TCELL, TDGYO, TEKTU, TERRA, TGSAS, THYAO, TKFEN, TKNSA, TLMAN, TMPOL, TMSN, TNZTP, TOASO, TRCAS, TRGYO, TRILC, TSKB, TSPOR, TTKOM, TTRAK, TUCLK, TUKAS, TUPRS, TUREX, TURGG, TURSG, UFUK, ULAS, ULKER, ULUFA, ULUSE, ULUUN, UMPAS, UNLU, USAK, UZERB, VAKBN, VAKFN, VAKKO, VANGD, VBTYZ, VERUS, VESBE, VESTL, VKFYO, VKGYO, VKING, VRGYO, YAPRK, YATAS, YAYLA, YBTAS, YEOTK, YESIL, YGGYO, YGYO, YKBNK, YKSLN, YONGA, YUNSA, YYAPI, YYLGD, ZEDUR, ZOREN, ZRGYO
"""

# --- 3. VERİ MOTORU ---
@st.cache_data(ttl=300)
def veri_getir(hisse, bar_sayisi, interval, period):
    try:
        symbol = f"{hisse}.IS" if not hisse.endswith(".IS") else hisse
        df = yf.download(symbol, period=period, interval=interval, progress=False)
        
        if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
        df = df.rename(columns={'Open':'Open', 'High':'High', 'Low':'Low', 'Close':'Close', 'Volume':'Volume'})
        
        if len(df) < 20: return None
        
        # TEKNİK İNDİKATÖRLER
        df['SMA20'] = df['Close'].rolling(20).mean()
        df['SMA50'] = df['Close'].rolling(50).mean()
        df['SMA200'] = df['Close'].rolling(200).mean()
        
        # RSI
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))

        return df.tail(bar_sayisi)
    except: return None

# --- 4. GELİŞMİŞ SKORLAMA VE POTANSİYEL MOTORU ---
def analiz_yap(df, secilen_formasyonlar, tolerans, zaman_etiketi):
    if len(df) < 50: return None
    son = df.iloc[-1]
    
    bulunan = None
    hedef_fiyat = 0
    skor = 50 # Başlangıç Puanı
    
    # Tolerans
    tol_katsayi = 1 + (tolerans * 0.01)

    # --- 1. SKORLAMA (PUAN TOPLAMA) ---
    # Trend Puanı (Max 30)
    if son['Close'] > son['SMA20']: skor += 10
    if son['SMA20'] > son['SMA50']: skor += 10
    if son['SMA50'] > son['SMA200']: skor += 10
    
    # RSI Puanı (Max 20)
    if 50 < son['RSI'] < 70: skor += 20 # İdeal Bölge
    elif son['RSI'] > 70: skor += 10 # Güçlü ama riskli
    
    # --- 2. FORMASYON VE HEDEF ---
    
    # A. BOĞA BAYRAK
    if "Boğa Bayrak" in secilen_formasyonlar:
        son_30 = df.tail(30)
        dip = son_30['Low'].min()
        tepe = son_30['High'].max()
        direk_boyu = tepe - dip
        
        esneklik = 0.85 / tol_katsayi 
        if son['Close'] > tepe * esneklik and son['Close'] > son['SMA20']:
            bulunan = "Boğa Bayrak"
            # HEDEF HESABI: Kırılım + Direk Boyu
            hedef_fiyat = son['Close'] + direk_boyu 
            
    # B. HIGH TIGHT FLAG
    if "High Tight Flag 🚀" in secilen_formasyonlar and not bulunan:
        kirk_bar = df['Close'].iloc[-40] if len(df) > 40 else df['Close'].iloc[0]
        prim_sarti = 1.60 / tol_katsayi
        
        if son['Close'] > kirk_bar * prim_sarti:
            if son['Close'] > df['High'].tail(10).max() * 0.90:
                bulunan = "High Tight Flag 🚀"
                skor += 15 # Roketler ekstra puan alır
                # HEDEF HESABI: Agresif %40
                hedef_fiyat = son['Close'] * 1.40 

    # C. FİNCAN KULP
    if "Fincan Kulp" in secilen_formasyonlar and not bulunan:
        # Derinlik Hesabı
        son_60 = df.tail(60)
        zirve = son_60['High'].max()
        dip_noktasi = son_60['Low'].min()
        derinlik = zirve - dip_noktasi
        
        if df['RSI'].iloc[-5:].min() < (30 * tol_katsayi) and son['RSI'] > 35:
             bulunan = "Fincan Kulp / Dip Dönüş"
             # HEDEF HESABI: Mevcut + Derinlik
             hedef_fiyat = son['Close'] + derinlik

    # --- 3. SONUÇ ÇIKTISI ---
    if bulunan:
        # GERÇEK POTANSİYEL YÜZDESİ
        # Formül: ((Hedef - Güncel) / Güncel) * 100
        potansiyel = ((hedef_fiyat - son['Close']) / son['Close']) * 100
        
        # Grafik Noktaları
        idx_dip = df['Low'].tail(60).idxmin()
        idx_tepe = df['High'].tail(60).idxmax()
        
        return {
            "Formasyon": bulunan, 
            "Skor": min(skor, 100), # Max 100 olsun
            "Hedef": hedef_fiyat, 
            "Potansiyel": potansiyel, 
            "Fiyat": son['Close'],
            "Periyot": zaman_etiketi, # İSTEDİĞİN ÖZELLİK
            "Points": {"t_start": idx_dip, "t_peak": idx_tepe, "t_break": df.index[-1], "p_start": df.loc[idx_dip]['Low'], "p_peak": df.loc[idx_tepe]['High'], "p_break": son['Close']}
        }
    return None

# --- 5. ARAYÜZ ---
st.title("📱 ZACHAİRA MOBILE V16")

with st.sidebar:
    st.header("KONTROL PANELİ")
    
    # 1. ZAMAN
    st.subheader("1. Zaman Dilimi")
    zaman_secimi = st.selectbox("Periyot:", ["GÜNLÜK (1D)", "HAFTALIK (1W)", "AYLIK (1M)"])
    if "GÜNLÜK" in zaman_secimi: yf_int, yf_per, z_etiket = "1d", "2y", "GÜNLÜK"
    elif "HAFTALIK" in zaman_secimi: yf_int, yf_per, z_etiket = "1wk", "5y", "HAFTALIK"
    else: yf_int, yf_per, z_etiket = "1mo", "max", "AYLIK"

    # 2. LİSTE
    st.subheader("2. Kaynak")
    liste_modu = st.radio("Seçim:", ["FAVORİLERİM", "TÜM HİSSELER", "BIST 30"])
    
    if liste_modu == "FAVORİLERİM":
        if 'fav_hisseler' not in st.session_state: st.session_state.fav_hisseler = "THYAO, GARAN, ASELS, AKBNK"
        user_list = st.text_area("Hisseler:", value=st.session_state.fav_hisseler)
        st.session_state.fav_hisseler = user_list
        hisseler = [h.strip() for h in user_list.split(',')]
    elif liste_modu == "TÜM HİSSELER":
        hisseler = [h.strip() for h in TUM_HISSELER_STR.replace('\n', '').split(',') if len(h) > 1]
    else:
        hisseler = "AKBNK,ARCLK,ASELS,ASTOR,BIMAS,BRSAN,EKGYO,ENKAI,EREGL,FROTO,GARAN,GUBRF,HEKTS,ISCTR,KCHOL,KONTR,KOZAL,KRDMD,ODAS,OYAKC,PETKM,PGSUS,SAHOL,SASA,SISE,TCELL,THYAO,TOASO,TUPRS,YKBNK".split(',')

    # 3. AYARLAR
    secilen_formasyonlar = st.multiselect("Formasyon", ["Boğa Bayrak", "High Tight Flag 🚀", "Fincan Kulp"], default=["Boğa Bayrak", "High Tight Flag 🚀"])
    bar_sayisi = st.slider("Grafik Derinliği", 30, 200, 100)
    tolerans = st.slider("Tolerans", 1, 10, 3)
    
    btn_baslat = st.button("🚀 BAŞLAT", type="primary")

# --- 6. SONUÇ EKRANI ---
if btn_baslat:
    temiz_hisseler = sorted(list(set([h.upper() for h in hisseler if len(h) > 1])))
    st.info(f"🔍 {len(temiz_hisseler)} hisse taranıyor... [{z_etiket}]")
    
    bar = st.progress(0)
    bulunanlar = []
    
    for i, hisse in enumerate(temiz_hisseler):
        bar.progress((i+1)/len(temiz_hisseler))
        df = veri_getir(hisse, bar_sayisi, yf_int, yf_per)
        if df is not None:
            # Zaman Etiketini fonksiyona yolla
            sonuc = analiz_yap(df, secilen_formasyonlar, tolerans, z_etiket)
            if sonuc:
                sonuc['Hisse'] = hisse
                bulunanlar.append(sonuc)
    bar.empty()
    
    if not bulunanlar:
        st.warning("❌ Sonuç yok. Toleransı artır.")
    else:
        st.success(f"🎉 {len(bulunanlar)} Fırsat!")
        
        tab1, tab2 = st.tabs(["🖼️ KARTLAR", "📋 TABLO"])
        
        with tab1:
            for veri in bulunanlar:
                with st.expander(f"📌 {veri['Hisse']} - %{veri['Potansiyel']:.1f}", expanded=True):
                    df_c = veri_getir(veri['Hisse'], bar_sayisi, yf_int, yf_per)
                    pts = veri['Points']
                    
                    fig, ax = plt.subplots(figsize=(10, 5))
                    ax.plot(df_c.index, df_c['Close'], color='#2563eb', linewidth=2)
                    ax.plot(df_c.index, df_c['SMA20'], color='orange', linestyle='--')
                    
                    # Noktalar
                    ax.scatter(pts['t_start'], pts['p_start'], color='green', s=100)
                    ax.scatter(pts['t_peak'], pts['p_peak'], color='red', s=100)
                    ax.scatter(pts['t_break'], pts['p_break'], color='gold', marker='*', s=200)
                    
                    ax.grid(True, alpha=0.3)
                    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))
                    plt.xticks(rotation=45)
                    st.pyplot(fig)
                    plt.close(fig)
                    
                    # Detaylar
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Hedef", f"{veri['Hedef']:.2f}")
                    c2.metric("Skor", f"{veri['Skor']}")
                    c3.metric("Zaman", f"{veri['Periyot']}")

        with tab2:
            # TABLOYA PERİYOT SÜTUNU EKLENDİ
            df_final = pd.DataFrame(bulunanlar)[['Hisse', 'Fiyat', 'Hedef', 'Potansiyel', 'Skor', 'Periyot', 'Formasyon']]
            st.dataframe(
                df_final, 
                use_container_width=True,
                column_config={
                    "Potansiyel": st.column_config.NumberColumn("Potansiyel %", format="%.1f%%"),
                    "Fiyat": st.column_config.NumberColumn("Fiyat", format="%.2f"),
                    "Hedef": st.column_config.NumberColumn("Hedef", format="%.2f")
                }
            )
