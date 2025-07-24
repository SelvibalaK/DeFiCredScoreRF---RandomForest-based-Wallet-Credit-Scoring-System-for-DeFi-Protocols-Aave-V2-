import pandas as pd
import json
from tqdm import tqdm

with open("user_transactions.json", "r") as f:
    data = json.load(f)

records = []
for item in tqdm(data):
    try:
        record = {
            "wallet": item["userWallet"],
            "action": item["action"],
            "amount": float(item["actionData"].get("amount", 0)) / 1e6,
            "timestamp": item["timestamp"]
        }
        records.append(record)
    except:
        continue

df = pd.DataFrame(records)
df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")

wallet_features = []

for wallet, group in df.groupby("wallet"):
    features = {
        "wallet": wallet,
        "total_txns": len(group),
        "unique_actions": group["action"].nunique(),
        "total_amount": group["amount"].sum(),
        "total_deposit": group[group["action"] == "deposit"]["amount"].sum(),
        "total_borrow": group[group["action"] == "borrow"]["amount"].sum(),
        "total_repay": group[group["action"] == "repay"]["amount"].sum(),
        "total_redeem": group[group["action"] == "redeemunderlying"]["amount"].sum(),
        "total_liquidations": len(group[group["action"] == "liquidationcall"]),
        "days_active": (group["timestamp"].max() - group["timestamp"].min()).days + 1,
    }

    features["repay_ratio"] = (
        features["total_repay"] / features["total_borrow"] if features["total_borrow"] > 0 else 0
    )
    features["deposit_redeem_ratio"] = (
        features["total_deposit"] / features["total_redeem"] if features["total_redeem"] > 0 else 0
    )

    wallet_features.append(features)

wallet_df = pd.DataFrame(wallet_features)
wallet_df.to_csv("wallet_features.csv", index=False)

df = wallet_df.copy()
df["score"] = 500

df.loc[df["repay_ratio"] >= 1.0, "score"] += 200
df.loc[df["repay_ratio"] < 0.5, "score"] -= 150
df.loc[df["total_liquidations"] > 0, "score"] -= 100 * df["total_liquidations"]
df.loc[df["days_active"] > 90, "score"] += 100
df.loc[df["days_active"] < 7, "score"] -= 50
df.loc[df["unique_actions"] <= 2, "score"] -= 50
df.loc[(df["total_borrow"] > 1e6) & (df["repay_ratio"] >= 1.0), "score"] += 100

df["score"] = df["score"].clip(0, 1000)
df[["wallet", "score"]].to_csv("wallet_scores.csv", index=False)

print("✅ One-step scoring complete. Output saved to wallet_scores.csv")
