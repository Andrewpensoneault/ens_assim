## This file contains the definition of classes of measurement algorithms. To add a new algorithm, add a new subclass to
## measure.py and give it a method get_current_meas
##
## Written by: Andrew Pensoneault

class Measure(object):
    ## Parent 
    def __init__(self):
        pass

    def set_covariance(self, covariance):
        self.covariance = covariance

    def set_measurements(self, measurements):
        self.measurements = measurements
    
    def set_operator(self, operator):
        self.operator = operator