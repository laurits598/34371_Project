import pexpect
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

PROMPT = r"[#>$] $"

class TelnetDevice:
    def __init__(self, host, user, password, timeout=10):
        self.host = host
        self.user = user
        self.password = password
        self.timeout = timeout
        self.child = None

    def connect(self):
        logging.info("Connecting to %s", self.host)
        self.child = pexpect.spawn(
            f"telnet -l {self.user} {self.host}",
            timeout=self.timeout,
            encoding="utf-8"
        )

        self.child.expect("assword:")
        self.child.sendline(self.password)
        self.child.expect(PROMPT)

    def run(self, cmd):
        logging.info("Running: %s", cmd)
        self.child.sendline(cmd)
        self.child.expect(PROMPT)
        return self.child.before

    def close(self):
        self.child.sendline("exit")
        self.child.expect(pexpect.EOF)

if __name__ == "__main__":
    host = sys.argv[1]
    dev = TelnetDevice(host, "admin", "password")

    try:
        dev.connect()
        #dev.run("touch test_file")
    except Exception as e:
        logging.error("FAILED: %s", e)
        sys.exit(1)
    finally:
        dev.close()
