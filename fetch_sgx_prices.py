import os
import yfinance as yf
import psycopg2
from datetime import datetime
from zoneinfo import ZoneInfo
import sys

# ---------------- TIMEZONE ----------------
SG_TZ = ZoneInfo("Asia/Singapore")

now_sg = datetime.now(SG_TZ)
print(f"🕒 Job started at (SGT): {now_sg}")

# ---------------- WEEKDAY GUARD ----------------
if now_sg.weekday() >= 5:
    print("⏸️ Weekend in Singapore. Job skipped.")
    sys.exit(0)

# ---------------- DEFINE STOCKS ----------------
MY_STOCKS = [
    {"name": "ACMA", "code": "AYV.SI", "total": 225},
    {"name": "F & N", "code": "F99.SI", "total": 1000},
    {"name": "FRASERS PROPERTY", "code": "TQ5.SI", "total": 2000},
    {"name": "GP INDUSTRIES", "code": "G20.SI", "total": 10000},
    {"name": "HL GLOBAL ENT", "code": "AVX.SI", "total": 2000},
    {"name": "HONG LEONG FIN", "code": "S41.SI", "total": 3073},
    {"name": "KEP INFRA TR", "code": "A7RU.SI", "total": 1053},
    {"name": "KEPPEL", "code": "BN4.SI", "total": 2750},
    {"name": "KEPPEL REIT", "code": "K71U.SI", "total": 1320},
    {"name": "OCBC BANK", "code": "O39.SI", "total": 100},
    {"name": "SEATRIUM LTD", "code": "5E2.SI", "total": 2919},
    {"name": "SEMBCORP IND", "code": "U96.SI", "total": 1000},
    {"name": "THAKRAL", "code": "AWI.SI", "total": 500},
    {"name": "WING TAI", "code": "W05.SI", "total": 6000},
]

# ---------------- DATABASE ----------------
DATABASE_URL = os.environ.get("POSTGRES_URI")
if not DATABASE_URL:
    raise RuntimeError("❌ POSTGRES_URI environment variable not set")

# ---------------- FETCH PRICES (PYTHONANYWHERE-EQUIVALENT) ----------------
def fetch_prices(stocks):
    prices = {}
    dates = {}

    for stock in stocks:
        ticker = yf.Ticker(stock["code"])

        # Fetch last 2 trading days to tolerate Yahoo delay
        history = ticker.history(
            period="2d",
            interval="1d",
            auto_adjust=False
        ).dropna()

        if history.empty:
            prices[stock["code"]] = None
            dates[stock["code"]] = None
            print(f"⚠️ No data for {stock['name']} ({stock['code']})")
            continue

        latest = history.iloc[-1]

        close_price = float(latest["Close"])
        trading_date = latest.name.date().isoformat()

        prices[stock["code"]] = close_price
        dates[stock["code"]] = trading_date

        print(
            f"[OK] {stock['name']} ({stock['code']}) "
            f"@ {close_price:,} on {trading_date}"
        )

    return prices, dates

# ---------------- UPDATE DB ----------------
def update_db(stocks):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    sql = """
    INSERT INTO stock_price (
        today_date, name, code, free, blocked, total,
        currency, market_price, market_value
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (today_date, code)
    DO UPDATE SET
        market_price = EXCLUDED.market_price,
        market_value = EXCLUDED.market_value,
        total = EXCLUDED.total,
        currency = EXCLUDED.currency
    """

    for stock in stocks:
        cursor.execute(sql, (
            stock["trading_date"],
            stock["name"],
            stock["code"].replace(".SI", ""),
            0, 0,
            stock["total"],
            "SGD",
            stock["market_price"],
            stock["market_value"]
        ))

    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ Database updated with {len(stocks)} stocks.")

# ---------------- MAIN ----------------
if __name__ == "__main__":
    prices, dates = fetch_prices(MY_STOCKS)

    enriched = []
    for stock in MY_STOCKS:
        code = stock["code"]
        price = prices.get(code)
        trading_date = dates.get(code)

        if price is None or trading_date is None:
            print(f"[SKIP] {stock['name']} ({code})")
            continue

        enriched.append({
            **stock,
            "market_price": price,
            "market_value": price * stock["total"],
            "trading_date": trading_date
        })

    if enriched:
        update_db(enriched)
    else:
        print("⚠️ No valid stocks to update.")

    print("🏁 SGX fetch job completed.")
