#This class is used to create a digital version of the uv light so the program
#can better control and replicate the state of the uv light.
class UV_Light:

    #Constructor...
    #
    #No arguement constructor which assigns a default value to the light_state attribute
    #of 0 to signify off.
    def __init__(self):
        self._light_state = 0

    #Setter...
    #
    #This setter allows a user or class to set the light_state attribute.
    #Decision structure ensure the state is either 1 or 0.
    def set_light_state(self, new_state):
        if new_state == 0:
            self._light_state = 0
        elif new_state == 1:
            self._light_state = 1
        else:
            self._light_state = 0

    #Getter...
    #
    #This getter allows a user or class to get the light_state attribute's current value.
    def get_light_state(self):
        return self._light_state