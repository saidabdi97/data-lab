import pandas as pd

# 1) Read CSV (semicolon-separated)
df = pd.read_csv("products.csv", sep=";")

# 2) Convert price to numeric (invalid -> NaN)
df["price"] = pd.to_numeric(df["price"], errors="coerce")

# 3) Clean string columns (strip whitespace, normalize currency)
df["id"] = df["id"].astype("string").str.strip()
df["name"] = df["name"].astype("string").str.strip()
df["currency"] = df["currency"].astype("string").str.strip().str.upper()

# 4) Robust date parsing:
#    - normalize separators so both "2024-01-10" and "2024/02/15" become "2024-..-.."
#    - parse using an explicit format
dates = (
    df["created_at"]
    .astype("string")
    .str.strip()
    .str.replace("/", "-", regex=False)
)
df["created_at"] = pd.to_datetime(dates, errors="coerce", format="%Y-%m-%d")

# 5) Inspect
print(df.head())
print(df.info())

# 6) Quality counts (quick checks)
print("Missing currency:", df["currency"].isna().sum())
print("Missing price:", df["price"].isna().sum())
print("Invalid dates:", df["created_at"].isna().sum())
print("Negative prices:", (df["price"] < 0).sum())
