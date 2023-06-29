#IMPORTS
#-------------------------------
from dht import DHT11, InvalidChecksum
from fan import Fan
from humidifier import Humidifier
from uv_light import UV_Light
from water_pump import Water_Pump
from ideal_plant_climate import Ideal_Plant_Climate
from machine import Pin, I2C, ADC
from machine_i2c_lcd import I2cLcd
import machine
import utime
#--------------------------------------------------------------------------------------------
#Pin Assignment
#-------------------------------
DHTPin = Pin(15, Pin.OUT, Pin.PULL_DOWN)            #Temp and Humidity sensor
relay_a_pin = Pin(4, Pin.OUT)                       #Lights
relay_b_pin = Pin(5, Pin.OUT)                       #Humidifier
relay_c_pin = Pin(6, Pin.OUT)                       #Water Pump
relay_d_pin = Pin(11, Pin.OUT)                      #Fan
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
        
    except  (InvalidPulseCount):
        
        #Recursively try again until success.
        read_temp_and_humidity()
        
    
    return fahr_temp, humidity

#The main function is made up of the logic used to call all the function neccassary for
#completing the programming task.
def main():

    #Try block is used for pin clean up.
    try:
        #Create a real time clock object and set datetime.
        rtc_object = machine.RTC()
        rtc_object.datetime((2023, 3, 28, 1, 11, 59, 0, 0))

        #Create a fan object.
        fan_object = Fan()

        #Create a humidifier object.
        humidifier_object = Humidifier()

        #Create a UV light object.
        uv_light_object = UV_Light()

        #Create a water pump object.
        water_pump_object = Water_Pump()

        #Create address object create a lcd object.
        address_object = i2c.scan()[0]
        lcd_object = I2cLcd(i2c, address_object, 2, 16)

        #Create a ideal plant climate object.
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
            if current_time[4] % ideal_plant_climate_object.get_watering_frequency() == 0:
                if iteration < 1:
                    water_pump_object.set_water_pump_state(1)
                    iteration += 1
                else:
                    water_pump_object.set_water_pump_state(0)
            else:
                water_pump_object.set_water_pump_state(0)
                iteration = 0
                #
            #Light On and Off...
            #
            #Retrieve and extract the light on hour and minute.
            light_on_time = ideal_plant_climate_object.get_light_on_time()
            light_on_list = light_on_time.split(':')
            #
            #Retrieve and extract the light off hour and minute.
            light_off_time = ideal_plant_climate_object.get_light_off_time()
            light_off_list = light_off_time.split(':')
            #
            #If light_on_hour is less than current_time hour and current_time
            #hour is less than light_off_hour, activate the lights.
            if int(light_on_list[0]) < current_time[4] < int(light_off_list[0]):
                uv_light_object.set_light_state(1)
                #
            #Elif light_on_hour is equal to current_time hour, proceed to
            #next condition.
            elif int(light_on_list[0]) == current_time[4]:
                #
                #If start_of_light_minute is less then current_time minute and
                #current_time minute is less then end_of_light_minute, activate
                #the lights.
                if int(light_on_list[1]) < current_time[5] < int(light_off_list[1]):
                    uv_light_object.set_light_state(1)
                #    
                #In any other situation, deactivate lights.
                else:
                    uv_light_object.set_light_state(0)
                    #
            #Elif end_of_light_hour is equal to current_time hour, check next
            #condition.
            elif int(light_off_list[0]) == current_time[4]:
                #
                #If current_time minutes is less than end_of_light_minutes, activate
                #the lights.
                if current_time[5] < int(light_off_list[1]):
                    uv_light_object.set_light_state(1)
                    #
                #In any other situation, deactivate the lights.
                else:
                    uv_light_object.set_light_state(0)
                    #
            #In any other situation, deactivate the lights.
            else:  
                uv_light_object.set_light_state(0)

            #Temperture and Humidity...
            #
            #Get the current temp and humidity.
            fahr_temp, humidity = read_temp_and_humidity()
            #
            #If the current humidity is less than optimal_hum_min, activate the humidifier
            #and wait a minute.
            if humidity < ideal_plant_climate_object.get_min_humidity():
                humidifier_object.set_humidifier_state(1)
                #
            #In all other situation, deactivate the humidifier.
            else:
                humidifier_object.set_humidifier_state(0)
                #
            #If humidity is greater than optimal_hum_max, activate the fans.
            if humidity > ideal_plant_climate_object.get_max_humidity():
                fan_object.set_fan_state(1)
                #
            #Elif optimal_temp_max is less than current temp, activate fans.
            elif ideal_plant_climate_object.get_max_temperature() < fahr_temp:
                fan_object.set_fan_state(1)
                #
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
            temperature_string = f'Temperature(F):\n {fahr_temp:.0f}'
            humidity_string = f'Humidity(%): \n{humidity:.0f}'
            display_list = [current_time_string, light_time_string, dark_time_string,
                            temperature_string, humidity_string]
            
            #Display all information to display.
            for item in display_list:
                lcd_object.clear()
                lcd_object.backlight_on()
                lcd_object.putstr(item)
                utime.sleep(10)

            #decision statements is used to determine how the physical objects represented
            #by the program need to be adjusted to match.
            if uv_light_object.get_light_state() == 1:
                relay_a_pin.value(1)
            else:
                relay_a_pin.value(0)
            if fan_object.get_fan_state() == 1:
                relay_d_pin.value(1)
            else:
                relay_d_pin.value(0)
            if humidifier_object.get_humidifier_state() == 1:
                relay_b_pin.value(1)
            else:
                relay_b_pin.value(0)
            if water_pump_object.get_water_pump_state() == 1:
                relay_c_pin.value(1)
            else:
                relay_c_pin.value(0)
                
            #Display all information to display.
            for x in range(6):
                for item in display_list:
                    lcd_object.clear()
                    lcd_object.backlight_on()
                    lcd_object.putstr(item)
                    utime.sleep(10)

    finally:
        DHTPin.value(0)         #Temp and Humidity sensor
        relay_a_pin.value(0)    #Lights
        relay_b_pin.value(0)    #Humidifier
        relay_c_pin.value(0)    #Water Pump
        relay_d_pin.value(0)    #Fan
            
#Call the main function if name == '__main__'
if __name__ == '__main__':
    main()