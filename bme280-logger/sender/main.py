import time
import os, json
from sensors import growbme280
import requests

bme280 = growbme280()

function_url = os.getenv("FUNCTION_URL")  # change this on each Pi
sensor_name = os.getenv("SENSOR")
sample_duration = 30  # seconds

if function_url == None:
    sys.stderr.write("env-var FUNCTION_URL is required i.e. http://192.168.0.21:8080/function/submit-sample")
    os.exit(1)

if sensor_name == None:
    sys.stderr.write("env-var SENSOR is required i.e. shed1")
    os.exit(1)

def get_cpu_temp():
    path="/sys/class/thermal/thermal_zone0/temp"
    f = open(path, "r")
    temp_raw = int(f.read().strip())
    temp_cpu = float(temp_raw / 1000.0)
    return temp_cpu

try:
    while True:
        print("Gathering sensor data.")
        temp_cpu = get_cpu_temp()
        readings = bme280.get_readings()
        readings["sensor"] = sensor_name
        readings["cpu_temperature"] = temp_cpu
        readings["iso_time"] = time.ctime()

        try:
          requests.post(function_url, data=json.dumps(readings), headers={"Content-type": "application/json"})
          print("Sent to function.. OK")

        except Exception as e:
          print(e)
          continue
        time.sleep(sample_duration)

except KeyboardInterrupt:
    pass
