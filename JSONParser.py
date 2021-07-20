
import json
from RectPolyomino import RectPolyomino
from LPolyomino import LPolyomino
from Field import Field
from JSON_LABELS import *


class JSONParser:
    def __init__(self, filename):
        self.filename = filename
        self.pId = 0
        self.polyominos = []
        self.field = None

    def parse(self):
        rawData = self.getRawData()
        self.parseField(rawData)
        self.parsePolyominos(rawData)

    def getRawData(self):
        fd = open(self.filename, 'r')
        data = json.loads(fd.read())
        fd.close()
        return data

    def parseField(self, data):
        fieldData = data[FIELD]
        fieldWidth = fieldData[WIDTH]
        fieldHeight = fieldData[HEIGHT]

        self.field = Field(fieldWidth, fieldHeight)

    def parsePolyominos(self, data):
        lPminos = data[L_POLYOMINO]
        rectPminos = data[RECT_POLYOMINO]

        for pData in lPminos + rectPminos:
            for _ in range(pData[CAPACITY]):
                width = pData[WIDTH]
                height = pData[HEIGHT]
                self.polyominos.append(
                    LPolyomino(self.pId, height, width)
                    if self.pId < len(lPminos)
                    else RectPolyomino(self.pId, height, width)
                )
                self.pId += 1

    def getPolyominos(self):
        return self.polyominos

    def getField(self):
        return self.field

    def getPolyominosCount(self):
        return self.pId
