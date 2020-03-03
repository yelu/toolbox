## cygwin

### sshd

**reset sshd config**

If sshd had been previously installed on the system, the following cleanup should be performed before invoking ssh-host-config:

    # Remove sshd service
    cygrunsrv --stop sshd
    cygrunsrv --remove sshd
    
    # Delete any sshd or related users (such as cyg_server) from /etc/passwd

    # Delete any sshd or relaged users (such as cyg_server) from the system
    net user sshd /delete
    net user cyg_server /delete

**The permissions on the directory /var are not correct**

In cygwin its not possible to change group permissions, until the group is Users or Root. Refer http://stackoverflow.com/questions/17091972/chmod-cannot-change-group-permission-on-cygwin

So you wont be able to change the group permission until you change var's group owner to Users So the best solution is:

    chown :Users /var
    chmod 757 /var
    chmod ug-s /var
    chmod +t /var

**/usr/sbin/sshd can't start the service**

Go to services of windows, find `cygwin sshd`, config username password, start it there.

### file read only

    vi /etc/fstab
    
add following line:

    none /cygdrive cygdrive binary,noacl,posix=0,user 0 0
