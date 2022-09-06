import platform
from time import time
from subprocess import Popen, PIPE
from ipaddress import ip_address

result = {'Доступные узлы': '', 'Недоступные узлы': ''}


def check_is_ip(value):
    try:
        ipv4 = ip_address(value)
    except ValueError:
        raise Exception('Некорректный ip адрес')
    return ipv4


def host_ping(hosts, get_list=False):
    print(f'тут будем проверять адреса')

    for host in hosts:
        try:
            ipv4 = check_is_ip(host)
        except Exception as e:
            ipv4 = host

        param = "-n" if platform.system().lower() == 'windows' else "-c"
        command = ["ping", param, "2", host]
        process = Popen(command, stdout=PIPE, stderr=PIPE)

        process.communicate()

        if process.returncode == 0:
            result['Доступные узлы'] += f'{ipv4}\n'
            res_string = f'{ipv4} -- узел доступен'
        else:
            result['Недоступные узлы'] += f'{ipv4}\n'
            res_string = f'{ipv4} -- узел недоступен'
        if not get_list:
            print(res_string)

    if get_list:
        return result


if __name__ == '__main__':
    hosts_list = ["google.com", "a", '192.168.1.1', '87.250.250.242', 'ya.ru']
    start = time()
    host_ping(hosts_list)
    end = time()
    print(f'{int(end-start)}')
