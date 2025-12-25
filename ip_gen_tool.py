import ipaddress

def generate_ips(start_ip, end_ip, filename):
    # Convert strings to IP address objects
    start = ipaddress.IPv4Address(start_ip)
    end = ipaddress.IPv4Address(end_ip)

    with open(filename, "w") as f:
        # Loop through all IPs in range
        for ip_int in range(int(start), int(end) + 1):
            f.write(str(ipaddress.IPv4Address(ip_int)) + "\n")

if __name__ == "__main__":
    # Define start, end, and output file
    start_ip = "212.130.1.10"
    end_ip = "212.140.1.10"
    output_file = "ips_gen.txt"

    generate_ips(start_ip, end_ip, output_file)
    print(f"Generated IPs have been saved to {output_file}")
