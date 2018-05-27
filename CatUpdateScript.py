#update execute_script
from Cat_update import *
import sys, time

class CatUpdateScript:
    def __init__(self, data):
        self.credFile = 'C:\\Users\\Owner\\Documents\\Important\\catcred.txt'
        self.credFile2 = 'C:\\Users\\Owner\\Documents\\Important\\cat_cred2.txt'
        self.catInst = Cat_update(self.credFile, self.credFile2, update_data=data)
    def updateImages(self):
        self.catInst.update_images()

if __name__ == "__main__":
    mInst = CatUpdateScript(sys.argv[1])
    mInst.catInst.start()
    time.sleep(1)
    
    mInst.updateImages()
