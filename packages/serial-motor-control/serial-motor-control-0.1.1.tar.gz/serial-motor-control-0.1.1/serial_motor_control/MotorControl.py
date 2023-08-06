#!/usr/bin/env python3
 # -*- coding: utf-8 -*-

from Serial.serialPi import SerialU

class MotorControl():
    def __init__(self):
        self.serial = SerialU()

    def MotionManage(self, MotorID: int, FrontMotorSpeed: int, BackMotorSpeed: int):
        FrontMotorSpeed = 65534 - abs(FrontMotorSpeed) if FrontMotorSpeed < 0 else abs(FrontMotorSpeed)
        BackMotorSpeed = 65534 - abs(BackMotorSpeed) if BackMotorSpeed < 0 else abs(BackMotorSpeed)

        data = [18, MotorID, FrontMotorSpeed >> 8, FrontMotorSpeed & 0xff, BackMotorSpeed >> 8, BackMotorSpeed & 0xff, 0]

        data.append(SerialU.CalculateCrc(data[1:]))
        data.append(36)
        self.serial.write(data, len(data))
        return data
