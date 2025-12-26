from helper_tools.ip_gen_tool_v2 import generate_ips 
from helper_tools.json_extract_to_txt import init_json_to_txt
from exploit_scan_tools.telnet_scan import main as telnet_main
import subprocess

IP_AMOUNT = 100000

print("Generating IP addresses...")
generate_ips(IP_AMOUNT)

print("Running masscan...")
masscan_command = [
    "sudo",
    "masscan",
    "-iL", "ip_data_files/generated_ips.txt",
    "-p23",
    "--rate", "10000",
    "--wait", "2",
    "-oJ", "ip_data_files/valid_ips.json"
]

subprocess.run(masscan_command, check=True)

print("Extracting valid IPs to text file...")
init_json_to_txt()

print("Running Telnet login prompt scan...")
path = "ip_data_files/target_ips.txt"
telnet_main(path)









