### 
#
# Electrolib, HAL library for Python
# Copyright (c) Project Iota (http://projectiota.github.io/)
#
# Library was originally created for WeIO, www.we-io.net and than forked as a
# separate project in order to promote concept of using interpreted languages
# in microcontrolers.
#
# Electrolib is licensed under an Apache license, version 2.0 license.
# All rights not explicitly granted in the Apache license, version 2.0 are reserved.
# See the included LICENSE file for more details.
#
# Authors : 
# Uros PETREVSKI <uros@nodesign.net>
# Drasko DRASKOVIC <drasko.draskovic@gmail.com>
#
###

import pinout

""" Dummy board for testing purposes """
class Board():
    def __init__(self):
        self.name = 'dummy'
        self.wirings = wirings.Wirings()
        print "Print pins", wirings.pins

    def digitalWrite(self, pin, state):
        print "dummyBoard.digitalWrite(pin, state) has been called with parameters: %d, %d" % (pin, state)
    
    def digitalRead(self, pin):
        print "dummyBoard.digitalRead(pin) has been called with parameter: %d" % pin
    
    def analogRead(self, pin):
        print "dummyBoard.analogRead(pin) has been called with parameter: %d" % pin
        
    def getBoardName(self):
        return self.name
        
    def stop():
        print "Stop function has been called"

    #etc...
