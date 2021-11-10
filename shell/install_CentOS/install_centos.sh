#!/bin/sh

echo **********Start install**********
echo start install python3
sh install_python3.sh
echo end install python3

echo start install git
sh install_git.sh
echo end install git

# need python3
echo start install virtualenv
sh install_virtualenv.sh
echo end install virtualenv

echo start install docker
sh install_docker.sh
echo end install docker

echo **********Install done**********