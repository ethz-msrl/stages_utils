import serial
import time

class threeAxisStage():
    def __init__(self,revperm=1000,port="/dev/ttyACM0"):
        self.ser=serial.Serial(port)
        self.ser.baudrate=9600
        self.ser.bytesize=8
        self.ser.parity='N'
        self.ser.stopbits=1
        self.delay_us=250
        self.stepnox=0
        self.stepnoy=0
        self.stepnoz=0
        self.revperm=revperm
        self.ser.read_all()
    def movedx(self,dist,use_steps=False):
        if use_steps:
            stepno=dist
        else:
            stepno=int(dist*self.revperm)
        self.stepnox=self.stepnox+stepno
        self.ser.write(b'MOVEX%d\n'%(stepno))
        self.wait_for_string("COMPLETE")
    def movedy(self,dist,use_steps=False):
        if use_steps:
            stepno=dist
        else:
            stepno=int(dist*self.revperm)
        self.stepnoy=self.stepnoy+stepno
        self.ser.write(b'MOVEY%d\n'%(stepno))
        self.wait_for_string("COMPLETE")
    def movedz(self,dist,use_steps=False):
        if use_steps:
            stepno=dist
        else:
            stepno=int(dist*self.revperm)
        self.stepnoz=self.stepnoz+stepno
        self.ser.write(b'MOVEZ%d\n'%(stepno))
        self.wait_for_string("COMPLETE")
    def movex(self,posx):
        nosteps=int(posx*self.revperm-self.stepnox)
        self.movedx(nosteps,use_steps=True)
    def movey(self,posy):
        nosteps=int(posy*self.revperm-self.stepnoy)
        self.movedy(nosteps,use_steps=True)
    def movez(self,posz):
        nosteps=int(posz*self.revperm-self.stepnoz)
        self.movedz(nosteps,use_steps=True)
    #set the time delay between motor steps in microseconds
    def setdelayus(self,delay_us):
        self.ser.write(b'SETSP%d\n'%(delay_us))
        self.wait_for_string("COMPLETE")
    def wait_for_string(self,waitstr):
        serstr=""
        while("COMPLETE" not in serstr):
            partial_string=self.ser.read_all().decode("utf-8")
            if(len(partial_string)>0):
                serstr=serstr+partial_string
            time.sleep(50e-3)
    def reset_origin(self):
        self.stepnox=0
        self.stepnoy=0
        self.stepnoz=0
    def get_position(self):
        return (self.stepnox/self.revperm,self.stepnoy/self.revperm,self.stepnoz/self.revperm)
    def __exit__(self):
        self.ser.close()
        
class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

stepnox_center=-21400
stepnoy_center=27600
#we measured a distance of 31.3cm for 50000 steps in x directions
revperm_=50000/0.313
distx_center=stepnox_center/revperm_
disty_center=stepnoy_center/revperm_

if __name__=="__main__":
    stage=threeAxisStage(revperm=revperm_,port="/dev/ttyACM0")
    time.sleep(1)
    stepcount=5000
    #set the delay between steps to 100us
    stage.setdelayus(100)
    #move in x direction
    stage.movedx(5e-2)
    #move in x direction
    stage.movedx(-5e-2)
    #move in x direction
    stage.movedy(5e-2)
    #move in x direction
    stage.movedy(-5e-2)
    #move in x direction
    stage.movedz(5e-2)
    #move in x direction
    stage.movedz(-5e-2)
    
    #drive stage around manually
    getch = _GetchUnix()
    increment=50
    while(True):
        time.sleep(0.05)
        res=getch()
        if(res=='a'):
            stage.movex(increment)
        if(res=='d'):
            stage.movex(-increment)
        if(res=='w'):
            stage.movey(increment)
        if(res=='s'):
            stage.movey(-increment)
        if(res=='r'):
            stage.movez(increment)
        if(res=='f'):
            stage.movez(-increment)
        print(res)
    pass