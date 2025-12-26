#!/usr/bin/expect -f
if {[llength $argv] < 1} {
    puts "Usage: ./telnet.sh host";
    exit 1;
}
set timeout 10
set host [lindex $argv 0]
set user "admin"
set password "password"
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
        interact
        exit 0;
    }
}
exit 1