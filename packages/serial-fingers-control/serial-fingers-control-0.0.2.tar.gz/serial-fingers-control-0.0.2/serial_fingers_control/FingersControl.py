#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from Serial.serialPi import SerialU

class FingersControl():
  def __init__(self):
        self.serial = SerialU()

  def _servoHandToBytes(self, servoId: int,
                              servoAngle: int,
                              servoSpeed: int) -> []:
        data = [23]
        d = [servoId, servoAngle >> 8, servoAngle & 0xff, servoSpeed]
        data+=d
        data.append(self.serial.CalculateCrc(data[1:]))

        return data

  def FingersManage(self, servoId: int,
                    servoAngle: int,
                    servoSpeed: int) -> []:

      data = self._servoHandToBytes(servoId, servoAngle, servoSpeed)
      data.append(36)

      self.serial.write(data, len(data))
      return data

     


