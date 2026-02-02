import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# --- 1. AYARLAR ---
st.set_page_config(
    page_title="ZACHAİRA PRO V18", 
    page_icon="🦅", 
    layout="wide", 
    initial_sidebar_state="expanded" 
)

st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .stExpander { background-color: #1f2937; border: 1px solid #4b5563; }
    div[data-testid="stMetricValue"] { font-family: 'Courier New', monospace; color: #4ade80; }
    /* Tablo Başlıkları */
    thead tr th:first-child { display:none }
    tbody th { display:none }
</style>
""", unsafe_allow_html=True)

# --- 2. LİSTE (FULL) ---
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
        
        # İndikatörler
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

# --- 4. ANALİZ MOTORU (GEOMETRİK HESAPLAMA) ---
def analiz_yap(df, secilen_formasyonlar, tolerans, zaman_etiketi):
    if len(df) < 50: return None
    son = df.iloc[-1]
    
    bulunan = None
    hedef_fiyat = 0
    skor = 50 
    
    tol_katsayi = 1 + (tolerans * 0.01)

    # --- A. TEMEL SKORLAMA (PUAN) ---
    if son['Close'] > son['SMA20']: skor += 10
    if son['SMA20'] > son['SMA50']: skor += 10
    if son['SMA50'] > son['SMA200']: skor += 10 # Trend Gücü
    if 45 < son['RSI'] < 70: skor += 20 # İdeal RSI

    # --- B. FORMASYON ANALİZİ ---
    
    # 1. BOĞA BAYRAK (BULL FLAG)
    if "Boğa Bayrak" in secilen_formasyonlar:
        # Son 30-40 mum içindeki Zirveyi bul
        pencere = 40
        son_veri = df.tail(pencere)
        
        idx_tepe = son_veri['High'].idxmax()
        tepe_fiyat = son_veri.loc[idx_tepe]['High']
        
        # DİKKAT: Zirveden ÖNCEKİ en düşük noktayı bul (Direk Başlangıcı)
        # Zirveye kadar olan kısmı kesip alıyoruz
        veri_oncesi = son_veri.loc[:idx_tepe]
        if len(veri_oncesi) > 5: # En az 5 mumluk bir yükseliş olmalı
            idx_dip = veri_oncesi['Low'].idxmin()
            dip_fiyat = veri_oncesi.loc[idx_dip]['Low']
            
            direk_boyu = tepe_fiyat - dip_fiyat
            
            # ŞARTLAR:
            # 1. Direk boyu anlamlı olmalı (En az %10 yükseliş)
            if direk_boyu > (dip_fiyat * 0.10):
                # 2. Şu anki fiyat tepeden çok düşmemeli (Bayrak Formu)
                esneklik = 0.88 / tol_katsayi
                if son['Close'] > tepe_fiyat * esneklik and son['Close'] > son['SMA20']:
                    
                    bulunan = "Boğa Bayrak"
                    # HEDEF: Mevcut Fiyat + Direk Boyu
                    hedef_fiyat = son['Close'] + direk_boyu
                    
                    # Skor Bonusu: Bayrak ne kadar darsa o kadar iyi
                    dusukluk = (tepe_fiyat - son['Close']) / tepe_fiyat
                    if dusukluk < 0.05: skor += 15 # Çok sıkı bayrak

    # 2. HIGH TIGHT FLAG (ROKET)
    if "High Tight Flag 🚀" in secilen_formasyonlar and not bulunan:
        # Son 60 güne bakalım
        pencere = 60
        son_veri = df.tail(pencere)
        
        # 1. Büyük Yükseliş (Direk)
        dipten_zirveye = (son_veri['High'].max() - son_veri['Low'].min()) / son_veri['Low'].min()
        
        if dipten_zirveye > 0.50: # En az %50 yükseliş (Direk)
            # 2. Konsolidasyon (Fiyat düşmemiş)
            zirve = son_veri['High'].max()
            if son['Close'] > zirve * (0.90 / tol_katsayi): # %10'dan fazla salmamış
                
                bulunan = "High Tight Flag 🚀"
                skor += 20
                # HEDEF: Fibonacci Uzatma (Direğin %61.8'i kadar daha gitmesi beklenir)
                direk_boyu = son_veri['High'].max() - son_veri['Low'].min()
                hedef_fiyat = son['Close'] + (direk_boyu * 0.618)

    # 3. FİNCAN KULP
    if "Fincan Kulp" in secilen_formasyonlar and not bulunan:
        # RSI'dan teyit alalım
        if df['RSI'].iloc[-10:].min() < (35 * tol_katsayi) and son['RSI'] > 40:
             # Basit Derinlik
             son_60 = df.tail(60)
             derinlik = son_60['High'].max() - son_60['Low'].min()
             
             bulunan = "Fincan Kulp"
             hedef_fiyat = son['Close'] + derinlik

    # --- C. PAKETLEME ---
    if bulunan:
        # Hata payı kontrolü (Negatif hedef çıkmasın)
        if hedef_fiyat <= son['Close']: hedef_fiyat = son['Close'] * 1.05
            
        potansiyel = ((hedef_fiyat - son['Close']) / son['Close']) * 100
        
        # Grafik noktaları (Hata almamak için güvenli seçim)
        idx_dip = df['Low'].tail(60).idxmin()
        idx_tepe = df['High'].tail(60).idxmax()
        
        return {
            "Formasyon": bulunan,
            "Skor": min(skor, 100),
            "Hedef": hedef_fiyat,
            "Potansiyel": potansiyel,
            "Fiyat": son['Close'],
            "Periyot": zaman_etiketi,
            "Points": {
                "t_start": idx_dip, "t_peak": idx_tepe, 
                "t_break": df.index[-1], 
                "p_start": df.loc[idx_dip]['Low'], 
                "p_peak": df.loc[idx_tepe]['High'], 
                "p_break": son['Close']
            }
        }
    return None

# --- 5. ARAYÜZ ---
st.title("🦅 ZACHAİRA V18 PRO")

with st.sidebar:
    st.header("KONTROL PANELİ")
    
    st.subheader("1. Zaman")
    zaman_secimi = st.selectbox("Periyot:", ["GÜNLÜK (1D)", "HAFTALIK (1W)", "AYLIK (1M)"])
    if "GÜNLÜK" in zaman_secimi: yf_int, yf_per, z_etiket = "1d", "2y", "GÜNLÜK"
    elif "HAFTALIK" in zaman_secimi: yf_int, yf_per, z_etiket = "1wk", "5y", "HAFTALIK"
    else: yf_int, yf_per, z_etiket = "1mo", "max", "AYLIK"

    st.subheader("2. Kaynak")
    liste_modu = st.radio("Liste:", ["FAVORİLERİM", "TÜM HİSSELER", "BIST 30"])
    
    if liste_modu == "FAVORİLERİM":
        if 'fav_hisseler' not in st.session_state: st.session_state.fav_hisseler = "THYAO, GARAN, ASELS, AKBNK"
        user_list = st.text_area("Hisseler:", value=st.session_state.fav_hisseler)
        st.session_state.fav_hisseler = user_list
        hisseler = [h.strip() for h in user_list.split(',')]
    elif liste_modu == "TÜM HİSSELER":
        hisseler = [h.strip() for h in TUM_HISSELER_STR.replace('\n', '').split(',') if len(h) > 1]
    else:
        hisseler = "AKBNK,ARCLK,ASELS,ASTOR,BIMAS,BRSAN,EKGYO,ENKAI,EREGL,FROTO,GARAN,GUBRF,HEKTS,ISCTR,KCHOL,KONTR,KOZAL,KRDMD,ODAS,OYAKC,PETKM,PGSUS,SAHOL,SASA,SISE,TCELL,THYAO,TOASO,TUPRS,YKBNK".split(',')

    secilen_formasyonlar = st.multiselect("Formasyon", ["Boğa Bayrak", "High Tight Flag 🚀", "Fincan Kulp"], default=["Boğa Bayrak", "High Tight Flag 🚀"])
    bar_sayisi = st.slider("Veri Derinliği", 30, 200, 100)
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
                baslik = f"📌 {veri['Hisse']} - {veri['Formasyon']} (%{veri['Potansiyel']:.1f})"
                with st.expander(baslik, expanded=True):
                    # Grafik Çiz
                    df_c = veri_getir(veri['Hisse'], bar_sayisi, yf_int, yf_per)
                    pts = veri['Points']
                    
                    fig, ax = plt.subplots(figsize=(10, 5))
                    ax.plot(df_c.index, df_c['Close'], color='#2563eb', linewidth=2, label="Fiyat")
                    ax.plot(df_c.index, df_c['SMA20'], color='orange', linestyle='--', label="SMA20")
                    
                    # Hedef Çizgisi (Yeşil Kesik)
                    ax.axhline(y=veri['Hedef'], color='green', linestyle=':', linewidth=2, label='HEDEF')
                    
                    # Noktalar
                    ax.scatter(pts['t_start'], pts['p_start'], color='green', s=100)
                    ax.scatter(pts['t_peak'], pts['p_peak'], color='red', s=100)
                    ax.scatter(pts['t_break'], pts['p_break'], color='gold', marker='*', s=200)
                    
                    ax.grid(True, alpha=0.3)
                    ax.legend(loc='upper left')
                    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))
                    plt.xticks(rotation=45)
                    st.pyplot(fig)
                    plt.close(fig)
                    
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Hedef Fiyat", f"{veri['Hedef']:.2f}")
                    c2.metric("Skor", f"{veri['Skor']}")
                    c3.metric("Zaman", f"{veri['Periyot']}")

        with tab2:
            df_final = pd.DataFrame(bulunanlar)
            cols = ['Hisse', 'Formasyon', 'Periyot', 'Fiyat', 'Hedef', 'Potansiyel', 'Skor']
            st.dataframe(
                df_final[cols], 
                use_container_width=True,
                column_config={
                    "Potansiyel": st.column_config.NumberColumn("Potansiyel %", format="%.1f%%"),
                    "Fiyat": st.column_config.NumberColumn("Fiyat", format="%.2f"),
                    "Hedef": st.column_config.NumberColumn("Hedef", format="%.2f")
                }
            )
