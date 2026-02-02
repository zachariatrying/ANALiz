import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
from scipy.signal import argrelextrema

# --- 1. AYARLAR ---
st.set_page_config(
    page_title="ZACHAİRA MOBILE", 
    page_icon="🦅", 
    layout="wide", 
    initial_sidebar_state="expanded" 
)

# Mobil CSS
st.markdown("""
<style>
    .stApp { background-color: transparent; }
    .streamlit-expanderHeader { 
        font-size: 1.1rem !important; 
        font-weight: bold !important; 
        background-color: #262730; 
        border-radius: 8px;
        color: white;
    }
    div[data-testid="stMetricValue"] { color: #4ade80; }
</style>
""", unsafe_allow_html=True)

# --- 2. LİSTE ---
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
        
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))

        return df.tail(bar_sayisi)
    except: return None

# --- 4. GRAFİK OLUŞTURUCU (PLOTLY) ---
def grafik_ciz(df, hisse, veri):
    # Arka planı şeffaf yapıp temaya uyduruyoruz
    layout = go.Layout(
        title=f"{hisse} - {veri['Formasyon']}",
        xaxis=dict(title='Tarih', gridcolor='rgba(128,128,128,0.2)'),
        yaxis=dict(title='Fiyat', gridcolor='rgba(128,128,128,0.2)'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=500,
        margin=dict(l=10, r=10, t=40, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    fig = go.Figure(layout=layout)

    # 1. MUM GRAFİĞİ
    fig.add_trace(go.Candlestick(
        x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
        name='Fiyat'
    ))

    # 2. SMA
    fig.add_trace(go.Scatter(x=df.index, y=df['SMA20'], line=dict(color='orange', width=1), name='SMA20'))

    # 3. KANAL & DESTEK/DİRENÇ
    if 'Tech' in veri:
        # Kanal
        fig.add_trace(go.Scatter(x=df.index, y=veri['Tech']['Upper'], line=dict(color='gray', width=1, dash='dash'), name='Kanal Üst', visible='legendonly'))
        fig.add_trace(go.Scatter(x=df.index, y=veri['Tech']['Lower'], line=dict(color='gray', width=1, dash='dash'), name='Kanal Alt', visible='legendonly'))
        
        # Destek/Direnç (Sonuncuları çizelim)
        for res in veri['Tech']['Resistances'][-2:]:
            fig.add_hline(y=res, line_dash="dot", line_color="red", opacity=0.5)
        for sup in veri['Tech']['Supports'][-2:]:
            fig.add_hline(y=sup, line_dash="dot", line_color="green", opacity=0.5)

    # 4. HEDEF ÇİZGİSİ
    fig.add_hline(y=veri['Hedef'], line_color="green", line_width=2, annotation_text=f"HEDEF: {veri['Hedef']:.2f}", annotation_position="top left")

    # 5. NOKTALAR (İnteraktif Markerlar)
    pts = veri['Points']
    fig.add_trace(go.Scatter(
        x=[pts['t_start'], pts['t_peak'], pts['t_break']],
        y=[pts['p_start'], pts['p_peak'], pts['p_break']],
        mode='markers',
        marker=dict(size=[10, 10, 15], color=['green', 'red', 'gold'], symbol=['circle', 'circle', 'star']),
        name='Formasyon Noktaları'
    ))
    
    fig.update_layout(xaxis_rangeslider_visible=False)
    
    return fig

# --- 5. ANALİZ MOTORU ---
def analiz_yap(df, secilen_formasyonlar, tolerans, zaman_etiketi):
    if len(df) < 50: return None
    son = df.iloc[-1]
    
    bulunan = None
    hedef_fiyat = 0
    skor = 50 
    tol_katsayi = 1 + (tolerans * 0.01)

    # Skorlama
    if son['Close'] > son['SMA20']: skor += 10
    if son['SMA20'] > son['SMA50']: skor += 10
    if 45 < son['RSI'] < 70: skor += 20 

    # --- FORMASYONLAR ---
    # 1. BOĞA BAYRAK
    if "Boğa Bayrak" in secilen_formasyonlar:
        son_30 = df.tail(30)
        dip = son_30['Low'].min()
        tepe = son_30['High'].max()
        direk_boyu = tepe - dip
        
        esneklik = 0.88 / tol_katsayi
        if son['Close'] > tepe * esneklik and son['Close'] > son['SMA20']:
             bulunan = "Boğa Bayrak"
             hedef_fiyat = son['Close'] + direk_boyu
             if (tepe - son['Close']) / tepe < 0.05: skor += 15

    # 2. ROKET
    if "High Tight Flag 🚀" in secilen_formasyonlar and not bulunan:
        kirk_bar = df['Close'].iloc[-40] if len(df) > 40 else df['Close'].iloc[0]
        if son['Close'] > kirk_bar * (1.60 / tol_katsayi):
            if son['Close'] > df['High'].tail(10).max() * 0.90:
                bulunan = "High Tight Flag 🚀"
                skor += 20
                direk = df['High'].tail(40).max() - df['Low'].tail(40).min()
                hedef_fiyat = son['Close'] + (direk * 0.618)

    # 3. FİNCAN
    if "Fincan Kulp" in secilen_formasyonlar and not bulunan:
        if df['RSI'].iloc[-10:].min() < (35 * tol_katsayi) and son['RSI'] > 40:
             derinlik = df['High'].tail(60).max() - df['Low'].tail(60).min()
             bulunan = "Fincan Kulp"
             hedef_fiyat = son['Close'] + derinlik

    if bulunan:
        if hedef_fiyat <= son['Close']: hedef_fiyat = son['Close'] * 1.05
        potansiyel = ((hedef_fiyat - son['Close']) / son['Close']) * 100
        
        # Teknik Çizgiler Hesapla (Destek/Direnç/Kanal)
        n=5
        ilocs_max = argrelextrema(df['High'].values, np.greater_equal, order=n)[0]
        ilocs_min = argrelextrema(df['Low'].values, np.less_equal, order=n)[0]
        direncler = df['High'].iloc[ilocs_max].tail(3).values
        destekler = df['Low'].iloc[ilocs_min].tail(3).values
        
        # Regresyon
        x = np.arange(len(df))
        y = df['Close'].values
        slope, intercept = np.polyfit(x, y, 1)
        trend = slope * x + intercept
        std = np.std(y - trend)
        
        idx_dip = df['Low'].tail(60).idxmin()
        idx_tepe = df['High'].tail(60).idxmax()

        return {
            "Formasyon": bulunan, "Skor": min(skor, 100), "Hedef": hedef_fiyat, "Potansiyel": potansiyel, "Fiyat": son['Close'], "Periyot": zaman_etiketi,
            "Points": {"t_start": idx_dip, "t_peak": idx_tepe, "t_break": df.index[-1], "p_start": df.loc[idx_dip]['Low'], "p_peak": df.loc[idx_tepe]['High'], "p_break": son['Close']},
            "Tech": {"Supports": destekler, "Resistances": direncler, "Upper": trend + 2*std, "Lower": trend - 2*std}
        }
    return None

# --- 6. ARAYÜZ ---
st.title("🦅 ZACHAİRA MOBILE V19")

with st.sidebar:
    st.header("KONTROL PANELİ")
    
    # ------------------ DÜZELTİLEN KISIM BURASI ------------------
    zaman_secimi = st.selectbox("Periyot:", ["GÜNLÜK (1D)", "HAFTALIK (1W)", "AYLIK (1M)"])
    if "GÜNLÜK" in zaman_secimi: yf_int, yf_per, z_etiket = "1d", "2y", "GÜNLÜK"
    elif "HAFTALIK" in zaman_secimi: yf_int, yf_per, z_etiket = "1wk", "5y", "HAFTALIK"
    else: yf_int, yf_per, z_etiket = "1mo", "max", "AYLIK"
    # -------------------------------------------------------------

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
    bar_sayisi = st.slider("Grafik Derinliği", 30, 200, 100)
    tolerans = st.slider("Tolerans", 1, 10, 3)
    btn_baslat = st.button("🚀 BAŞLAT", type="primary")

# --- 7. ÇIKTI EKRANI ---
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
        st.warning("❌ Sonuç yok.")
    else:
        st.success(f"🎉 {len(bulunanlar)} Fırsat!")
        
        tab1, tab2 = st.tabs(["🖼️ KARTLAR", "📋 TABLO"])
        
        with tab1:
            for veri in bulunanlar:
                # Expander Başlığı (Tıklanabilir Alan)
                baslik = f"📌 {veri['Hisse']} | {veri['Formasyon']} | 🎯 Pot: %{veri['Potansiyel']:.1f}"
                with st.expander(baslik, expanded=False): # Varsayılan kapalı olsun ki liste düzenli dursun
                    # İNTERAKTİF GRAFİK ÇİZ
                    df_c = veri_getir(veri['Hisse'], bar_sayisi, yf_int, yf_per)
                    fig = grafik_ciz(df_c, veri['Hisse'], veri)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Detaylar
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Fiyat", f"{veri['Fiyat']:.2f}")
                    c2.metric("Hedef", f"{veri['Hedef']:.2f}")
                    c3.metric("Skor", f"{veri['Skor']}")

        with tab2:
            df_final = pd.DataFrame(bulunanlar)
            cols = ['Hisse', 'Fiyat', 'Formasyon', 'Periyot', 'Potansiyel', 'Hedef', 'Skor']
            st.dataframe(
                df_final[cols], 
                use_container_width=True,
                column_config={
                    "Potansiyel": st.column_config.NumberColumn("Potansiyel %", format="%.1f%%"),
                    "Fiyat": st.column_config.NumberColumn("Fiyat", format="%.2f"),
                    "Hedef": st.column_config.NumberColumn("Hedef", format="%.2f")
                }
            )
