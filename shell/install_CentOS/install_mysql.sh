#!/bin/sh
wget http://repo.mysql.com/mysql-community-release-el7-5.noarch.rpm
rpm -ivh mysql-community-release-el7-5.noarch.rpm
yum -y update
yum -y install mysql-server
rm -f mysql-community-release-el7-5.noarch.rpm

chown -R mysql:mysql /var/lib/mysql
mysqld --initialize
