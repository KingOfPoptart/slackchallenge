# Apache2 Install

* Initial issue
    ```
    root@ip-172-31-255-28:~# apt-get install apache2
    Reading package lists... Error!
    E: Write error - write (28: No space left on device)
    E: Can't mmap an empty file
    E: Failed to truncate file - ftruncate (9: Bad file descriptor)
    E: The package lists or status file could not be parsed or opened.
    ```
* Out of disk space 
    ```
    root@ip-172-31-255-28:~# df -h
    Filesystem      Size  Used Avail Use% Mounted on
    udev            240M   12K  240M   1% /dev
    tmpfs            49M  340K   49M   1% /run
    /dev/xvda1      7.8G  7.8G     0 100% /
    none            4.0K     0  4.0K   0% /sys/fs/cgroup
    none            5.0M     0  5.0M   0% /run/lock
    none            245M     0  245M   0% /run/shm
    none            100M     0  100M   0% /run/user
    ```
* However, its probably just a hanging file descriptor since there doesn't seem to be a large file anywhere on disk
    ```
    root@ip-172-31-255-28:~# du -h --max-depth=1 /
    61M	/lib
    32K	/home
    344K	/run
    9.6M	/bin
    0	/sys
    240M	/var
    0	/proc
    512M	/usr
    16K	/lost+found
    4.0K	/opt
    4.0K	/tmp
    4.0K	/mnt
    16K	/root
    25M	/boot
    4.0K	/srv
    4.0K	/lib64
    5.6M	/etc
    9.4M	/sbin
    12K	/dev
    4.0K	/media
    861M	/
    ```
* Killed process holding onto large file
    ```
    root@ip-172-31-255-28:~# lsof -nP | grep -i deleted
    named     1488           root    3w      REG              202,1 7436824576      26446 /tmp/tmp.e5ZgvyaZzc (deleted)
    root@ip-172-31-255-28:~# kill -9 1488
    root@ip-172-31-255-28:~# df -h
    Filesystem      Size  Used Avail Use% Mounted on
    udev            240M   12K  240M   1% /dev
    tmpfs            49M  340K   49M   1% /run
    /dev/xvda1      7.8G  817M  6.6G  11% /
    none            4.0K     0  4.0K   0% /sys/fs/cgroup
    none            5.0M     0  5.0M   0% /run/lock
    none            245M     0  245M   0% /run/shm
    none            100M     0  100M   0% /run/user
    ```
* Now can't resolve hostnames
    ```
    root@ip-172-31-255-28:~# ping us-east-1.ec2.archive.ubuntu.com
    ping: unknown host us-east-1.ec2.archive.ubuntu.com

    root@ip-172-31-255-28:~# ping 172.217.7.228
    PING 172.217.7.228 (172.217.7.228) 56(84) bytes of data.
    64 bytes from 172.217.7.228: icmp_seq=1 ttl=48 time=1.02 ms
    --- 172.217.7.228 ping statistics ---
    2 packets transmitted, 2 received, 0% packet loss, time 1001ms
    ```
* Fixed resolve.conf
    ```
    root@ip-172-31-255-28:~# cat /etc/resolv.conf
    nameserver 8.8.8.8
    ```
* Able to install apache2, but service failed to start because it couldn't bind to the address
    ```
    apt-get update
    apt-get install apache2 --fix-missing
    ```
* Killed nc process listening on http port
    ```
    root@ip-172-31-255-28:~# lsof -n | grep LISTEN
    sshd      1265           root    3u     IPv4               9600      0t0        TCP *:ssh (LISTEN)
    sshd      1265           root    4u     IPv6               9605      0t0        TCP *:ssh (LISTEN)
    nc        1484           root    3u     IPv4              10504      0t0        TCP *:http (LISTEN)
    root@ip-172-31-255-28:~# kill -9 1484
    ```
* Started the apache2 service - service started and worked, but threw errors
    ```
    root@ip-172-31-255-28:~# service apache2 start
    * Starting web server apache2                                                                                               AH00557: apache2: apr_sockaddr_info_get() failed for ip-172-31-255-28
    AH00558: apache2: Could not reliably determine the server's fully qualified domain name, using 127.0.0.1. Set the 'ServerName' directive globally to suppress this message
    ```
* Added this line to `/etc/apache2/apache2.conf`
    ```
    ServerName slackchallenge
    ```
* Restarted apache2
    ```
    root@ip-172-31-255-28:~# service apache2 restart
    * Restarting web server apache2           [ OK ]
    ```
* Website's up at http://34.228.161.169 and Bob's your uncle.