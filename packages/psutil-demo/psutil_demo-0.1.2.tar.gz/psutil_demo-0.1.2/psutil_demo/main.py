import datetime
from pprint import pprint
from time import sleep

import psutil


class Monitor:

    def cpu(self):
        """获取cpu的信息"""
        data = dict(
            percent_avg=psutil.cpu_percent(interval=0, percpu=False),
            percent_per=psutil.cpu_percent(interval=0, percpu=True),
            num_p=psutil.cpu_count(logical=False),  # 核心数量
            num_l=psutil.cpu_count(logical=True)
        )
        return data

    def mem(self):
        """获取内存信息"""
        data = dict(
            total=round(psutil.virtual_memory().total / 1024 / 1024, 2),
            used=round(psutil.virtual_memory().used / 1024 / 1024, 2),
        )
        return data

    def net(self):
        """获取网卡信息(适配器名称，ipv4，收发数据流等)"""
        address = psutil.net_if_addrs()  # ip
        address_info = {
            k: [
                dict(
                    family=data.family.name,
                    addr=data.address,
                    netmask=data.netmask,
                    broadcast=data.broadcast,
                )
                for data in v if data.family.name == 'AF_INET'
            ][0]
            for k, v in address.items()
        }
        io = psutil.net_io_counters(pernic=True)
        rs_data = [
            dict(
                name=k,
                bytes_sent=v.bytes_sent,
                bytes_recv=v.bytes_recv,
                packets_sent=v.packets_sent,
                packets_recv=v.packets_recv,
                **address_info[k]
            )
            for k, v in io.items()
        ]
        return rs_data

    def disk(self):
        """获取磁盘信息"""
        io = psutil.disk_partitions()
        rs_data = [
            dict(
                disk_total=str(int(psutil.disk_usage(i.device).total / (1024.0 * 1024.0 * 1024.0))) + "G",
                disk_path=i.device,
                disk_used=str(int(psutil.disk_usage(i.device).used / (1024.0 * 1024.0 * 1024.0))) + "G",
                disk_free=str(int(psutil.disk_usage(i.device).free / (1024.0 * 1024.0 * 1024.0))) + "G"
            )
            for i in io
        ]
        return rs_data

    def sys_dt(self):
        """获取系统时间"""
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def print_msg(msg):
    print('{}'.format(msg))


if __name__ == '__main__':
    m = Monitor()
    # while True:
    #     sleep(1)
    #     print(m.cpu())
    #     print(m.mem())
    #     print(m.disk())
    #     pprint(m.net())
