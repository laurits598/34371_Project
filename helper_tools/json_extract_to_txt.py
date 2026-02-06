import json
import re

def init_json_to_txt(
    input_path="ip_data_files/valid_ips.json",
    output_path="ip_data_files/valid_ips.txt",
):
    with open(input_path, "r", encoding="utf-8") as f:
        raw = f.read()

    # This fixes the common invalid JSON array issue.
    fixed = re.sub(r",\s*\]", "\n]", raw)

    # (Optional) also remove a trailing comma at end-of-file if someone forgot the closing bracket properly
    fixed = re.sub(r",\s*\Z", "\n", fixed)

    data = json.loads(fixed)  # expects a JSON array: [ {...}, {...} ]

    with open(output_path, "w", encoding="utf-8") as out:
        for item in data:
            ip = item.get("ip")
            if ip:
                out.write(ip + "\n")


INPUT_FILE = "ip_data_files/valid_ips.json"
OUTPUT_FILE = "ip_data_files/target_ips.txt"




def init_json_to_txt_in(input, output):
    with open(input, "r") as f:
        data = json.load(f)

    ips = set()

    for entry in data:
        ip = entry.get("ip")
        if ip:
            ips.add(ip)

    with open(output, "w") as f:
        for ip in sorted(ips):
            f.write(ip + "\n")

    print(f"Wrote {len(ips)} IPs to {output}")

