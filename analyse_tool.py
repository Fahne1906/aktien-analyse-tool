import streamlit as st
import yfinance as yf
import pandas as pd

# Erweiterte Liste von Aktien-Tickern (beispielhaft gekürzt)
tickers = [
     "AAPL", "MSFT", "TSLA", "AMZN", "GOOG", "META", "NVDA", "NFLX", "KO", "PEP",
    "JNJ", "PG", "MCD", "BRK.A", "V", "MA", "DIS", "BMW.DE", "ALV.DE", "SIE.DE", 
    "SAP.DE", "DBK.DE", "VOW3.DE", "BASF.DE", "ADS.DE", "BAYN.DE", "MRK.DE", "SHOP", 
    "PYPL", "ZM", "SNAP", "UBER", "TWTR", "BABA", "JD", "NTES", "TCEHY", "BIDU", 
    "BA", "SPOT", "ROKU", "PINS", "PFE", "XOM", "CVX", "BP", "LULU", "F", "GM", 
    "NKE", "VZ", "T", "FISV", "WMT", "HD", "LOW", "COST", "AMT", "DHR", "BDX", 
    "ISRG", "ABT", "TSM", "TMO", "LVMH.PA", "OR.PA", "AXP", "GS", "MS", "JPM", 
    "V", "MA", "AMEX", "RDS.A", "SHEL", "NEE", "XEL", "DUK", "AWK", "AEP", "SO", 
    "SYY", "CL", "KMB", "PG", "CLX", "PEP", "KO", "GIS", "K", "CPB", "SJM", 
    "UNH", "CVS", "MDT", "BDX", "CI", "HUM", "ANTM", "CNC", "EL", "UL", "BIB", 
    "FSLR", "ENPH", "RUN", "SOL", "SPWR", "SEDG", "CSIQ", "VEEV", "NOW", "CRM",
    "WORK", "VEEV", "MDB", "FVRR", "UPST", "DOCU", "CRWD", "ZS", "OKTA", "RNG", 
    "LSPD", "SHOP", "SHOP.TO", "PSTG", "PTON", "PLTR", "DT", "DKNG", "BBBY", 
    "ELF", "UPST", "TSLA", "LCID", "RIVN", "BYND", "HOOD", "COIN", "PINS", 
    "MSFT", "AAPL", "MELI", "RBLX", "ROKU", "TTD", "SNAP", "SPOT", "NVDA", 
    "XPEV", "NIO", "LI", "FSR", "BA", "LMT", "NOC", "RTX", "GD", "HON", "CAT", 
    "DE", "IR", "ETN", "EMR", "HII", "LHX", "ITW", "MMM", "GE", "TRMB", "SNA", 
    "SCHW", "ETFC", "BLK", "TROW", "STT", "JEF", "MS", "GS", "JP", "BAC", "C", 
    "WFC", "USB", "PNC", "TD", "BMO", "RY", "CIBC", "AMT", "SBAC", "CCI", "PLD", 
    "EQIX", "DRE", "DLR", "PSA", "SBUX", "MCD", "YUM", "DPZ", "CMG", "TACO", 
    "WEN", "PZZA", "PTN", "STZ", "MO", "PM", "UVV", "HRL", "SYY", "COST", "WMT", 
    "COST", "LMT", "CSX", "NSC", "UPL", "PXD", "COP", "EOG", "XOM", "CVX", 
    "PBR", "OXY", "BKR", "HES", "SLB", "GE", "GEHC", "HON", "ADBE", "INTU", 
    "VRSK", "AKAM", "CSCO", "QCOM", "AMAT", "NVDA", "AMD", "INTC", "TSM", "MU",
    "ON", "LRCX", "SOXX", "SMH", "TQQQ", "SPY", "QQQ", "VTI", "VOO", "SPYG", 
    "SCHG", "SCHX", "IJR", "IWM", "VO", "VUG", "MGK", "IWF", "IWD", "IJH", 
    "IWB", "SCHV", "IWV", "SCHA", "VTHR", "VUG", "QTEC", "XLY", "XLF", "XLC", 
    "XLI", "XLE", "XLB", "XME", "XHE", "HACK", "SOXX", "XBI", "LIT", "KRE"
]

# Funktion zur Bewertung der Aktien
def bewertung(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    
    # Wichtige Kennzahlen abrufen
    kgv = info.get('trailingPE', None)
    kbv = info.get('priceToBook', None)
    div_yield = info.get('dividendYield', 0)
    roe = info.get('returnOnEquity', None)
    beta = info.get('beta', None)
    earnings_growth = info.get('earningsQuarterlyGrowth', None)
    peg = info.get('pegRatio', None)
    ps_ratio = info.get('priceToSalesTrailing12Months', None)
    debt_to_equity = info.get('debtToEquity', None)
    fcf = info.get('freeCashflow', None)

    # Bewertungskriterien
    punkte = 0
    if kgv and kgv < 20: punkte += 1
    if kbv and kbv < 3: punkte += 1
    if div_yield > 0.03: punkte += 1
    if roe and roe > 0.10: punkte += 1
    if beta and beta < 1: punkte += 1
    if earnings_growth and earnings_growth > 0: punkte += 1
    if peg and peg < 1: punkte += 1
    if ps_ratio and ps_ratio < 2: punkte += 1
    if debt_to_equity and debt_to_equity < 1: punkte += 1
    if fcf and fcf > 0: punkte += 1

    return punkte, info.get('longName', ticker)

# Bewertung für alle Aktien durchführen
bewertete_aktien = []
for ticker in tickers:
    punkte, name = bewertung(ticker)
    bewertete_aktien.append((name, ticker, punkte))

# Sortiere die Aktien nach ihrer Punktzahl (höchste zuerst)
bewertete_aktien = sorted(bewertete_aktien, key=lambda x: x[2], reverse=True)

# Ausgabe der besten Empfehlungen
st.title("📊 Beste Kaufempfehlungen - Aktien und ETFs")
st.subheader("Die besten Kaufempfehlungen:")

# Tabelle der besten Aktien
df_bewertung = pd.DataFrame(bewertete_aktien, columns=["Name", "Ticker", "Punkte"])
st.table(df_bewertung)

# Zeige die besten 5
st.subheader("Top 5 Kaufempfehlungen:")
st.table(df_bewertung.head(5))
