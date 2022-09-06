import platform
import threading
from time import time
from subprocess import Popen, PIPE
from ipaddress import ip_address
from threading import Thread

SHARED_RESOURCE_LOCK = threading.Lock()
result = {'Доступные узлы': '', 'Недоступные узлы': ''}

def check_is_ip(value):
    try:
        ipv4 = ip_address(value)
    except ValueError:
        raise Exception('Некорректный ip адрес')
    return ipv4


def thread_ping(ipv4, result, get_list=False):
    param = "-n" if platform.system().lower() == 'windows' else "-c"
    command = ["ping", param, "2", str(ipv4)]
    response = Popen(command, stdout=PIPE, stderr=PIPE)

    response.communicate()

    if response.returncode == 0:
        with SHARED_RESOURCE_LOCK:
            result['Доступные узлы'] += f'{ipv4}\n'
            res_string = f'{ipv4} -- узел доступен'
            if not get_list:
                print(res_string)
            return res_string
    else:
        with SHARED_RESOURCE_LOCK:
            result['Недоступные узлы'] += f'{ipv4}\n'
            res_string = f'{ipv4} -- узел недоступен'
            if not get_list:
                print(res_string)
            return res_string

def host_ping(hosts, get_list=False):
    print(f'начинаем проверку')
    threads = []
    for host in hosts:
        try:
            ipv4 = check_is_ip(host)
        except Exception as e:
            ipv4 = host

        th = Thread(target=thread_ping, args=(ipv4, result, get_list))
        th.start()
        threads.append(th)

    for th in threads:
        th.join()

    if get_list:
        return result


if __name__ == '__main__':
    hosts_list = ["google.com", "a", '192.168.1.1', '87.250.250.242', 'ya.ru']
    start = time()
    host_ping(hosts_list)
    end = time()
    print(f'total time: {int(end-start)}')

