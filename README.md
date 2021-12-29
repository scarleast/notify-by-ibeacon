# notify-by-iBeacon

一个借助iBeacon新信标，判断是否进入、离开某个区域，以发出提醒，以免自己忘记打卡的项目。

思路是：树莓派不断扫描周围iBeacon信标发出的广播数据，当第一次检测到iBeacon节点进入时，触发相应的告警，当检测到iBeacon节点离开后，同样触发告警。

本项目中的告警，只是通过server酱，基于iBeacon信标，可以扩展出相当多的自动化功能，如智能家居等，希望本项目能起到抛砖引玉的作用。

# 依赖

## 硬件平台

一个可以连接互联网的树莓派（带有蓝牙的型号），一个iBeacon信标（某宝搜索iBeacon即可）。

## 软件

请在树莓派上输入一下命令，以安装依赖：

```bash
sudo apt-get -y install python-dev libbluetooth-dev libcap2-bin git
sudo setcap 'cap_net_raw,cap_net_admin+eip' $(readlink -f $(which python))
sudo pip3 install beacontools[scan] requests
```

# 运行

```bash
sudo python3 ble_test.py
```

# 配置文件

```json
{
    "timeout": 60,
    "serverchain_receiver": {
        "SCUXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX": {
            "bt_addr": "XX:XX:XX:XX:XX:XX",
            "uuid": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
            "major": 1,
            "minor": 1
        }
    }
}
```

- timeout：超时时间。即树莓派扫描不到相应iBeacon信标多少秒后，触发提醒。
- serverchain_recerver：使用server酱接收提醒。该字段的value为一个字典，key为server酱的SCKEY，value为iBeacon信标的相关参数。
  - bt_addr：iBeacon节点的mac地址。
  - uuid：希望检测的UUID值。
  - major：用于区分相同UUID值下不同的服务，取值范围0~65535。
  - minor：用于区分相同UUID值、相同major下不同的服务，取值范围0~65535.

> 由于iBeacon信标可以自定义UUID、major、minor，有的iBeacon信标甚至可以广播三组不同的UUID，因此可以扩展出来的玩法也很多。`serverchain_receiver`字段可以配置多个用于提醒的SCKEY，每个SCKEY设置好相应的bt_addr、uuid、major、minor即可。

# 感谢

citruz：[beacontools](https://github.com/citruz/beacontools)

server酱：http://sc.ftqq.com/

