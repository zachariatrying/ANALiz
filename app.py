import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
from scipy.signal import argrelextrema

# --- 1. AYARLAR ---
st.set_page_config(
    page_title="ZACHAİRA V24", 
    page_icon="🦅", 
    layout="wide", 
    initial_sidebar_state="expanded" 
)

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
        try:
            df = yf.download(symbol, period=period, interval=interval, progress=False)
        except: return None
        
        if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
        df = df.rename(columns={'Open':'Open', 'High':'High', 'Low':'Low', 'Close':'Close', 'Volume':'Volume'})
        
        if df.empty or len(df) < 20: return None
        
        df['SMA20'] = df['Close'].rolling(20).mean()
        df['SMA50'] = df['Close'].rolling(50).mean()
        
        # RSI HESABI (DÜZELTİLDİ)
        delta = df['Close'].diff()
        up = delta.clip(lower=0)
        down = -1 * delta.clip(upper=0)
        gain = up.rolling(window=14).mean()
        loss = down.rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))

        return df.tail(bar_sayisi)
    except: return None

# --- 4. GRAFİK ---
def grafik_ciz(df, hisse, veri):
    layout = go.Layout(
        title=dict(text=f"{hisse} - {veri['Formasyon']}", font=dict(size=18)),
        xaxis=dict(title='Tarih', gridcolor='rgba(128,128,128,0.2)'),
        yaxis=dict(title='Fiyat', gridcolor='rgba(128,128,128,0.2)'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=500,
        margin=dict(l=10, r=10, t=40, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    fig = go.Figure(layout=layout)
    fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='Fiyat'))
    fig.add_trace(go.Scatter(x=df.index, y=df['SMA20'], line=dict(color='orange', width=1), name='SMA20'))
    
    # Teknik Seviyeler
    if 'Tech' in veri:
        fig.add_trace(go.Scatter(x=df.index, y=veri['Tech']['Upper'], line=dict(color='gray', width=1, dash='dot'), name='Kanal Üst', visible='legendonly'))
        fig.add_trace(go.Scatter(x=df.index, y=veri['Tech']['Lower'], line=dict(color='gray', width=1, dash='dot'), name='Kanal Alt', visible='legendonly'))
        for res in veri['Tech']['Resistances'][-2:]: fig.add_hline(y=res, line_dash="dot", line_color="red", opacity=0.5)
        for sup in veri['Tech']['Supports'][-2:]: fig.add_hline(y=sup, line_dash="dot", line_color="green", opacity=0.5)

    # HEDEF
    fig.add_hline(y=veri['Hedef'], line_color="green", line_width=2, annotation_text=f"HEDEF: {veri['Hedef']:.2f}", annotation_position="top left")

    if 'Points' in veri:
        pts = veri['Points']
        fig.add_trace(go.Scatter(
            x=[pts['t_start'], pts['t_peak'], pts['t_break']],
            y=[pts['p_start'], pts['p_peak'], pts['p_break']],
            mode='markers', marker=dict(size=[10, 10, 15], color=['green', 'red', 'gold'], symbol=['circle', 'circle', 'star']), name='Noktalar'
        ))
    
    fig.update_layout(xaxis_rangeslider_visible=False)
    return fig

# --- 5. ANALİZ MOTORU (DÜZELTİLMİŞ MATEMATİK) ---
def analiz_yap(df, secilen_formasyonlar, tolerans, zaman_etiketi, tek_hisse_modu=False):
    if len(df) < 50: return None
    son = df.iloc[-1]
    
    bulunan = None
    hedef_fiyat = 0
    skor = 50 
    tol_katsayi = 1 + (tolerans * 0.01)
    if tek_hisse_modu: tol_katsayi *= 1.20 # Tolerans artırıldı

    # Skorlama
    if son['Close'] > son['SMA20']: skor += 10
    if son['SMA20'] > son['SMA50']: skor += 10
    if 45 < son['RSI'] < 70: skor += 20 

    # --- FORMASYON MATEMATİĞİ ---

    # 1. BOĞA BAYRAK (GEOMETRİK DÜZELTME)
    if "Boğa Bayrak" in secilen_formasyonlar:
        # Son 40 mumluk pencere
        pencere = 40
        son_veri = df.tail(pencere)
        
        # 1. Adım: Zirveyi Bul
        idx_tepe = son_veri['High'].idxmax()
        tepe_fiyat = son_veri.loc[idx_tepe]['High']
        
        # 2. Adım: SADECE Zirveden Önceki Dibi Bul (Zaman Kontrolü)
        veri_oncesi = son_veri.loc[:idx_tepe]
        
        # Eğer zirve en baştaysa (yani yükseliş yoksa) iptal
        if len(veri_oncesi) > 3:
            idx_dip = veri_oncesi['Low'].idxmin()
            dip_fiyat = veri_oncesi.loc[idx_dip]['Low']
            
            direk_boyu = tepe_fiyat - dip_fiyat
            
            # Direk en az %5 olmalı (Gürültü olmasın)
            if direk_boyu > (dip_fiyat * 0.05):
                # Bayrak Koşulu: Fiyat zirveden çok uzaklaşmamalı
                esneklik = 0.88 / tol_katsayi
                if son['Close'] > tepe_fiyat * esneklik and son['Close'] > son['SMA20']:
                    bulunan = "Boğa Bayrak"
                    # HEDEF: Kırılım Noktası + Direk Boyu
                    # (Şu anki fiyatı kırılım kabul ediyoruz)
                    hedef_fiyat = son['Close'] + direk_boyu

    # 2. HIGH TIGHT FLAG (ROKET)
    if "High Tight Flag 🚀" in secilen_formasyonlar and not bulunan:
        # Son 50 gün
        son_50 = df.tail(50)
        idx_zirve = son_50['High'].idxmax()
        zirve_fiyat = son_50.loc[idx_zirve]['High']
        
        # Zirveden önceki dip
        veri_oncesi = son_50.loc[:idx_zirve]
        if len(veri_oncesi) > 5:
            dip_fiyat = veri_oncesi['Low'].min()
            
            # Direk %50'den büyük mü?
            if (zirve_fiyat - dip_fiyat) / dip_fiyat > 0.50:
                # Fiyat zirveye yakın mı?
                if son['Close'] > zirve_fiyat * (0.90 / tol_katsayi):
                    bulunan = "High Tight Flag 🚀"
                    skor += 20
                    direk_boyu = zirve_fiyat - dip_fiyat
                    hedef_fiyat = son['Close'] + (direk_boyu * 0.618)

    # 3. FİNCAN
    if "Fincan Kulp" in secilen_formasyonlar and not bulunan:
        # RSI ve Fiyat yapısı
        if df['RSI'].iloc[-10:].min() < (40 * tol_katsayi) and son['RSI'] > 45:
             # Basit Derinlik: Son 60 günün Yükseği - Düşüğü
             derinlik = df['High'].tail(60).max() - df['Low'].tail(60).min()
             bulunan = "Fincan Kulp"
             hedef_fiyat = son['Close'] + derinlik

    # KURTARICI
    if not bulunan and tek_hisse_modu:
        bulunan = "Genel Teknik Görünüm"
        hedef_fiyat = son['Close'] * 1.05 
        
    if bulunan:
        # HEDEF KONTROLÜ (Saçma negatif veya aşırı hedefleri engelle)
        if hedef_fiyat <= son['Close']: hedef_fiyat = son['Close'] * 1.05
        
        potansiyel = ((hedef_fiyat - son['Close']) / son['Close']) * 100
        
        # Teknik Çizgiler
        n=5
        ilocs_max = argrelextrema(df['High'].values, np.greater_equal, order=n)[0]
        ilocs_min = argrelextrema(df['Low'].values, np.less_equal, order=n)[0]
        direncler = df['High'].iloc[ilocs_max].tail(3).values
        destekler = df['Low'].iloc[ilocs_min].tail(3).values
        
        x = np.arange(len(df))
        y = df['Close'].values
        slope, intercept = np.polyfit(x, y, 1)
        trend = slope * x + intercept
        std = np.std(y - trend)
        
        # Noktaları belirle (Çizim için)
        idx_dip = df['Low'].tail(60).idxmin()
        idx_tepe = df['High'].tail(60).idxmax()

        data = {
            "Formasyon": bulunan, "Skor": min(skor, 100), "Hedef": hedef_fiyat, "Potansiyel": potansiyel, "Fiyat": son['Close'], "Periyot": zaman_etiketi,
            "Tech": {"Supports": destekler, "Resistances": direncler, "Upper": trend + 2*std, "Lower": trend - 2*std}
        }
        
        if "Genel" not in bulunan:
            data["Points"] = {"t_start": idx_dip, "t_peak": idx_tepe, "t_break": df.index[-1], "p_start": df.loc[idx_dip]['Low'], "p_peak": df.loc[idx_tepe]['High'], "p_break": son['Close']}
        else:
             data["Points"] = {"t_start": df.index[-10], "t_peak": df.index[-5], "t_break": df.index[-1], "p_start": son['Close'], "p_peak": son['Close'], "p_break": son['Close']}
        return data
    return None

# --- 6. ARAYÜZ ---
st.title("🦅 ZACHAİRA V24")

with st.sidebar:
    st.header("KONTROL PANELİ")
    
    zaman_secimi = st.selectbox("Periyot:", ["GÜNLÜK (1D)", "HAFTALIK (1W)", "AYLIK (1M)", "1 SAATLİK (1h)"])
    if "GÜNLÜK" in zaman_secimi: yf_int, yf_per, z_etiket = "1d", "2y", "GÜNLÜK"
    elif "HAFTALIK" in zaman_secimi: yf_int, yf_per, z_etiket = "1wk", "5y", "HAFTALIK"
    elif "AYLIK" in zaman_secimi: yf_int, yf_per, z_etiket = "1mo", "max", "AYLIK"
    else: yf_int, yf_per, z_etiket = "60m", "730d", "1 SAAT"

    liste_modu = st.radio("Kaynak:", ["TEK HİSSE (Hızlı Analiz)", "FAVORİLERİM", "TÜM HİSSELER", "BIST 30"])
    
    tek_hisse_aktif = False
    if liste_modu == "TEK HİSSE (Hızlı Analiz)":
        tek_hisse_input = st.text_input("Hisse Kodu (Örn: IZMDC):", "IZMDC")
        temiz_kod = tek_hisse_input.upper().strip()
        hisseler = [temiz_kod]
        tek_hisse_aktif = True
    elif liste_modu == "FAVORİLERİM":
        if 'fav_hisseler' not in st.session_state: st.session_state.fav_hisseler = "THYAO, GARAN, ASELS, AKBNK"
        user_list = st.text_area("Hisseler:", value=st.session_state.fav_hisseler)
        st.session_state.fav_hisseler = user_list
        hisseler = [h.strip() for h in user_list.split(',')]
    elif liste_modu == "TÜM HİSSELER":
        hisseler = [h.strip() for h in TUM_HISSELER_STR.replace('\n', '').split(',') if len(h) > 1]
    else:
        hisseler = "AKBNK,ARCLK,ASELS,ASTOR,BIMAS,BRSAN,EKGYO,ENKAI,EREGL,FROTO,GARAN,GUBRF,HEKTS,ISCTR,KCHOL,KONTR,KOZAL,KRDMD,ODAS,OYAKC,PETKM,PGSUS,SAHOL,SASA,SISE,TCELL,THYAO,TOASO,TUPRS,YKBNK".split(',')

    secilen_formasyonlar = st.multiselect("Formasyon", ["Boğa Bayrak", "High Tight Flag 🚀", "Fincan Kulp"], default=["Boğa Bayrak", "High Tight Flag 🚀"])
    bar_sayisi = st.slider("Grafik Derinliği", 30, 250, 100)
    tolerans = st.slider("Tolerans", 1, 10, 3)
    btn_baslat = st.button("🚀 BAŞLAT", type="primary")

# --- 7. ÇIKTI ---
if btn_baslat:
    temiz_hisseler = sorted(list(set([h.upper() for h in hisseler if len(h) > 1])))
    st.info(f"🔍 {len(temiz_hisseler)} hisse taranıyor... [{z_etiket}]")
    
    bar = st.progress(0)
    bulunanlar = []
    
    for i, hisse in enumerate(temiz_hisseler):
        bar.progress((i+1)/len(temiz_hisseler))
        df = veri_getir(hisse, bar_sayisi, yf_int, yf_per)
        if df is not None:
            sonuc = analiz_yap(df, secilen_formasyonlar, tolerans, z_etiket, tek_hisse_aktif)
            if sonuc:
                sonuc['Hisse'] = hisse
                bulunanlar.append(sonuc)
    bar.empty()
    
    if not bulunanlar:
        if tek_hisse_aktif: st.error(f"❌ {temiz_hisseler[0]} bulunamadı.")
        else: st.warning("❌ Sonuç yok.")
    else:
        st.success(f"🎉 {len(bulunanlar)} Sonuç!")
        
        for veri in bulunanlar:
            ikon = "📊" if "Genel" in veri['Formasyon'] else "🚀"
            baslik = f"{ikon} {veri['Hisse']} | {veri['Formasyon']} | Pot: %{veri['Potansiyel']:.1f}"
            with st.expander(baslik, expanded=True):
                df_c = veri_getir(veri['Hisse'], bar_sayisi, yf_int, yf_per)
                fig = grafik_ciz(df_c, veri['Hisse'], veri)
                st.plotly_chart(fig, use_container_width=True)
                
                c1, c2, c3 = st.columns(3)
                c1.metric("Fiyat", f"{veri['Fiyat']:.2f}")
                c2.metric("Hedef", f"{veri['Hedef']:.2f}")
                c3.metric("Skor", f"{veri['Skor']}")

        st.divider()
        st.subheader("📋 ÖZET TABLO")
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
