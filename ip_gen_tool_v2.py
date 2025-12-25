import random

with open("generated_ips.txt", "w") as f:
    for _ in range(1000000):
        ip = ".".join(str(random.randint(1, 254)) for _ in range(4))
        f.write(ip + "\n")
#

