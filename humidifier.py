#This class is used to create a digital version of the Humidifier so the program
#can better control and replicate the state of the Humidifier.
class Humidifier:

    #Constructor...
    #
    #No arguement constructor which assigns a default value to the humidifier_state attribute
    #of 0 to signify off.
    def __init__(self):
        self._humidifier_state = 0

    #Setter...
    #
    #This setter allows a user or class to set the humidifier_state attribute.
    #Decision structure ensure the state is either 1 or 0.
    def set_humidifier_state(self, new_state):
        if new_state == 0:
            self._humidifier_state = 0
        elif new_state == 1:
            self._humidifier_state = 1
        else:
            self._humidifier_state = 0

    #Getter...
    #
    #This getter allows a user or class to get the humidifier_state attribute's current value.
    def get_humidifier_state(self):
        return self._humidifier_state