from car import*
import time
class CarController:
    '''
    A car controller that can control the car via function self.get_command() or self.key()
    CAUTION: make sure to call self.shutdown() everytime you finish executing the program
    '''
    def __init__(self):
        ''' pc0_s: intialize PCA9685 for steering control
            pc0_t: intialize PCA9685 for throttle control
            p0_s: controller for steering
            p0_t: controller for throttle'''
        self.pc0_s = PCA9685(0)
        self.pc0_t = PCA9685(0,address = 0x60)
        self.p0_s = PWMSteering(controller=self.pc0_s)
        self.p0_t = PWMThrottle(controller=self.pc0_t)

    def get_command(self,command, df=100, db=100):
        '''read command(str) and decide whether to turn left, right or move forward, backward
        
        Parameters
        ----------
        command : str
        
         a string that give control instruction(left,right,forward,backward,stable)
        '''
        
        # stop the engine and steer straight everytime the function is called
        #self.p0_s.shutdown()
        #self.p0_t.shutdown()
        #turn left and move forward
        if command == ("left"):
            if df>10:
                self.p0_s.run(-180)
                self.p0_t.run(0.2)
            else:
                self.shutdown()
        # turn right and move forward
        elif command == ("right"):
            if df>10:
                self.p0_s.run(180)
                self.p0_t.run(0.2)
            else:
                self.shutdown()
        #move forward
        elif command == ("forward"):
            if df>10:
                self.p0_s.shutdown()
                self.p0_t.run(0.2)
            else:
                self.shutdown()
        #move backward
        elif command == ("backward"):
            if db>10:
                self.p0_s.shutdown()
                self.p0_t.run(-0.2)
            else:
                self.shutdown()
        
        else:
            self.shutdown()
        #wait for 0.5 second(so the car motion can kept going for a while)
        time.sleep(0.5)
    
    def shutdown(self):
        '''stop the engine and steer straight'''
        self.p0_t.shutdown()
        self.p0_s.shutdown()
    
    def key(self,command):
        '''using keyboard as controller
        a = left
        d = right
        w = forward
        s = backward
        q = quit
        '''
        if command == "a":
            self.get_command("left")
        elif command == "d":
            self.get_command("right")
        elif command == "w":
            self.get_command("forward")
        elif command == "s":
            self.get_command("backward")
        elif command == "q":
            self.shutdown()

if __name__ == "__main__":
    # command from keyboard: 
    ctr = CarController()
    while True:
        command = input("enter command :")
        ctr.key(command)
        if command == "q":
            break
        ctr.shutdown()
    
    # command from server example:
    # ctr.get_command("left")
    # ctr.get_command("left")
    # ctr.get_command("left")
    # ctr.get_command("right")
    # ctr.get_command("right")
    # ctr.get_command("right")
    ctr.shutdown()