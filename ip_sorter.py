import pandas as pd

target_file = "ip_comma_port.txt"

# Load the data
df = pd.read_csv(target_file, names=["IP", "Port"])

# Sort by port
df_sorted = df.sort_values(by="Port")

# Show sorted data
print("Sorted by port:")
print(df_sorted)

# Filter by specific port (e.g., 23)
port_23 = df_sorted[df_sorted["Port"] == 23]

# Save filtered IPs to a file
port_23["IP"].to_csv("port_23_ips.txt", index=False, header=False)

print("\nSaved IPs with port 23 to 'port_23_ips.txt'")