### 
#
# WEIO Web Of Things Platform
# Copyright (C) 2013 Nodesign.net, Uros PETREVSKI, Drasko DRASKOVIC
# All rights reserved
#
#               ##      ## ######## ####  #######  
#               ##  ##  ## ##        ##  ##     ## 
#               ##  ##  ## ##        ##  ##     ## 
#               ##  ##  ## ######    ##  ##     ## 
#               ##  ##  ## ##        ##  ##     ## 
#               ##  ##  ## ##        ##  ##     ## 
#                ###  ###  ######## ####  #######
#
#                    Web Of Things Platform 
#
# This file is part of WEIO and is published under BSD license.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. All advertising materials mentioning features or use of this software
#    must display the following acknowledgement:
#    This product includes software developed by the WeIO project.
# 4. Neither the name of the WeIO nor the
# names of its contributors may be used to endorse or promote products
# derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY WEIO PROJECT AUTHORS AND CONTRIBUTORS ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL WEIO PROJECT AUTHORS AND CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Authors : 
# Uros PETREVSKI <uros@nodesign.net>
# Drasko DRASKOVIC <drasko.draskovic@gmail.com>
#
###

from weioLib.weio import *

LCD_RS = 0x40
LCD_EN = 0x20
LCD_CMD = 0
LCD_STR = 1

class Hd44780:
    LINE1 = 0x80                                                       
    LINE2 = 0xC0 
    
    def __init__(self, port):
        self.port = port
        portMode(self.port, OUTPUT)

        # Initialise display
        self.__lcd_byte(0x33, LCD_CMD)
        self.__lcd_byte(0x32, LCD_CMD)
        self.__lcd_byte(0x28, LCD_CMD)
        self.__lcd_byte(0x0C, LCD_CMD)
        self.__lcd_byte(0x06, LCD_CMD)
        self.__lcd_byte(0x01, LCD_CMD)  
        
    def selectLine(self, line):
        self.__lcd_byte(line, LCD_CMD)

    def writeString(self, message):
        # Send string to display
    
        message = message.ljust(16," ")  
        
        for i in range(16):
            self.__lcd_byte(ord(message[i]),LCD_STR)
        
    def __lcd_byte(self, bits, mode):
        msg = 0
        if mode:
            msg = (LCD_RS | (bits >> 4))
        else:
            msg = (bits >> 4)
        portWrite(self.port, msg)
                                
        msg = msg + LCD_EN
        portWrite(self.port, msg)
        msg = msg - LCD_EN
        portWrite(self.port, msg)
                                                    
        msg = 0
        if mode:
            msg = (LCD_RS | (bits & 0x0F))
        else:
            msg = (bits & 0x0F)
        portWrite(self.port, msg)
                                                                                   
        msg = msg + LCD_EN
        portWrite(self.port, msg)
        msg = msg - LCD_EN
        portWrite(self.port, msg)