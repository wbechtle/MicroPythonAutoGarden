#This class is used to create a digital version of the water pump so the program
#can better control and replicate the state of the water pump.
class Water_Pump:

    #Constructor...
    #
    #No arguement constructor which assigns a default value to the water_pump_state attribute
    #of 0 to signify off.
    def __init__(self):
        self._water_pump_state = 0

    #Setter...
    #
    #This setter allows a user or class to set the water_pump_state attribute.
    #Decision structure ensure the state is either 1 or 0.
    def set_water_pump_state(self, new_state):
        if new_state == 0:
            self._water_pump_state = 0
        elif new_state == 1:
            self._water_pump_state = 1
        else:
            self._water_pump_state = 0

    #Getter...
    #
    #This getter allows a user or class to get the water_pump_state attribute's current value.
    def get_water_pump_state(self):
        return self._water_pump_state