import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# --- 1. AYARLAR ---
st.set_page_config(
    page_title="ZACHAİRA PRO", 
    page_icon="🦅", 
    layout="wide", 
    initial_sidebar_state="expanded" 
)

# Sistem Mesajı (Çalıştığını görmek için)
st.success("Sistem ve Veri Bağlantısı Aktif. Analiz yapmaya hazır.")

# --- 2. DEVASA HİSSE LİSTESİ (500+ ADET) ---
TUM_HISSELER_STR = """
A1CAP, ACSEL, ADEL, ADESE, ADGYO, AEFES, AFYON, AGES, AGHOL, AGROT, AGYO, AHGAZ, AHSGY, AKBNK, AKCNS, AKENR, AKFGY, AKGRT, AKMGY, AKSA, AKSEN, AKSGY, AKSUE, AKYHO, ALARK, ALBRK, ALCAR, ALCTL, ALFAS, ALGYO, ALKA, ALKIM, ALMAD, ALTNY, ANELE, ANGEN, ANHYT, ANSGR, ARASE, ARCLK, ARDYZ, ARENA, ARSAN, ARZUM, ASELS, ASGYO, ASTOR, ASUZU, ATAKP, ATATP, ATEKS, ATLAS, ATPSY, AVGYO, AVHOL, AVOD, AVTUR, AYCES, AYDEM, AYEN, AYES, AYGAZ, AZTEK, BAGFS, BAKAB, BALAT, BANVT, BARMA, BASCM, BASGZ, BAYRK, BEGYO, BERA, BERK, BESLR, BEYAZ, BFREN, BIENY, BIGCH, BIMAS, BINBN, BINHO, BIOEN, BIZIM, BJKAS, BLCYT, BMSCH, BMSTL, BNTAS, BOBET, BORLS, BOSSA, BRISA, BRKO, BRKSN, BRKVY, BRLSM, BRMEN, BRSAN, BRYAT, BSOKE, BTCIM, BUCIM, BURCE, BURVA, BVSAN, BYDNR, CANTE, CASA, CATES, CCOLA, CELHA, CEMAS, CEMTS, CEOEM, CIMSA, CLEBI, CMBTN, CMENT, CONSE, COSMO, CRDFA, CRFSA, CUSAN, CVKMD, CWENE, DAGH, DAPGM, DARDL, DAREN, DENGE, DERHL, DERIM, DESA, DESPC, DEVA, DGATE, DGGYO, DGNMO, DIRIT, DITAS, DMSAS, DNISI, DOAS, DOBUR, DOGUB, DOHOL, DOKTA, DOYLE, DURDO, DYOBY, DZGYO, EBEBK, ECILC, ECZYT, EDATA, EDIP, EGEEN, EGGUB, EGPRO, EGSER, EKGYO, EKIZ, EKSUN, ELITE, EMNIS, ENJSA, ENKAI, ENSRI, ENTRA, EPLAS, EREGL, ERSU, ESCAR, ESCOM, ESEN, ETILR, ETYAT, EUHOL, EUREN, EUYO, FADE, FENER, FLAP, FMIZP, FONET, FORMT, FORTE, FRIGO, FROTO, FZLGY, GARAN, GARFA, GEDIK, GEDZA, GENTS, GEREL, GERSAN, GESAN, GGLO, GIPTA, GLBMD, GLRYH, GLYHO, GMTAS, GOKNR, GOLTS, GOODY, GOZDE, GPNTP, GRNYO, GRSEL, GSDDE, GSDHO, GUBRF, GUNDG, GWIND, GZNMI, HALKB, HATEK, HATSN, HDFGS, HEDEF, HEKTS, HKTM, HLGYO, HRKET, HTTBT, HUBVC, HUNER, HURGZ, ICBCT, IDEAS, IDGYO, IEYHO, IHEVA, IHGZT, IHLAS, IHLGM, IHYAY, IMASM, INDES, INFO, INGRM, INTEM, INVEO, INVES, IPEKE, ISATR, ISBIR, ISBTR, ISCTR, ISDMR, ISFIN, ISGSY, ISGYO, ISKPL, ISKUR, ISMEN, ISSEN, ISYAT, IZFAS, IZMDC, IZENR, JANTS, KAPLM, KAREL, KARSN, KARTN, KARYE, KATMR, KAYSE, KBORU, KCAER, KCHOL, KENT, KERVN, KERVT, KFEIN, KGYO, KILIZ, KIMMR, KLGYO, KLKIM, KLMSN, KLNMA, KLRHO, KLSYN, KMPUR, KNFRT, KOCMT, KONKA, KONTR, KONYA, KOPOL, KORDS, KOTON, KOZAL, KOZAA, KRGYO, KRONT, KRPLS, KRSTL, KRTEK, KRVGD, KSTUR, KTLEV, KTSKR, KUTPO, KUVVA, KUYAS, KZBGY, KZGYO, LIDER, LIDFA, LILAK, LINK, LKMNH, LMKDC, LOGO, LUKSK, MAALT, MACKO, MAGEN, MAKIM, MAKTK, MANAS, MARBL, MARKA, MARTI, MAVI, MEDTR, MEGAP, MEKAG, MENTD, MEPET, MERCN, MERIT, MERKO, METRO, METUR, MGROS, MIATK, MHRGY, MIPAZ, MKRS, MNDRS, MOBTL, MPARK, MRGYO, MRSHL, MSGYO, MTRKS, MTRYO, MZHLD, NATEN, NETAS, NIBAS, NTGAZ, NTHOL, NUGYO, NUHCM, OBAMS, OBAS, ODAS, ODINE, OFSYM, ONCSM, ORCAY, ORGE, ORMA, OSMEN, OSTIM, OTKAR, OYAKC, OYLUM, OYOYO, OZGYO, OZKGY, OZRDN, OZSUB, PAGYO, PAMEL, PARSN, PASEU, PATEK, PCILT, PEGYO, PEKGY, PENGD, PENTA, PETKM, PETUN, PGSUS, PINSU, PKART, PKENT, PLAT, PNLSN, PNSUT, POLHO, POLTK, PRDGS, PRKAB, PRKME, PRZMA, PSDTC, PSGYO, QNBFB, QUAGR, RALYH, RAYSG, REEDR, RGYAS, RNPOL, RODRG, ROYAL, RTALB, RUBNS, RYGYO, RYSAS, SAFKR, SAHOL, SAMAT, SANEL, SANFM, SANKO, SARKY, SASA, SAYAS, SDTTR, SEGYO, SEKFK, SEKUR, SELEC, SELGD, SELVA, SEYKM, SILVR, SISE, SKBNK, SKTAS, SMART, SMRTG, SNAI, SNICA, SNPAM, SODSN, SOKE, SOKM, SONME, SRVGY, SUMAS, SUNGW, SURGY, SUWEN, TABGD, TARKM, TATGD, TAVHL, TBORG, TCELL, TDGYO, TEKTU, TERRA, TGSAS, THYAO, TKFEN, TKNSA, TLMAN, TMPOL, TMSN, TNZTP, TOASO, TRCAS, TRGYO, TRILC, TSKB, TSPOR, TTKOM, TTRAK, TUCLK, TUKAS, TUPRS, TUREX, TURGG, TURSG, UFUK, ULAS, ULKER, ULUFA, ULUSE, ULUUN, UMPAS, UNLU, USAK, UZERB, VAKBN, VAKFN, VAKKO, VANGD, VBTYZ, VERUS, VESBE, VESTL, VKFYO, VKGYO, VKING, VRGYO, YAPRK, YATAS, YAYLA, YBTAS, YEOTK, YESIL, YGGYO, YGYO, YKBNK, YKSLN, YONGA, YUNSA, YYAPI, YYLGD, ZEDUR, ZOREN, ZRGYO
"""

# --- 3. VERİ MOTORU ---
@st.cache_data(ttl=300)
def veri_getir(hisse, bar_sayisi):
    try:
        symbol = f"{hisse}.IS" if not hisse.endswith(".IS") else hisse
        # Veriyi çek
        df = yf.download(symbol, period="1y", progress=False)
        if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
        df = df.rename(columns={'Open':'Open', 'High':'High', 'Low':'Low', 'Close':'Close', 'Volume':'Volume'})
        
        # İndikatörler (Gerçek Matematik)
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

# --- 4. ANALİZ MOTORU (DİNAMİK HEDEF) ---
def analiz_yap(df, secilen_formasyonlar, tolerans):
    if len(df) < 50: return None
    son = df.iloc[-1]
    
    bulunan = None
    skor = 0
    hedef_fiyat = 0
    
    # Tolerans Katsayısı (Tolerans arttıkça kurallar gevşer)
    tol_katsayi = 1 + (tolerans * 0.01) # Örn: Tolerans 3 ise %3 esneklik

    # 1. BOĞA BAYRAK
    if "Boğa Bayrak" in secilen_formasyonlar:
        # Direk Boyu hesapla
        son_30 = df.tail(30)
        dip = son_30['Low'].min()
        tepe = son_30['High'].max()
        direk_boyu = tepe - dip
        
        # Koşul: Tepeden fazla uzaklaşmamış ve ortalama üstünde
        esneklik = 0.85 / tol_katsayi 
        if son['Close'] > tepe * esneklik and son['Close'] > son['SMA20']:
            bulunan = "Boğa Bayrak"
            skor = 85
            hedef_fiyat = son['Close'] + (direk_boyu * 0.8)
            
    # 2. HIGH TIGHT FLAG (Roket)
    if "High Tight Flag 🚀" in secilen_formasyonlar and not bulunan:
        kirk_gun = df['Close'].iloc[-40] if len(df) > 40 else df['Close'].iloc[0]
        # 40 günde %60 prim yapmış mı?
        prim_sarti = 1.60 / tol_katsayi
        if son['Close'] > kirk_gun * prim_sarti:
            if son['Close'] > df['High'].tail(10).max() * 0.90:
                bulunan = "High Tight Flag 🚀"
                skor = 98
                hedef_fiyat = son['Close'] * 1.40 
                
    # 3. DİP DÖNÜŞ / FİNCAN
    if "Fincan Kulp" in secilen_formasyonlar and not bulunan:
        if df['RSI'].iloc[-5:].min() < (30 * tol_katsayi) and son['RSI'] > 35:
             bulunan = "Dip Dönüşü / Fincan"
             skor = 80
             hedef_fiyat = son['Close'] * 1.20 

    if bulunan:
        potansiyel = ((hedef_fiyat - son['Close']) / son['Close']) * 100
        idx_dip = df['Low'].tail(60).idxmin()
        idx_tepe = df['High'].tail(60).idxmax()
        
        return {
            "Formasyon": bulunan, 
            "Skor": skor, 
            "Hedef": hedef_fiyat, 
            "Potansiyel": potansiyel,
            "Fiyat": son['Close'],
            "Points": {
                "t_start": idx_dip, 
                "t_peak": idx_tepe, 
                "t_break": df.index[-1], 
                "p_start": df.loc[idx_dip]['Low'], 
                "p_peak": df.loc[idx_tepe]['High'], 
                "p_break": son['Close']
            }
        }
    return None

# --- 5. ARAYÜZ (TÜM ÖZELLİKLER AKTİF) ---
st.title("🦅 ZACHAİRA PRO V12")

with st.sidebar:
    st.header("⚙️ KONTROL PANELİ")
    
    # 1. LİSTE KAYNAĞI
    st.subheader("1. Liste Kaynağı")
    liste_modu = st.radio("Seçim:", ["FAVORİLERİM", "TÜM HİSSELER (500+)", "BIST 30"])
    
    if liste_modu == "FAVORİLERİM":
        if 'fav_hisseler' not in st.session_state:
            st.session_state.fav_hisseler = "THYAO, GARAN, ASELS, AKBNK, TCELL, EREGL"
        user_list = st.text_area("Hisselerinizi Girin:", value=st.session_state.fav_hisseler, height=100)
        st.session_state.fav_hisseler = user_list
        hisseler = [h.strip() for h in user_list.split(',')]
        
    elif liste_modu == "TÜM HİSSELER (500+)":
        st.warning("⚠️ Tüm borsa taranacak. 2-3 dakika sürebilir.")
        hisseler = [h.strip() for h in TUM_HISSELER_STR.replace('\n', '').split(',') if len(h) > 1]
        
    else: # BIST 30
        hisseler = "AKBNK,ARCLK,ASELS,ASTOR,BIMAS,BRSAN,EKGYO,ENKAI,EREGL,FROTO,GARAN,GUBRF,HEKTS,ISCTR,KCHOL,KONTR,KOZAL,KRDMD,ODAS,OYAKC,PETKM,PGSUS,SAHOL,SASA,SISE,TCELL,THYAO,TOASO,TUPRS,YKBNK".split(',')
        
    # 2. DİĞER AYARLAR
    st.subheader("2. Analiz Ayarları")
    secilen_formasyonlar = st.multiselect("Formasyonlar", ["Boğa Bayrak", "High Tight Flag 🚀", "Fincan Kulp"], default=["Boğa Bayrak", "High Tight Flag 🚀"])
    
    # 3. HASSASİYET (Senin İstediğin Kısım)
    st.subheader("3. Hassasiyet")
    bar_sayisi = st.slider("Grafik Derinliği", 50, 200, 100)
    tolerans = st.slider("Tolerans", 1, 10, 3, help="Değer arttıkça daha çok sonuç bulur.")
    
    btn_baslat = st.button("🚀 TARAMAYI BAŞLAT", type="primary")

# --- 6. SONUÇ EKRANI ---
if btn_baslat:
    temiz_hisseler = sorted(list(set([h.upper() for h in hisseler if len(h) > 1])))
    st.info(f"🔍 Toplam {len(temiz_hisseler)} hisse taranıyor... (Güvenli Mod)")
    
    bar = st.progress(0)
    bulunanlar = []
    
    for i, hisse in enumerate(temiz_hisseler):
        bar.progress((i+1)/len(temiz_hisseler))
        df = veri_getir(hisse, bar_sayisi)
        if df is not None:
            sonuc = analiz_yap(df, secilen_formasyonlar, tolerans)
            if sonuc:
                sonuc['Hisse'] = hisse
                bulunanlar.append(sonuc)
    bar.empty()
    
    if not bulunanlar:
        st.warning("❌ Kriterlere uygun hisse bulunamadı. Toleransı artırarak tekrar deneyin.")
    else:
        st.success(f"🎉 {len(bulunanlar)} Fırsat Bulundu!")
        
        tab_grafik, tab_liste = st.tabs(["🖼️ GRAFİK KARTLARI", "📋 ÖZET LİSTE"])
        
        # TAB 1: Grafikler
        with tab_grafik:
            for veri in bulunanlar:
                with st.expander(f"📌 {veri['Hisse']} - %{veri['Potansiyel']:.1f} Potansiyel", expanded=True):
                    # Grafik
                    df_c = veri_getir(veri['Hisse'], bar_sayisi)
                    pts = veri['Points']
                    
                    fig, ax = plt.subplots(figsize=(10, 5))
                    ax.plot(df_c.index, df_c['Close'], color='#007bff', linewidth=2, label='Fiyat')
                    ax.plot(df_c.index, df_c['SMA20'], color='orange', linestyle='--', alpha=0.7, label='SMA 20')
                    
                    # Noktalar
                    ax.scatter(pts['t_start'], pts['p_start'], color='green', s=100, label='Dip')
                    ax.scatter(pts['t_peak'], pts['p_peak'], color='red', s=100, label='Tepe')
                    ax.scatter(pts['t_break'], pts['p_break'], color='gold', marker='*', s=200, label='Sinyal')
                    
                    ax.set_title(f"HEDEF: {veri['Hedef']:.2f} TL")
                    ax.grid(True, alpha=0.3)
                    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))
                    plt.xticks(rotation=45)
                    st.pyplot(fig)
                    plt.close(fig)
                    
                    # Bilgi
                    c1, c2 = st.columns(2)
                    with c1:
                        st.write(f"**Fiyat:** {veri['Fiyat']:.2f} TL")
                        st.write(f"**Skor:** {veri['Skor']}/100")
                    with c2:
                        st.info(f"🎯 Hedef: {veri['Hedef']:.2f} TL")

        # TAB 2: Özet Liste
        with tab_liste:
            df_table = pd.DataFrame(bulunanlar)
            if not df_table.empty:
                df_final = df_table[['Hisse', 'Fiyat', 'Hedef', 'Potansiyel', 'Formasyon', 'Skor']]
                st.dataframe(
                    df_final,
                    use_container_width=True,
                    column_config={
                        "Fiyat": st.column_config.NumberColumn("Fiyat", format="%.2f TL"),
                        "Hedef": st.column_config.NumberColumn("Hedef", format="%.2f TL"),
                        "Potansiyel": st.column_config.NumberColumn("Potansiyel %", format="%.1f%%"),
                    }
                )
