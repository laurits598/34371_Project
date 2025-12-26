import json

INPUT_FILE = "ip_data_files/valid_ips.json"
#INPUT_FILE = "test.json"
OUTPUT_FILE = "ip_data_files/target_ips.txt"

def init_json_to_txt():
    with open(INPUT_FILE, "r") as f:
        data = json.load(f)

    ips = set()

    for entry in data:
        ip = entry.get("ip")
        if ip:
            ips.add(ip)

    with open(OUTPUT_FILE, "w") as f:
        for ip in sorted(ips):
            f.write(ip + "\n")

    print(f"Wrote {len(ips)} IPs to {OUTPUT_FILE}")
