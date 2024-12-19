from PyQt5.QtCore import QObject, pyqtSignal



class SignalEmitter(QObject):
    function_done = pyqtSignal(bool) 

global_signal_emitter = SignalEmitter()
global_signal_emitter_2 = SignalEmitter()
