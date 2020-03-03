# start ssh server on bash on windows
sudo apt-get remove openssh-server
sudo apt-get install openssh-server
# make sure PasswordAuthentication is set to yes if you want to login using a password
sudo vim /etc/ssh/sshd_config
# full restart
sudo service ssh --full-restart

# install git
sudo apt-get install git

# download linux env files
https://bitbucket.org/yelu27/devbox/src/549783622b1e8a624c916dea06e5100e2a983280/shell/.vimrc
https://bitbucket.org/yelu27/devbox/src/549783622b1e8a624c916dea06e5100e2a983280/shell/.inputrc
https://bitbucket.org/yelu27/devbox/src/549783622b1e8a624c916dea06e5100e2a983280/shell/.bash_profile

# install build-essential
sudo apt-get install build-essential
sudo apt-get install python-pip

# install anaconda, create an virtualenv with py2.7
bash Anaconda3-4.3.1-Linux-x86_64.sh
conda create --name py27 python=2.7

# install tensorflow, 1.0, py27, cpu only
source activate py27
pip install --ignore-installed --upgrade https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-1.0.1-cp27-none-linux_x86_64.whl

# install cython and make it use gcc 4.9
sudo apt-get install g++
sudo add-apt-repository ppa:ubuntu-toolchain-r/test
sudo apt-get update
sudo apt-get install gcc-4.9 g++-4.9
pip install cython
export CC=g++-4.9