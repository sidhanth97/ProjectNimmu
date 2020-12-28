#!/usr/bin/env python3
from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250
import rospy
from datetime import datetime
from sensor_msgs.msg import Imu,MagneticField

mpu = MPU9250(
    address_ak=AK8963_ADDRESS, 
    address_mpu_master=MPU9050_ADDRESS_68, # In 0x68 Address
    address_mpu_slave=None, 
    bus=1,
    gfs=GFS_1000, 
    afs=AFS_8G, 
    mfs=AK8963_BIT_16, 
    mode=AK8963_MODE_C100HZ)

mpu.configure()

def talker():
	rospy.init_node('imu_tutorials',anonymous=True)
	pub1 = rospy.Publisher('/imu/data_raw', Imu, queue_size=10)
	pub2 = rospy.Publisher('/imu/mag', MagneticField, queue_size=10)
	mag = MagneticField()
	msg = Imu()
	msg.orientation.x = 0.0
	msg.orientation.y = 0.0
	msg.orientation.z = 0.0
	msg.orientation.w = 1.0
	msg.header.frame_id = 'imu_frame'
	mag.header.frame_id = 'imu_frame'
	print('Publishing')
	#rate = rospy.Rate(5)
	while not rospy.is_shutdown():
		msg.header.stamp.secs = int(rospy.get_time())
		mag.header.stamp.secs = int(rospy.get_time())
		msg.linear_acceleration.x = mpu.readAccelerometerMaster()[0]
		msg.linear_acceleration.y = mpu.readAccelerometerMaster()[1]
		msg.linear_acceleration.z = mpu.readAccelerometerMaster()[2]
		
		msg.angular_velocity.x = mpu.readGyroscopeMaster()[0]
		msg.angular_velocity.y = mpu.readGyroscopeMaster()[1]
		msg.angular_velocity.z = mpu.readGyroscopeMaster()[2]
		
		mag.magnetic_field.x = mpu.readMagnetometerMaster()[0]
		mag.magnetic_field.y = mpu.readMagnetometerMaster()[1]
		mag.magnetic_field.z = mpu.readMagnetometerMaster()[2]
		
		pub1.publish(msg)
		pub2.publish(mag)

if __name__ == '__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		passrospy.spin()
