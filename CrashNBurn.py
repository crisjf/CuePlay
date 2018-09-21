from threading import Thread
import time

import numpy as np
import WonderPy.core.wwMain
from WonderPy.core.wwConstants import WWRobotConstants
from WonderPy.components.wwMedia import WWMedia

class MyClass(object):
	def __init__(self):
		self.speed = 60
		self.halt_tolerance = 40
		self.head_rotation_rate = 0.5
		self.halt_state = True
		self.flee_state = False

	def on_connect(self, robot):
		print("Starting a thread for %s." % (robot.name))
		Thread(target=self.thread_mover, args=(robot,)).start()
		Thread(target=self.thread_flee, args=(robot,)).start()

	def on_sensors(self, robot):
		if (not self.halt_state):
			if (robot.sensors.distance_front_left_facing.distance_approximate<self.halt_tolerance)|(robot.sensors.distance_front_right_facing.distance_approximate<self.halt_tolerance):
				Thread(target=self.thread_crash, args=(robot,)).start()

	def thread_mover(self,robot):
		print "Move!"
		robot.cmds.media.do_audio("SNCHBIGROBUO")
		robot.cmds.head.stage_pan_angle(0)
		robot.cmds.head.stage_tilt_angle(0)
		robot.block_until_button_main_press_and_release()
		robot.cmds.media.do_audio("SNCHHEREICOME")
		robot.cmds.RGB.stage_all(0, 0, 1)
		time.sleep(0.5)
		self.halt_state = False
		robot.cmds.body.stage_wheel_speeds(self.speed, self.speed)
		while not self.halt_state:
			angle = (1 if np.random.random()>=0.5 else -1)*(10+45*np.random.random())
			robot.cmds.head.stage_pan_angle(angle)
			robot.cmds.head.stage_tilt_angle(angle*0.5)
			time.sleep(self.head_rotation_rate)

	def thread_crash(self,robot):
		print "Crash!"
		self.halt_state = True
		robot.cmds.body.stage_stop()
		robot.cmds.RGB.stage_all(1, 0, 0)
		robot.cmds.media.stage_audio("SNCHWHOACRANB")
		while (robot.sensors.distance_front_left_facing.distance_approximate<self.halt_tolerance)|(robot.sensors.distance_front_right_facing.distance_approximate<self.halt_tolerance):
			robot.cmds.body.do_forward(-30,20)
		robot.cmds.body.do_turn(180+30*(np.random.random()-0.5)/0.5,180)
		Thread(target=self.thread_mover, args=(robot,)).start()

	def thread_flee(self,robot):
		while True:
			while (robot.sensors.distance_front_left_facing.distance_approximate<self.halt_tolerance)&(robot.sensors.distance_front_right_facing.distance_approximate<self.halt_tolerance):
				robot.cmds.body.do_forward(-5,20)
			while (robot.sensors.distance_front_left_facing.distance_approximate<self.halt_tolerance):
				robot.cmds.body.do_turn(45,180)
			while (robot.sensors.distance_front_right_facing.distance_approximate<self.halt_tolerance):
				robot.cmds.body.do_turn(-45,180)
			time.sleep(0.1)

# kick off the program !
if __name__ == "__main__":
	WonderPy.core.wwMain.start(MyClass())
