#!/usr/bin/env python2.7
# -*- encoding: utf-8 -*-

import os
import sys

import time
import datetime
import json
import telnetlib

import requests

GLOBAL_DEFAULT_TIMEOUT = 2


class IPChecker(object):

    def __init__(self, config_path):
        self.config_path = config_path

    @staticmethod
    def load_config(file_path):
        with open(file_path, "r") as f:
            return json.load(f)

    @classmethod
    def check_hosts(cls, host_infos):
        failed_hosts = []
        for host_info in host_infos:
            host = host_info.get("host", "")
            if not host:
                continue
            port = host_info.get("port", 0)
            timeout = host_info.get("timeout", GLOBAL_DEFAULT_TIMEOUT)
            status = cls.test(host, port=port, timeout=timeout)
            if not status:
                failed_hosts.append(host_info)
        return failed_hosts

    @staticmethod
    def test(host, port=0, timeout=2):
        try:
            telnet = telnetlib.Telnet(host=host, port=port, timeout=timeout)
            telnet.close()
        except IOError:
            return False
        else:
            return True

    def report_failed(self, run_time, ignore_hours, sckey, failed_hosts):

        title = "Host报警: {}".format(run_time.strftime("%Y-%m-%d %H:%M"))
        content = ""

        for host in failed_hosts:
            content += "host:{} port:{} timeout:{}\n".format(
                host.get("host", ""),
                host.get("port", 0),
                host.get("timeout", GLOBAL_DEFAULT_TIMEOUT),
            )

        hour = run_time.hour
        if hour in ignore_hours or not sckey:
            return
        self.send_report(title, content, sckey)

    @staticmethod
    def send_report(title, content, sckey):
        url = "https://sc.ftqq.com/{}.send".format(sckey)
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "text": title,
            "desp": content,
        }
        try:
            requests.post(url, data=data, headers=headers, verify=False)
        except Exception:
            pass

    def run(self):
        while True:
            now = datetime.datetime.now()
            config = self.load_config(self.config_path)

            hosts = config.get("hosts", [])
            ignore_hours = set(config.get("ignore", []))
            sckey = config.get("sckey", "")

            if not hosts:
                time.sleep(1800)
                continue
            failed_hosts = self.check_hosts(hosts)
            self.report_failed(now, ignore_hours, sckey, failed_hosts)
            time.sleep(1800)


def run(config_path):
    checker = IPChecker(config_path)
    checker.run()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("command: command config_file")
        exit(-1)

    config_file_path = sys.argv[1]
    if not os.path.isfile(config_file_path):
        print("command: not find config_file")

    run(config_file_path)
