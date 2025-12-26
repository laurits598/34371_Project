import random

def generate_ips(num_ips):
    with open("ip_data_files/generated_ips.txt", "w") as f:
        for _ in range(num_ips):
            ip = ".".join(str(random.randint(1, 254)) for _ in range(4))
            f.write(ip + "\n")
    

#generate_ips(1000000)