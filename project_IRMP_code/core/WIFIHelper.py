import subprocess

"""Помошник по подключению wifi"""


class WIFIController:

    @staticmethod
    def what_wifi():
        process = subprocess.run(['nmcli', '-t', '-f', 'ACTIVE,SSID', 'dev', 'wifi'], stdout=subprocess.PIPE)
        if process.returncode == 0:
            return process.stdout.decode('utf-8').strip().split(':')[1]
        else:
            return ''

    @staticmethod
    def is_connected_to(ssid: str):
        return WIFIController.what_wifi() == ssid

    @staticmethod
    def scan_wifi():
        process = subprocess.run(['nmcli', '-t', '-f', 'SSID,SECURITY,SIGNAL', 'dev', 'wifi'], stdout=subprocess.PIPE)
        if process.returncode == 0:
            return process.stdout.decode('utf-8').strip().split('\n')
        else:
            return []

    @staticmethod
    def is_wifi_available(ssid: str):
        return False
        return ssid in [x.split(':')[0] for x in WIFIController.scan_wifi()]

    @staticmethod
    def connect_to(ssid: str, password: str):
        if not WIFIController.is_wifi_available(ssid):
            return False
        subprocess.call(['nmcli', 'd', 'wifi', 'connect', ssid, 'password', password])
        return WIFIController.is_connected_to(ssid)

    @staticmethod
    def connect_to_saved(ssid: str):
        if not WIFIController.is_wifi_available(ssid):
            return False
        subprocess.call(['nmcli', 'c', 'up', ssid])
        return WIFIController.is_connected_to(ssid)
