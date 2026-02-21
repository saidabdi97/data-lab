import pandas as pd

df = pd.read_csv("products.csv", sep=";")

df["price"] = pd.to_numeric(df["price"], errors="coerce")

print(df.head())
print(df.info())
