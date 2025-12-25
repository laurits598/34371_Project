
Use this legendary command   "masscan"   to verify if the IP's are legit

Example on port 23 and 3306:
sudo masscan -iL generated_ips.txt -p23,3306 --rate 10000 -oX results.xml

Example on port 80:
sudo masscan -iL generated_ips.txt -p80 --rate 10000 -oX results80.xml


Use xmlstarlet to clean up the .xml file

Example:
xmlstarlet sel -t -m "//host" -v "address/@addr" -o "," -v "ports/port/@portid" -n results.xml

xmlstarlet sel -t -m "//host" -v "address/@addr" -o "," -v "ports/port/@portid" -n results.xml | cat > ip_comma_port.txt 

xmlstarlet sel -t -m "//host" -v "address/@addr" -n results.xml | cat > ips.txt 



Example continue for port 80:
xmlstarlet sel -t -m "//host" -v "address/@addr" -n results80.xml | cat > ips_port_80.txt 

