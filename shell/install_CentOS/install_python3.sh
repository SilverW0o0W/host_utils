#!/bin/sh
yum install openssl-devel bzip2-devel expat-devel gdbm-devel readline-devel sqlite-devel
wget https://www.python.org/ftp/python/3.7.9/Python-3.7.9.tgz
tar -zxvf Python-3.7.9.tgz
cd Python-3.7.9/ || exit
mkdir /usr/local/python3
./configure -prefix=/usr/local/python3
make && make install
ln -s /usr/local/python3/bin/python3 /usr/bin/python3
ln -s /usr/local/python3/bin/pip3 /usr/bin/pip3
