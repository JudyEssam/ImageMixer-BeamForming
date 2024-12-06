import numpy as np
class BeamForming:
    def __init__(self, array, signal):
        self._signal= signal
        self._array=array
        self._resulted_signal=None
    
    def apply_signal_to_array(self):
        steer_vector = self._array.get_steer_vector()
        steer_vector = steer_vector.reshape(-1,1) # make s a column vector nx1
        signal = self._signal.reshape(1,-1) # make signal a row vector 1 X no_of_sampling points
        #each row correspond to the signal recieved/transmitted by one element in the array
        self._resulted_signal= steer_vector @ signal #shape= no_of_elements*no_of_samples
        #apply noise to the signal
        noise = np.random.randn( self._resulted_signal.shape) + 1j*np.random.randn(self._resulted_signal.shape)
        self._resulted_signal=  self._resulted_signal + 0.5*noise 
    
    def find_DOA(self): #for Receiving mode only- Get Direction of arrival (we don't know the beam angle)
        elements_num,spacing,_= self._array.get_array_factor()
        theta_scan = np.linspace(-1*np.pi, np.pi, 1000) # 1000 different thetas between -180 and +180 degrees
        results = []
        #These weights align the phases of incoming signals from different directions.
        for theta_i in theta_scan:
            weights = np.exp(-2j * np.pi * spacing * np.arange(elements_num) * np.sin(theta_i)) # Conventional, aka delay-and-sum, beamformer
            X_weighted = weights.conj().T @ self._resulted_signal # apply our weights. (i.e., perform the beamforming)
            results.append(10*np.log10(np.var(X_weighted))) # power in signal, in dB so its easier to see small and large lobes at the same time
        results -= np.max(results) # normalize (optional)

        # print angle that gave us the max value
        print(theta_scan[np.argmax(results)] * 180 / np.pi) 
        #Graphing DOA
        # plt.plot(theta_scan*180/np.pi, results) # lets plot angle in degrees
        # plt.xlabel("Theta [Degrees]")
        # plt.ylabel("DOA Metric")
        # plt.grid()
        # plt.show()

    def find_beam_pattern(self):
        pass

    def find_interference_map(self):
        pass

