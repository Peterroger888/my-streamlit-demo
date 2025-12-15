import os
import yfinance as yf
import psycopg2
from datetime import datetime

# -------- DEFINE STOCKS --------
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
    {"name": "WING TAI", "code": "W05.SI", "total": 6000}
]

# -------- DATABASE URL FROM ENV --------
DATABASE_URL = os.environ.get("POSTGRES_URI")

if not DATABASE_URL:
    raise RuntimeError("📌 ERROR: POSTGRES_URI environment variable is not set!")


# -------- FETCH PRICES FROM YAHOO --------
def fetch_prices(stocks):
    prices = {}
    dates = {}

    for stock in stocks:
        ticker = yf.Ticker(stock["code"])
        history = ticker.history(period="1d")

        if not history.empty:
            close_price = float(history["Close"].iloc[-1])
            trading_date = history.index[-1].date().isoformat()

            prices[stock["code"]] = close_price
            dates[stock["code"]] = trading_date

            print(
                f"[OK] {stock['name']} ({stock['code']}) "
                f"@ {close_price:,} on {trading_date}"
            )
        else:
            prices[stock["code"]] = None
            dates[stock["code"]] = None
            print(f"[WARN] No data for {stock['name']} ({stock['code']})")

    return prices, dates


# -------- UPDATE DB --------
def update_db(stocks):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    # UPSERT: if (today_date, code) exists, update values
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
            0,  # free
            0,  # blocked
            stock["total"],
            "SGD",
            stock["market_price"],
            stock["market_value"]
        ))

    conn.commit()
    cursor.close()
    conn.close()
    print(f"[SUCCESS] DB updated with {len(stocks)} stocks.")


# -------- MAIN --------
if __name__ == "__main__":
    print("🕒 Starting SGX price fetch at", datetime.utcnow().isoformat())

    prices, dates = fetch_prices(MY_STOCKS)
    enriched = []

    for stock in MY_STOCKS:
        code = stock["code"]
        price = prices.get(code)
        date_str = dates.get(code)

        if price is None or date_str is None:
            print(f"[SKIP] {stock['name']} ({code}) skipped.")
            continue

        total = stock["total"]
        market_val = price * total

        enriched.append({
            **stock,
            "market_price": price,
            "market_value": market_val,
            "trading_date": date_str
        })

    if enriched:
        update_db(enriched)
    else:
        print("⚠ No valid stocks to update.")

    print("✅ Fetch job complete.")
