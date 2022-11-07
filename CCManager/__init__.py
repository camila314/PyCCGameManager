import os
import zlib
import base64
import struct
import platform
from itertools import cycle
from Crypto.Cipher import AES

class GDData(object):
    def __init__(self,path):
        self.path = path
        self.ccll_path = f"{path}/CCLocalLevels.dat"
        self.ccgm_path = f"{path}/CCGameManager.dat"
        self.ccll = self.decode(open(self.ccll_path,"rb").read())
        self.ccgm = self.decode(open(self.ccgm_path,"rb").read())

    def injectLevel(self, levelData, levelName="CCLJect", levelDesc="This level was injected into your CCLocalLevels"):
        levels = self.ccll.split(">k_")
        payload = f"{header}>k_0</k><d><k>kCEK</k><i>4</i><k>k18</k><i>2</i><k>k2</k><s>{levelName}</s><k>k4</k><s>{levelData}</s><k>k5</k><s>{levelDesc}/s><k>k13</k><t /><k>k21</k><i>2</i><k>k16</k><i>1</i><k>k80</k><i>338</i><k>k81</k><i>23</i><k>k83</k><i>109</i><k>k50</k><i>35</i><k>k48</k><i>23</i><k>kI1</k><r>-1118.36</r><k>kI2</k><r>-366.449</r><k>kI3</k><r>0.7</r><k>kI4</k><i>2</i><k>kI5</k><i>11</i><k>kI7</k><i>1</i><k>kI6</k><d><k>0</k><s>0</s><k>1</k><s>0</s><k>2</k><s>0</s><k>3</k><s>0</s><k>4</k><s>0</s><k>5</k><s>0</s><k>6</k><s>0</s><k>7</k><s>0</s><k>8</k><s>0</s><k>9</k><s>0</s><k>10</k><s>0</s><k>11</k><s>2</s><k>12</k><s>0</s></d></d><k"
        for i in range(1,len(levels)):
            payload += f">k_{i}<{"<".join(levels[i].split("<")[1:])}"
        self.ccll = payload

    def save(self,ccll=True,ccgm=True):
        if ccll:
            open(self.ccll_path,"wb").write(self.encode(self.ccll))
        if ccgm:
            open(self.ccgm_path,"wb").write(self.encode(self.ccgm))

    def encode(self,data):
        pass

    def decode(self,data):
        pass

class GDWinData(GDData):
    def __init__(self):
        super().__init__(self,os.path.join(os.getenv("LOCALAPPDATA"), "GeometryDash"))

    def encode(self,data):
        compressed = zlib.compress(data)
        crc32 = struct.pack('I',zlib.crc32(data))
        size = struct.pack('I',len(data))
        encrypted = base64.b64encode(b'\x1f\x8b\x08\x00\x00\x00\x00\x00\x00\x0b' + compressed[2:-4] + crc32 + size,'-_')
        return bytes([ord(a) ^ 11 for a in encrypted])

    def decode(self,data):
        encrypted = bytes([ord(a) ^ 11 for a in data]) 
        return zlib.decompress(base64.b64decode(encrypted,'-_')[10:],-zlib.MAX_WBITS)

class GDMacData(GDData):
    MAC_KEY = b"\x69\x70\x75\x39\x54\x55\x76\x35\x34\x79\x76\x5d\x69\x73\x46\x4d\x68\x35\x40\x3b\x74\x2e\x35\x77\x33\x34\x45\x32\x52\x79\x40\x7b"
    def __init__(self):
        super().__init__(self,os.path.join(os.path.expanduser("~"),"Library/Application Support/GeometryDash"))
        self.cipher = AES.new(GDMacData.MAC_KEY, AES.MODE_ECB)

    def encode(self,data):
        extra = len(data) % 16
        if extra > 0:
            data += ('\x0b' * (16 - extra))
        return self.cipher.encrypt(data)

    def decode(self,data):
        return self.cipher.decrypt(data)

def newManager():
    if platform.system() == 'Darwin':
        return GDMacData()
    else:
        return GDWinData()
