#!/usr/bin/expect -f
if {[llength $argv] < 1} {
    puts "Usage: ./telnet.sh host"
    exit 1
}

set timeout 10
set host [lindex $argv 0]
set user "admin"
set password "password"

spawn telnet -l $user $host

expect {
    "?ser*" {
        send "$user\r"
        exp_continue
    }
    "?ogin*" {
        send "$user\r"
        exp_continue
    }
    "?assword*" {
        send "$password\r"
    }
}

# ---- ADDITION STARTS HERE ----

# Wait for shell prompt
expect {
    -re {[#>$] $} {}
    timeout { puts "No shell prompt"; exit 1 }
}

# Run command
send "touch test_file\r"

# Wait for command to finish
expect -re {[#>$] $}

# Exit cleanly
send "exit\r"
expect eof

# ---- ADDITION ENDS HERE ----
