import pandas as pd

# Load the CSV (assumes no header and comma-separated)
df = pd.read_csv("results.csv", header=None, names=["IP", "Flag", "Unused1", "Unused2"])

df["Flag"] = df["Flag"].astype(str).str.strip().str.lower() == "true"

# Filter rows where Flag is True
filtered = df[df["Flag"]]

# Save matching IPs to a file
filtered["IP"].to_csv("telnet_login_accept.txt", index=False, header=False)

print(f"Saved {len(filtered)} IPs with Flag=True to 'true_ips.txt'")
