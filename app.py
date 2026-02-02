import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# --- 1. AYARLAR ---
st.set_page_config(
    page_title="ZACbabaPRO V11", 
    page_icon="🦅", 
    layout="wide", 
    initial_sidebar_state="expanded" 
)

st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #e0e0e0; }
    [data-testid="stSidebar"] { background-color: #111827; }
    .stButton>button { border-radius: 8px; font-weight: bold; height: 3.5em; background: linear-gradient(90deg, #10b981 0%, #3b82f6 100%); color: white; border: none; }
    div[data-testid="stMetricValue"] { color: #4ade80; font-family: monospace; }
    .stExpander { border: 1px solid #374151; border-radius: 8px; background-color: #1f2937; }
</style>
""", unsafe_allow_html=True)

# --- 2. DEVASA HİSSE LİSTESİ (KORUNDU) ---
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
