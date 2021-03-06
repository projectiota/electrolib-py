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

import time
import signal
import sys

###
# User API functions for GPIO
###

class Electrolib():
    def __init__(self, boardName):
        boardObj = __import__(boardName, fromlist=[''])
        self.board = boardObj.Board(self.mainInterrupt)
        self.wirings = self.board.wirings
        
        """Assure that program is closed properly if signal is received"""
        signal.signal(signal.SIGINT, self.signal_handler)
        
        self.declaredPins = []
        for i in range(0,len(self.wirings.PINS)):
            self.declaredPins.append(-1)
            
        self.interrupts = []
        for i in range(0, self.wirings.HARD_INTERRUPTS):
            # 1 is available
            self.interrupts.append(None)
            
    def signal_handler(self, signal, frame):
        print "\nStopping electronics and exiting program"
        self.stop()
        sys.exit(0)
        
    def mainInterrupt(self, data):
        myid = data[1][0]
        for inter in self.interrupts:
            if inter.myid == myid:
                inter.callback(data[1][1])
                break
        
    def getBoardName(self):
        return self.board.getBoardName()

    def pinMode(self, pin, mode):
        result = None
        if hasattr(self.board, 'pinMode'):
            result = self.board.pinMode(pin, mode)
            self.declaredPins[pin] = mode
        return result
            
    def digitalWrite(self, pin, state):
        res = None
        if hasattr(self.board, 'digitalWrite'):
            if self.declaredPins[pin] != self.wirings.OUTPUT:
                self.board.pinMode(pin, self.wirings.OUTPUT)
                self.declaredPins[pin] = self.wirings.OUTPUT
    
            res = self.board.digitalWrite(pin, state)
        return res
    
    def digitalRead(self, pin):
        res = None
        if hasattr(self.board, 'digitalRead'):
            # Force input mode (High Impedance) if input was not declared
            if (self.declaredPins[pin] != self.wirings.INPUT_HIGHZ) and (self.declaredPins[pin] != self.wirings.INPUT_PULLUP) and (self.declaredPins[pin] != self.wirings.INPUT_PULLDOWN) :
                self.board.pinMode(pin, self.wirings.INPUT_HIGHZ)
                self.declaredPins[pin] = self.wirings.INPUT_HIGHZ
            res = self.board.digitalRead(pin)
        return res
    
    def analogRead(self, pin):
        res = None
        if hasattr(self.board, 'analogRead'):
            if ((pin >= self.wirings.ADCS[0]) and (pin <= self.wirings.ADCS[-1])):
                if self.declaredPins[pin] != self.wirings.INPUT_ADC:
                    self.declaredPins[pin] = self.wirings.INPUT_ADC
                    self.board.pinMode(pin, self.wirings.INPUT_ADC)
                res = self.board.analogRead(pin)
            else:
                print "Pin %d is not ADC pin" % pin
        return res
    
    def pwmWrite(self, pin, value):
        res = None
        if hasattr(self.board, 'pwmWrite'):
            if (pin >= self.wirings.PWMS[0]) and (pin <= self.wirings.PWMS[-1]):
                if self.declaredPins[pin] != self.wirings.OUTPUT_PWM:
                    self.declaredPins[pin] = self.wirings.OUTPUT_PWM
                    self.board.pinMode(pin, self.wirings.OUTPUT_PWM)
                
                # value limiters
                if (value < 0) :
                    value = 0
                if (value > self.wirings.PWM_LIMIT):
                    value = self.wirings.PWM_LIMIT
                
                # do proportion calculus
                # People think in bit precision rather in microseconds. It's common to connect sensor outputs to pwm
                # so we have to make a small proportion calculus here to make interface more friendly
                # for example if period is 1000us and limit 255 (8bit), 1000 will be divided to 255 steps to drive pwm
                out = self.proportion(value, 0, self.wirings.PWM_LIMIT, 0, self.wirings.PWM_PERIOD)
                #print int(out), self.wirings.PWM_LIMIT, self.wirings.PWM_PERIOD
                res = self.board.pwmWrite(pin, int(out))
            else :
                print "Pin %d is not PWM pin" % pin
        else:
            print "electripyError: Board %s has no function pwmWrite()" % self.board.name
        return res
    
    def analogWrite(self, pin, value):
        """Defining synonime of pwmWrite to match arduino syntax"""
        res = None
        if hasattr(self.board, 'pwmWrite'):
            res = self.board.pwmWrite(pin, value)
    
    def setPwmPeriod(self, period):
        res = None
        if hasattr(self.board, 'setPwmPeriod'):
            if ((period >= 0) and (period <= self.wirings.PWM_PERIOD_LIMIT_CONST)): 
                self.wirings.PWM_PERIOD = int(period)
                res = self.board.setPwmPeriod(self.wirings.PWM_PERIOD)
            else :
                print "electripyError: PWM period can be only between 0-%s" % self.wirings.PWM_PERIOD_LIMIT_CONST
        else :        
            print "electripyError: Board %s has no function setPwmPeriod()" % self.board.name
        return res
        
    def setPwmLimit(self, limit):
        res = None
        res = self.wirings.PWM_LIMIT = int(limit)
        return res

    def getAvailableInterruptId(self) :
        for i in range(0,self.wirings.HARD_INTERRUPTS):
            if self.interrupts[i] == None:
                return i
        print "weioBoard.getAvailableInterruptId, there is only %s interrupts available" % self.wirings.HARD_INTERRUPTS 
        return None

    def attachInterrupt(self, pin, mode, callback):
        res = None
        if hasattr(self.board, 'attachInterrupt'):
            myid = self.getAvailableInterruptId()
            if not(myid is None) :
                inter = Interrupt(myid, pin, mode, callback)
                self.interrupts[myid] = inter
                res = self.board.attachInterrupt(inter)
        return res

    def detachInterrupt(self, pin):
        res = None
        if hasattr(self.board, 'detachInterrupt'):
            for m in self.interrupts:
                if not(m is None):
                    if (m.pin==pin):
                        #print "pin to be detached ", m.pin
                        res = self.board.detachInterrupt(m)
        return res

    def delay(self, period):
        """Delay expressed in milliseconds. Delay can be evil because is blocking function"""
        time.sleep(period/1000.0)
        
    def proportion(self, value,istart,istop,ostart,ostop) :
        """This is port of Processing map function. It's useful to make proportion calculation"""
        return float(ostart) + (float(ostop) - float(ostart)) * ((float(value) - float(istart)) / (float(istop) - float(istart)))
        
    def stop(self): 
        """Procedure tp stop the board"""
        res = None
        if hasattr(self.board, 'stop'):
            res = self.board.stop()
        return res

# This is class that stores all data regarding interrupt events
class Interrupt():
    def __init__(self, myid, pin, mode, callback):
        self.myid = myid
        self.pin = pin
        self.mode = mode
        self.callback = callback
