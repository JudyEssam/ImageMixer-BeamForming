class Antenna:

    def __init__(self, is_isotropic, phase, gain=None):
        if is_isotropic:
            self.gain=1 #uniformly trasnmit the signal
        else:
            self.gain= gain   #determine how much it will attenuate or amplify the signal

        self.phase=phase    #there's already interinsic phase shift due to spacing and exterinsic phase shift
        #applying phase shift to the elements (steering angle) change the direction of the beam (beam_angle)

 


        