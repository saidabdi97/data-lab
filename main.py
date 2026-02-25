import pandas as pd

# --- Load ---
df = pd.read_csv("products.csv", sep=";")

# --- Transform / clean ---
df["price"] = pd.to_numeric(df["price"], errors="coerce")

df["id"] = df["id"].astype("string").str.strip()
df["name"] = df["name"].astype("string").str.strip()
df["currency"] = df["currency"].astype("string").str.strip().str.upper()

dates = (
    df["created_at"]
    .astype("string")
    .str.strip()
    .str.replace("/", "-", regex=False)
)
df["created_at"] = pd.to_datetime(dates, errors="coerce", format="%Y-%m-%d")

# --- Quality checks (flag / reject rules) ---
missing_price = df["price"].isna()
missing_currency = df["currency"].isna()
missing_id = df["id"].isna()

negative_price = df["price"] < 0
zero_price = df["price"] == 0

invalid_date = df["created_at"].isna()

# Reject = "omöjligt att använda i analys"
# (konservativt: saknar id eller valuta, eller negativt pris)
reject_condition = missing_id | missing_currency | negative_price

# Flag = "misstänkt/behöver kollas" men kan vara giltigt
flag_condition = zero_price | invalid_date

# --- Analytics base (what we actually use for avg/median) ---
# Vi använder bara priser som är:
# - numeriska
# - inte negativa
# - inte rejectade
df_analysis = df.loc[~reject_condition].copy()
df_analysis = df_analysis.loc[df_analysis["price"].notna() & (df_analysis["price"] >= 0)]

# --- Required summary metrics ---
avg_price = df_analysis["price"].mean()
median_price = df_analysis["price"].median()
total_products = len(df)
missing_price_count = int(missing_price.sum())

summary = pd.DataFrame([{
    "average_price": avg_price,
    "median_price": median_price,
    "product_count": total_products,
    "missing_price_count": missing_price_count
}])

summary.to_csv("analytics_summary.csv", index=False)

# --- Print quick status (for you & teacher) ---
print(df.head())
print("Total products:", total_products)
print("Missing currency:", int(missing_currency.sum()))
print("Missing price:", missing_price_count)
print("Invalid dates:", int(invalid_date.sum()))
print("Negative prices:", int(negative_price.sum()))
print("Rejected rows:", int(reject_condition.sum()))
print("Flagged rows:", int(flag_condition.sum()))
print("Wrote: analytics_summary.csv")
