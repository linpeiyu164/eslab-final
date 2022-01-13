import time
class PCA9685:
    ''' 
    PWM motor controler using PCA9685 boards. 
    This is used for most RC Cars
    '''
    def __init__(self, channel, address=0x40, frequency=60, busnum=None, init_delay=0.1):
        self.default_freq = 60
        self.pwm_scale = frequency / self.default_freq

        import Adafruit_PCA9685
        # Initialise the PCA9685 using the default address (0x40).
        if busnum is not None:
            from Adafruit_GPIO import I2C
            #replace the get_bus function with our own
            def get_bus():
                return busnum
            I2C.get_default_bus = get_bus
        self.pwm = Adafruit_PCA9685.PCA9685(address=address)
        self.pwm.set_pwm_freq(frequency)
        self.channel = channel
        time.sleep(init_delay) # "Tamiya TBLE-02" makes a little leap otherwise

    def set_pulse(self, pulse):
        self.pwm.set_pwm(self.channel, 0, int(pulse * self.pwm_scale))

    def run(self, pulse):
        self.set_pulse(pulse)

class PWMSteering:
    """
    Wrapper over a PWM motor cotnroller to convert angles to PWM pulses.
    """
    LEFT_ANGLE = -1 
    RIGHT_ANGLE = 1

    def __init__(self, controller=None,
                       left_pulse=360,
                       right_pulse=640):

        self.controller = controller
        self.left_pulse = left_pulse
        self.right_pulse = right_pulse

    def run(self, angle):
        pulse = ((self.right_pulse-self.left_pulse)/2)*(angle/180)+(self.right_pulse+self.left_pulse)/2
        self.controller.set_pulse(pulse)

    def shutdown(self):
        self.run(0) #set steering straight

class PWMThrottle:
    """
    Wrapper over a PWM motor cotnroller to convert -1 to 1 throttle
    values to PWM pulses.
    """
    MIN_THROTTLE = -1
    MAX_THROTTLE =  1

    def __init__(self, controller=None,
                       max_pulse=4095,
                       min_pulse=-4095,
                       zero_pulse=0):

        self.controller = controller
        self.max_pulse = max_pulse
        self.min_pulse = min_pulse
        self.zero_pulse = zero_pulse
        
        #send zero pulse to calibrate ESC
        print("Init ESC")
        self.controller.set_pulse(self.zero_pulse)
        time.sleep(1)


    def run(self, throttle):
        if throttle > 0:
            pulse = int(throttle*(self.max_pulse-self.zero_pulse))
            self.controller.pwm.set_pwm(self.controller.channel,0,pulse) 
            self.controller.pwm.set_pwm(self.controller.channel+1,0,4095) 
            self.controller.pwm.set_pwm(self.controller.channel+2,0,0) 
            self.controller.pwm.set_pwm(self.controller.channel+3,0,0)
            self.controller.pwm.set_pwm(self.controller.channel+4,0,pulse)
            self.controller.pwm.set_pwm(self.controller.channel+7,0,pulse)
            self.controller.pwm.set_pwm(self.controller.channel+6,0,4095)
            self.controller.pwm.set_pwm(self.controller.channel+5,0,0)      
        else:
            pulse = int(throttle*(self.zero_pulse-self.min_pulse))
            self.controller.pwm.set_pwm(self.controller.channel,0,- pulse)
            self.controller.pwm.set_pwm(self.controller.channel+2,0,4095)
            self.controller.pwm.set_pwm(self.controller.channel+1,0,0)
            self.controller.pwm.set_pwm(self.controller.channel+3,0,- pulse)
            self.controller.pwm.set_pwm(self.controller.channel+4,0,0)
            self.controller.pwm.set_pwm(self.controller.channel+7,0,- pulse)
            self.controller.pwm.set_pwm(self.controller.channel+5,0,4095)
            self.controller.pwm.set_pwm(self.controller.channel+6,0,0)
            
    def shutdown(self):
        self.run(0) #stop vehicle



# pc0 = PCA9685(0)
# pc1 = PCA9685(0,address = 0x60)
# p0_t = PWMThrottle(controller=pc1)
# p0_s = PWMSteering(controller=pc0)

