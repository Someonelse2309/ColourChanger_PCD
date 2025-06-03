import cv2
import numpy as np

class replacingColor():

    def __init__(self, hTol = 80, sTol = 80, vTol = 80):
        self.hTol = hTol
        self.sTol = sTol
        self.vTol = vTol
        self.masking = None
        self.result = None

    def changeThreshold(self, hTol, sTol, vTol):
        self.hTol = hTol
        self.sTol = sTol
        self.vTol = vTol
    
    def getThreshold(self):
        return self.hTol, self.sTol, self.vTol

    def inputImage(self, img, colorBefore, colorAfter):
        self.img = img
        self.hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)

        self.before = self.convertToBGR(colorBefore)
        self.after =  self.convertToBGR(colorAfter)

        self.processImages()
    
    def convertToBGR(self, hex):
        RGBCol = [int(hex[i:i+2], 16) for i in (1, 3, 5)]
        BGRCol = RGBCol[::-1]
        return  np.uint8([[BGRCol]])
    
    def convertToHSV(self, BGRCol):
        HSVCol = cv2.cvtColor(BGRCol, cv2.COLOR_BGR2HSV)
        print(BGRCol, HSVCol)
        return HSVCol[0][0]

    
    def processImages(self):
        hB, sB, vB = self.convertToHSV(self.before) 
        # hA, sA, vA = self.convertToHSV(self.after) 
        batasAtas = np.array([
            min(int(hB) + self.hTol, 179),
            min(int(sB) + self.sTol, 255),
            min(int(vB) + self.vTol, 255)
        ])
        batasBawah = np.array([
            max(int(hB) - self.hTol, 0),
            max(int(sB) - self.sTol, 0),
            max(int(vB) - self.vTol, 0)
        ])


        print("Lower bound:", batasBawah)
        print("Upper bound:", batasAtas)


        self.masking = cv2.inRange(self.hsv, batasBawah, batasAtas)
        if np.count_nonzero(self.masking) == 0:
            print("Warning: Mask kosong, threshold tidak cocok!")

        warna_ganti = tuple(int(c) for c in self.after[0][0])
        
        self.result = self.img.copy()
        self.result[self.masking > 0] =  warna_ganti

    def getResult(self):
        return self.result

    def getMasking(self):
        return self.masking


    
if __name__ == "__main__":
    img = cv2.imread('download.png')
    hexBefore = "#0000ff"
    hexAfter = "#F6Ac48"
    temp = replacingColor(img,hexBefore,hexAfter)
    finalImg = temp.getResult()
    cv2.imshow("nama",finalImg)
    cv2.waitKey(0)

