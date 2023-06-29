#This class is used to create a digital version of the fan so the program
#can better control and replicate the state of the fan.
class Fan:

    #Constructor...
    #
    #No arguement constructor which assigns a default value to the fan_state attribute
    #of 0 to signify off.
    def __init__(self):
        self._fan_state = 0

    #Setter...
    #
    #This setter allows a user or class to set the fan_state attribute.
    #Decision structure ensure the state is either 1 or 0.
    def set_fan_state(self, new_state):
        if new_state == 0:
            self._fan_state = 0
        elif new_state == 1:
            self._fan_state = 1
        else:
            self._fan_state = 0

    #Getter...
    #
    #This getter allows a user or class to get the fan_state attribute's current value.
    def get_fan_state(self):
        return self._fan_state