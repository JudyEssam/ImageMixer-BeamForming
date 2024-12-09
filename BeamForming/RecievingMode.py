
import numpy as np
from BeamSimulator import BeamForming


class RecievingMode(BeamForming):
    def __init__(self):
        super.__init__(self)

    def find_DOA(self): #for Receiving mode only- Get Direction of arrival (we don't know the beam angle)
        recieved_signal= self.apply_signal_to_array('R')
        elements_num,spacing,_= self._array.get_array_factor()
        theta_scan = np.linspace(-1*np.pi, np.pi, 1000) # 1000 different thetas between -180 and +180 degrees
        results = []
        #These weights align the phases of incoming signals from different directions.
        for theta_i in theta_scan:
            weights = np.exp(-2j * np.pi * spacing * np.arange(elements_num) * np.sin(theta_i)) # Conventional, aka delay-and-sum, beamformer
            X_weighted = weights.conj().T @ recieved_signal # apply our weights. (i.e., perform the beamforming)
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