#IMPORTS
#-------------------------------
from dht import DHT11, InvalidChecksum
from fan import Fan
from humidifier import Humidifier
from uv_light import UV_Light
#from water_pump import Water_Pump
from ideal_plant_climate import Ideal_Plant_Climate
from machine import Pin, I2C, ADC
from machine_i2c_lcd import I2cLcd
import machine
import utime
#--------------------------------------------------------------------------------------------
#Pin Assignment
#-------------------------------
DHTPin = Pin(15, Pin.OUT, Pin.PULL_DOWN)            #Temp and Humidity sensor
light_relay = Pin(4, Pin.OUT)                       #Socket A
humidifier_relay = Pin(5, Pin.OUT)                  #Socket C
#pump_relay = Pin(6, Pin.OUT)                       #Socket B
fan_relay = Pin(11, Pin.OUT)                        #Fan
i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=400000)   #LCD

#Wait to help boot...
utime.sleep(2)
#--------------------------------------------------------------------------------------------
#Function Definitions
#-------------------------------
#The read_temp_and_humidity function reads the humidty level and temperature, con-
#verts the temperature from celsius to fahrenheit then returns the two values as a tuple.
def read_temp_and_humidity():
    
    #Create sensorObject to obtain readings.
    sensorObject = DHT11(DHTPin)
        
    #Try block is used in case of faulty pulse reading.
    try:
    
        #This sections reads the values returned from the sensors and covnerts the temp.
        #value into fahrenheit.
        fahr_temp = (sensorObject.temperature / 5 * 9 + 32)
        humidity = (sensorObject.humidity)
              
    except:
            fahr_temp = 99
            humidity = 99
                
    return fahr_temp, humidity

#The main function is made up of the logic used to call all the function neccassary for
#completing the programming task.
def main():

    #Try block is used for pin clean up.
    try:
        #Create a real time clock object and set datetime.
        rtc_object = machine.RTC()
        rtc_object.datetime((2023, 10, 7, 6, 16, 43, 0, 0))

        #Create a fan object.
        fan_object = Fan()

        #Create a humidifier object.
        humidifier_object = Humidifier()

        #Create a UV light object.
        uv_light_object = UV_Light()

        #Create a water pump object.
        #water_pump_object = Water_Pump()

        #Create address object create a lcd object.
        address_object = i2c.scan()[0]
        lcd_object = I2cLcd(i2c, address_object, 2, 16)

        #Create an ideal plant climate object.
        ideal_plant_climate_object = Ideal_Plant_Climate()

        #Create an iteration variable to count iterations.
        iteration = 0

        #Infinite while loop used to iterate the program.
        while True:

            #Create a current time variable and get current time.
            current_time = rtc_object.datetime()

            #Watering Frequency...
            #
            #Decision statement used to determine if it is water time.
            #if current_time[4] % ideal_plant_climate_object.get_watering_frequency() == 0:
                #if iteration < 1:
                    #water_pump_object.set_water_pump_state(1)
                    #iteration += 1
                #else:
                    #water_pump_object.set_water_pump_state(0)
            #else:
                #water_pump_object.set_water_pump_state(0)
                #iteration = 0
                
            #Light On and Off...
            
            #Retrieve and extract the light on hour and minute.
            light_on_time = ideal_plant_climate_object.get_light_on_time()
            light_on_list = light_on_time.split(':')
            
            #Retrieve and extract the light off hour and minute.
            light_off_time = ideal_plant_climate_object.get_light_off_time()
            light_off_list = light_off_time.split(':')
            
            # Current hour > light on hour
            if current_time[4] > int(light_on_list[0]):
                uv_light_object.set_light_state(1)
                
            # Current hour < light on hour
            elif current_time[4] < int(light_on_list[0]):
                
                # Current hour < light off hour
                if current_time[4] < int(light_off_list[0]):
                    uv_light_object.set_light_state(1)
                    
                else:
                    uv_light_object.set_light_state(0)

             
            # Current hour == light on hour
            elif current_time[4] == int(light_on_list[0]):
                
                # Current minute >= light on minute
                if current_time[5] >= int(light_on_list[1]):
                    uv_light_object.set_light_state(1) 
                else:
                    uv_light_object.set_light_state(0)
                  
            # Current hour == light off hour
            elif current_time[4] == int(light_off_list[0]):
                
                # Current minute >= light off minute
                if current_time[5] >= int(light_off_list[1]):
                    uv_light_object.set_light_state(0)
                else:
                    uv_light_object.set_light_state(1)

            #Temperture and Humidity...
            
            #Get the current temp and humidity.
            fahr_temp, humidity = read_temp_and_humidity()
            
            #If the current humidity is less than optimal_hum_min, activate the humidifier.
            if humidity < ideal_plant_climate_object.get_min_humidity():
                humidifier_object.set_humidifier_state(1)
            
            #In all other situation, deactivate the humidifier.
            else:
                humidifier_object.set_humidifier_state(0)
                
            #If humidity is greater than optimal_hum_max, activate the fans.
            if humidity > ideal_plant_climate_object.get_max_humidity():
                fan_object.set_fan_state(1)
                
            #Elif optimal_temp_max is less than current temp, activate fans.
            elif ideal_plant_climate_object.get_max_temperature() < fahr_temp:
                fan_object.set_fan_state(1)
                
            #In any other situation, deactivate fans.
            else:
                fan_object.set_fan_state(0)

            #Format the time for display.
            current_hour = current_time[4]
            if current_hour < 10:
                current_hour = str(current_time[4])
                current_hour = '0' + current_hour
            current_minute = current_time[5]
            if current_minute < 10:
                current_minute = str(current_time[5])
                current_minute = '0' + current_minute
            light_hour = light_on_list[0]
            light_minute = light_on_list[1]
            dark_hour = light_off_list[0]
            dark_minute = light_off_list[1]
        
            #Create formatted string for displaying to LCD and create a list of them.
            current_time_string = 'Current Time:   ' + str(current_hour) + ':' + str(current_minute)
            light_time_string = 'Light On Time:  ' + str(light_hour) + ':' + str(light_minute)
            dark_time_string = 'Light Off Time: ' + str(dark_hour) + ':' + str(dark_minute)
            temperature_string = str(f'Temperature(F):\n {fahr_temp:.0f}')
            humidity_string = str(f'Humidity(%): \n{humidity:.0f}')
            display_list = [current_time_string, light_time_string, dark_time_string,
                            temperature_string, humidity_string]
            
            #Display all information to display.
            for item in display_list:
                lcd_object.clear()
                lcd_object.backlight_on()
                lcd_object.putstr(item)
                utime.sleep(12)

            #decision statements is used to determine how the physical objects represented
            #by the program need to be adjusted to match.
            if uv_light_object.get_light_state() == 1:
                light_relay.value(1)
            else:
                light_relay.value(0)
            if fan_object.get_fan_state() == 1:
                fan_relay.value(1)
            else:
                fan_relay.value(0)
            if humidifier_object.get_humidifier_state() == 1:
                humidifier_relay.value(1)
            else:
                humidifier_relay.value(0)
            #if water_pump_object.get_water_pump_state() == 1:
            #    pump_relay.value(1)
            #else:
            #    pump_relay.value(0)
                
            #Display all information to display.
            #for x in range(6):
                #for item in display_list:
                    #lcd_object.clear()
                    #lcd_object.backlight_on()
                    #lcd_object.putstr(item)
                    #utime.sleep(10)

    finally:
        DHTPin.value(0)         #Temp and Humidity sensor
        light_relay.value(0)    #Lights
        humidifier_relay.value(0)    #Humidifier
        #pump_relay.value(0)    #Water Pump
        fan_relay.value(0)    #Fan
            
#Call the main function if name == '__main__'
if __name__ == '__main__':
    main()
