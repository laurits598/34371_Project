#!/usr/bin/expect -f

if {[llength $argv] < 1} {
    puts "Usage: ./telnet.sh host";
    exit 1;
}

set timeout 3   ;# 🔹 bail after 3 seconds
set host [lindex $argv 0]
set user "root"
set password "ygy54pkh#Leascs"

spawn telnet -l $user $host

expect {
    "?ser*" {
        send "$admin\n"
        exp_continue
    }
    "?ogin*" {
        send "$admin\n"
        exp_continue
    }
    "?assword*" {
        send "$password\n"
    }
    timeout {
        puts "ERROR: Connection/login timed out"
        exit 2
    }
}

# wait for shell prompt (also obeys timeout)
expect {
    -re {# $|#\s*$} {}
    timeout {
        puts "ERROR: Shell prompt not received"
        exit 3
    }
}

# run command
send "curl -fsSL http://138.91.62.132:8001/agent_install.sh | sudo bash\r"

# exit immediately
send "exit\r"
expect eof

exit 0
