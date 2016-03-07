'''
Created on 4.3.2016

@author: Rohmu
'''
class CorruptedMapFileError(Exception):

    def __init__(self, message):
        super(CorruptedMapFileError, self).__init__(message)