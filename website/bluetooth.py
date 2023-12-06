import subprocess
import time

def blue_it():
    status = subprocess.call('ls /dev/input/event0 2>/dev/null', shell=True)
    while status == 0:
        print("Bluetooth UP")
        print(status)
        result = subprocess.run('hcitool rssi BC:09:63:44:CC:74', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:            
            print("Output:")
            print(result.stdout)
        else:
            print("Error:")
            print(result.stderr)
            waiting();
        time.sleep(1)
        status = subprocess.call('ls /dev/input/event0 2>/dev/null', shell=True)
    else:
        waiting()

def waiting():
    status = subprocess.run('hcitool rssi BC:09:63:44:CC:74', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    while status.returncode != 0:
        print("Bluetooth DOWN")
        print(status)
        subprocess.call('~/scripts/autopair', shell=True)
        time.sleep(5)
        status = subprocess.run('hcitool rssi BC:09:63:44:CC:74', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    else:
        blue_it()
    
        
if __name__ == '__main__':
    waiting()
