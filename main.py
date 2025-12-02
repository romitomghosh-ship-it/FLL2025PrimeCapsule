# Import the modules
import machine
import time
import dht
from I2C_LCD import I2CLcd


#DHT11 is the sensor that measures temperature and humidity
DHT11_PIN=2 # The Raspberry Pi Pico pin (GPO) connected to the DHT11 sensor
# Initialize the DHT11 sensor
DHT11=dht.DHT11(machine.Pin(DHT11_PIN))

#i2c is the display in which the temperature and humidity will be displayed
i2c = machine.I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
devices = i2c.scan()

# Define Motor Driver
enb = machine.PWM(machine.Pin(13))
enb.freq(1500)
in3 = machine.Pin(14, machine.Pin.OUT)
in4 = machine.Pin(15, machine.Pin.OUT)

#Define run_fan
def run_fan(speed):
    in3.high()
    in4.low()
    enb.duty_u16(speed)
    
#Define stop_fan    
def stop_fan():
    in3.low()
    in4.low()
    enb.duty_u16(0)

# Read data from the sensor every 2 seconds
while True:
    
    # Measure and display temperature and humidity
    DHT11.measure()
    temp=DHT11.temperature() # Gets the temperature in celcius
    humidity=DHT11.humidity() # Gets the relative humidity in %
    print("Temperature: {:.2f}°C, Humidity: {:.2f}%".format(temp, humidity))
    
    # if humidity is above 50% start fan, if it is below 50% stop fan
    if temp > 25:
        run_fan(65535)
    else:
        stop_fan()
            
    # Show humidity and temperature on display
    if devices != []:
        lcd = I2CLcd(i2c, devices[0], 2, 16)
        lcd.move_to(0, 0)
        lcd.putstr("Temp: {:.2f}°C".format(temp))
        lcd.move_to(0, 1)
        lcd.putstr("Hum: {:.2f}%".format(humidity))
    else:
        print("No address found")    
    
    #Wait 1 seconds until you measure again
    time.sleep(2)


    