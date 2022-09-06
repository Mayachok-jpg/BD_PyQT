from ipaddress import ip_address
from tabulate import tabulate
from hw_01_thread import host_ping, check_is_ip
# from hw_01 import host_ping
from pprint import pprint


def host_range_ping(get_list=False):

    while True:
        start_ip = input('Введите начальный адрес: ')
        try:
            ipv4_start = check_is_ip(start_ip)
            last_oct = int(start_ip.split('.')[3])
            break
        except Exception as e:
            print(e)

    while True:
        end_ip = input('Сколько адресов проверить? : ')
        if not end_ip.isnumeric():
            print('нужно число')
        else:
            if (last_oct + int(end_ip)) > 256:
                print(f'нужно число меньше {256- last_oct}')
            else:
                break
    data = [ipv4_start + i for i in range(0, int(end_ip))]
    # print(data)
    return host_ping(data, get_list)



def host_range_ping_tab():
    res = host_range_ping(get_list=True)
    print(tabulate([res], headers='keys', tablefmt="pipe", stralign="center"))
    # print(res)


# host_range_ping()
host_range_ping_tab()