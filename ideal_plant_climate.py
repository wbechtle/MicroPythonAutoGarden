#This class is used to create a digital version of the ideal plant climate so the program
#can better control and replicate the state of the ideal plant climate.
class Ideal_Plant_Climate:

    #Constructor...
    #
    #No arguement constructor which assigns a default value to the max_temperature 
    #attribute of 0 to signify off.
    def __init__(self):
        self._max_temperature = 75
        self._max_humidity = 40
        self._min_temperature = 65
        self._min_humidity = 30
        self._light_on_time = '09:00'
        self._light_off_time = '19:00'
        self._watering_frequency = 4

    #Getter...
    #
    #This getter allows a user or class to get the max_temperature attribute's current value.
    def get_max_temperature(self):
        return self._max_temperature
    #
    #This getter allows a user or class to get the max_humidity attribute's current value.
    def get_max_humidity(self):
        return self._max_humidity
    #
    #This getter allows a user or class to get the min_temperature attribute's current value.
    def get_min_temperature(self):
        return self._min_temperature
    #
    #This getter allows a user or class to get the min_humidity attribute's current value.
    def get_min_humidity(self):
        return self._min_humidity
    #
    #This getter allows a user or class to get the light_on_time attribute's current value.
    def get_light_on_time(self):
        return self._light_on_time
    #
    #This getter allows a user or class to get the light_off_time attribute's current value.
    def get_light_off_time(self):
        return self._light_off_time
    #
    #This getter allows a user or class to get the watering_frequency attribute's current value.
    def get_watering_frequency(self):
        return self._watering_frequency