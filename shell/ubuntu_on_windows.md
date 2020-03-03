## Ubuntu on windows

### start a sshd

    sudo apt-get remove openssh-server
    sudo apt-get install openssh-server
    # disallow root login by setting PermitRootLogin no. Then add a line beneath it that says: AllowUsers yourusername
    # make sure PasswordAuthentication is set to yes if you want to login using a password.
    # Disable privilege separation by adding/modifying : UsePrivilegeSeparation no
    sudo vim /etc/ssh/sshd_config    
    sudo service ssh --full-restart