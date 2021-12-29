#!/usr/bin/env python3
# coding:utf-8

"""
@author: scarleast
@contact: scarleast@hotmail.com
@software: PyCharm
@file: ble_test.py
@time: 2020/4/19 11:27 下午
"""
import time
from beacontools import BeaconScanner
from requests import Session
from requests.adapters import HTTPAdapter
import json

with open("config.json", "r") as f:
    config = json.loads(f.read())
beacon_nodes = {}
timeout = config.get("timeout")
receivers = config.get("serverchain_receiver")


def push_to_pushbear(sckey, text, desp):
    session = Session()
    session.mount('https://', HTTPAdapter(max_retries=3))
    session.get("https://sc.ftqq.com/{}.send".format(sckey), params={
        "text": text,
        "desp": desp
    }, timeout=5)


def leave_judge_process():
    global beacon_nodes
    print("leave judge process run!")
    while True:
        tmp_timestamp = int(time.time())
        tmp_beacon_nodes = {k: v for k, v in beacon_nodes.items() if v}
        for key, value in tmp_beacon_nodes.items():
            # print("interve:{}, old:{}, new:{}".format(tmp_timestamp - value["additional_info"]["timestamp"],
            #                                           value["additional_info"].get("timestamp"),
            #                                           tmp_timestamp))
            if tmp_timestamp - value["additional_info"]["timestamp"] > timeout:
                print("node:{} leave!".format(key))
                node_info = beacon_nodes.pop(key).get("additional_info")
                for single_receiver, single_config in receivers.items():
                    tmp_bt_addr = single_config.get("bt_addr")
                    tmp_uuid = single_config.get("uuid")
                    tmp_major = single_config.get("major")
                    tmp_minor = single_config.get("minor")

                    # print(node_info)
                    if (tmp_bt_addr, tmp_uuid, tmp_major, tmp_minor) == \
                            (key, node_info.get("uuid"), node_info.get("major"), node_info.get("minor")):
                        print("下班提醒已触发！")
                        try:
                            pass
                            push_to_pushbear(single_receiver, "下班打卡提醒",
                                             "time:{}\n\n下班了也记得打卡呀！".format(time.ctime()))
                        except Exception as e:
                            print(e)
        time.sleep(1)


def callback(bt_addr, rssi, packet, additional_info):
    global beacon_nodes
    # print("addr:{}\nrssi:{}\npacket:{}\nadditon:{}\n\n".format(bt_addr, rssi, packet, additional_info))
    if bt_addr not in beacon_nodes:
        print("node:{} in!".format(bt_addr))

        beacon_nodes.setdefault(bt_addr, {})
        beacon_nodes[bt_addr]["rssi"] = str(rssi)
        beacon_nodes[bt_addr]["packet"] = str(packet)

        beacon_nodes[bt_addr].setdefault("additional_info", additional_info)
        beacon_nodes[bt_addr]["additional_info"]["timestamp"] = int(time.time())

        for single_receiver, single_config in receivers.items():
            tmp_bt_addr = single_config.get("bt_addr")
            tmp_uuid = single_config.get("uuid")
            tmp_major = single_config.get("major")
            tmp_minor = single_config.get("minor")
            if (tmp_bt_addr, tmp_uuid, tmp_major, tmp_minor) == \
                    (bt_addr, additional_info.get("uuid"), additional_info.get("major"), additional_info.get("minor")):
                print("上班提醒已触发！")
                try:
                    pass
                    push_to_pushbear(single_receiver, "上班打卡提醒",
                                     "time:{}\n\n上班了也记得打卡呀！".format(time.ctime()))
                except Exception as e:
                    print(e)

    else:
        beacon_nodes[bt_addr]["additional_info"]["timestamp"] = int(time.time())


def main():
    scanner = BeaconScanner(callback)
    scanner.start()
    leave_judge_process()


if __name__ == "__main__":
    main()
