
## Cool comomands
lau@LinuxVM:~$ curl https://ipinfo.io/ip
<IP>

# Masscan

Use this legendary command   "masscan"   to verify if the IP's are legit

Example on port 23 and 3306:
sudo masscan -iL generated_ips.txt -p23 --rate 10000 -oJ valid_ips.json

Example on port 80:
sudo masscan -iL generated_ips.txt -p80 --rate 10000 -oX results80.xml

## Masscan Output Formats

Masscan supports the following output formats:

- **XML** (`-oX`)
- **JSON** (`-oJ`)
- **Binary** (`-oB`)
- **List (plain text)** (`-oL`)
- **Grepable** (`-oG`)


# Other interesting ports
## High-Risk / “Should Almost Never Be Open”
These are comparable to Telnet in how unsafe they are.

### 21 – FTP
Credentials sent in cleartext
Often anonymous or weak credentials

### 513 / 514 – rlogin / rsh
Legacy remote shells with trust-based auth

### 109 / 110 – POP3
Cleartext email credentials

### 143 – IMAP
Same issue unless explicitly using TLS

### 2049 – NFS
Can expose entire filesystems if misconfigured

### 512 – rexec
Legacy remote command execution



Use xmlstarlet to clean up the .xml file

### Example:
xmlstarlet sel -t -m "//host" -v "address/@addr" -o "," -v "ports/port/@portid" -n results.xml

xmlstarlet sel -t -m "//host" -v "address/@addr" -o "," -v "ports/port/@portid" -n results.xml | cat > ip_comma_port.txt 

xmlstarlet sel -t -m "//host" -v "address/@addr" -n results.xml | cat > ips.txt 

### Example continue for port 80:
xmlstarlet sel -t -m "//host" -v "address/@addr" -n results80.xml | cat > ips_port_80.txt 


# Shell script login
sudo apt update
sudo apt install expect -y

