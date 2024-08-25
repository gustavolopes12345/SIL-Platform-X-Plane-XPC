import sys
import xpc
import PID as PID_Controller
import time
from GUI import RealTimeGraph
from PyQt5 import QtCore, QtWidgets
from TrajectoryGenerator import TrajectoryGenerator
from GUI_Classes import PIDControllerUI, SetPointReferenceUI, WaypointUI, MplCanvas
from XPlaneDataRefs import *

"""--------------------------------------------------------------------------
PID Controller Configuration and Initial Setpoints
-----------------------------------------------------------------------------"""

setpoint_roll = 0 #degree
setpoint_pitch = 2 #degree
setpoint_yaw = 0 # degree
setpoint_speed = 110 # (KIAS) knots of indicated airspeed
setpoint_alt = 1640 # foots
setpoint_hdg = 0 # degree

# The starting latitude and longitude at Seattle Tacoma Airport is 47.456 latitude and 122.32 longitude
target_waypoint1 = (47.456010708014833,-122.378017488055293)
target_waypoint2 = (47.456010708014833,-122.428017488055293)
target_waypoint3 = (47.406010708014833,-122.428017488055293)
target_waypoint4 = (47.406010708014833,-122.378017488055293)
target_waypoint5 = (47.456010708014833,-122.378017488055293)

# The initial mission can be changed in the tuple array below
target_waypoint_array = [target_waypoint1,target_waypoint2,target_waypoint3,target_waypoint4, target_waypoint5]

# PID Pitch Gains
Kp_gain_Pitch = 0.10
Ki_gain_Pitch = 0.01
Kd_gain_Pitch = 0.02

# PID Roll Gains
Kp_gain_Roll = 0.10
Ki_gain_Roll = 0.01
Kd_gain_Roll = 0.02

# PID Altitude Gains
Kp_gain_Altitude = 0.10
Ki_gain_Altitude = 0.01
Kd_gain_Altitude = 0.05

# PID Speed Gains
Kp_gain_Speed = 0.1 
Ki_gain_Speed =  0.01 
Kd_gain_Speed = 0.05 

# PID Guidance Gains
Kp_gain_Guidance = 0.1 
Ki_gain_Guidance = 0.01
Kd_gain_Guidance = 0.05 


PIDPitch = PID_Controller.PID(Kp_gain_Pitch, Ki_gain_Pitch, Kd_gain_Pitch)
PIDPitch.SetPoint = setpoint_pitch

PIDRoll = PID_Controller.PID(Kp_gain_Roll, Ki_gain_Roll, Kd_gain_Roll)
PIDRoll.SetPoint = setpoint_roll

PIDAltitude = PID_Controller.PID(Kp_gain_Altitude, Ki_gain_Altitude, Kd_gain_Altitude)
PIDAltitude.SetPoint = setpoint_alt

PIDSpeed = PID_Controller.PID(Kp_gain_Speed, Ki_gain_Speed, Kd_gain_Speed)
PIDSpeed.SetPoint = setpoint_speed

PIDGuidance = PID_Controller.PID(Kp_gain_Guidance,Ki_gain_Guidance,Kd_gain_Guidance)
PIDGuidance.SetPoint = setpoint_hdg 

    
"""--------------------------------------------------------------------------
Graphic Interface
-----------------------------------------------------------------------------"""

app = QtWidgets.QApplication(sys.argv)
main_window = RealTimeGraph(PIDAltitude, PIDSpeed, PIDGuidance, setpoint_alt, setpoint_speed, target_waypoint_array)
main_window.show()

"""--------------------------------------------------------------------------
Helper Methods
-----------------------------------------------------------------------------"""


def saturator(signal, min=-1, max=1):
    '''Saturator in Python'''
    if (signal > max):
        return max
    elif (signal < min):
        return min
    else:
        return signal
    
"""--------------------------------------------------------------------------
Control Loop
-----------------------------------------------------------------------------"""

def main():

    start_time = time.perf_counter()
    accumulated_time = 0.0
    with xpc.XPlaneConnect() as client: # Establishes UDP communication with X-Plane via UDP sockets
        start_time = time.perf_counter()
        accumulated_time = 0.0
        points = []

        # Plots the initial waypoints
        for waypoint in target_waypoint_array:
            points.append(waypoint[0])  
            points.append(waypoint[1])  
            points.append(setpoint_alt * 0.3048) 

        client.sendWYPT(3, points) # Clear all waypoints
        client.sendWYPT(1, points) # Sends the command to X-Plane to plot the initial waypoints
        
        current_target_waypoint = target_waypoint1 # WayPoint 0 is the first
        currentWaypointInArray = 0        
        while True:
            current_time = time.perf_counter()
            elapsed_time = current_time - start_time 
            if (elapsed_time >= 0.05): # Control Period 0.05 seconds, frequency 20HZ. You can change this value to change the control frequency
                start_time = current_time
                accumulated_time += elapsed_time

                ctrl = client.getCTRL()
                
                # You can get any DREF from X-Plane by simply adding it in the XPlaneDataRefs.py file. All these dataRefs constants are declared there
                X_Plane_Data_Refs = client.getDREFs(XPlaneDREFs)

                pitch = X_Plane_Data_Refs[dataRef_Pitch][0]
                roll = X_Plane_Data_Refs[dataRef_Roll][0]
                yaw =  X_Plane_Data_Refs[dataRef_Heading][0]
                latitude = X_Plane_Data_Refs[dataRef_Latitude][0]
                longitude = X_Plane_Data_Refs[dataRef_Longitude][0]
                altitude_in_foots = X_Plane_Data_Refs[dataRef_Altitude_Meters][0] 
                altitude_in_meter = X_Plane_Data_Refs[dataRef_Altitude_Foots][0]
                true_airspeed = X_Plane_Data_Refs[dataRef__true_airspeed][0]
                indicated_airspeed = X_Plane_Data_Refs[dataRef__airspeed_kts_pilot][0]
                magnetic_heading = X_Plane_Data_Refs[dataRef_Magnetic_Heading][0]
                onground = X_Plane_Data_Refs[dataRef__onground][0]

                distance_to_waypoint = 0

                if(altitude_in_foots < 300): # The SIL is activated after the aircraft reaches 300 feet
                    manualControl = 1
                else:

                    PIDAltitude.update(altitude_in_foots)
                    PIDSpeed.update(indicated_airspeed)
                    PIDPitch.update(pitch)
                    PIDRoll.update(roll)
                    PIDGuidance.update(magnetic_heading)

                    #Altitude Controller
                    new_pitch_from_altitude = saturator(PIDAltitude.output, -10, 10)
                    PIDPitch.SetPoint = new_pitch_from_altitude
                    PIDAltitude.SetPoint = main_window.altitude_reference_window.setpoint

                    #Guidance Controller
                    current_target_waypoint, currentWaypointInArray = TrajectoryGenerator.nextWaypoint((latitude, longitude), current_target_waypoint, target_waypoint_array, currentWaypointInArray)
                    heading_angle_to_target_waypoint = TrajectoryGenerator.calculates_LOS((latitude, longitude), current_target_waypoint)
                    distance_to_waypoint  = TrajectoryGenerator.haversine((latitude, longitude), current_target_waypoint)
                    PIDGuidance.SetPoint = heading_angle_to_target_waypoint
                    new_roll_from_heading_error = saturator(PIDGuidance.output, -20, 20)
                    PIDRoll.SetPoint = new_roll_from_heading_error

                    #Speed Controller
                    PIDSpeed.SetPoint = main_window.speed_reference_window.setpoint

                    elevator_signal = saturator(PIDPitch.output, min=-1, max=1)
                    aileron_signal = saturator(PIDRoll.output, min=-1, max=1)
                    throttle_signal = saturator(PIDSpeed.output, min=0, max=1)

                    # The function below sets the new control surface commands on the aircraft
                    ctrl = [elevator_signal, aileron_signal, 0.0, throttle_signal] 
                    client.sendCTRL(ctrl)
                # Updates the graphical interface
                main_window.update_data(accumulated_time, pitch, roll, yaw, magnetic_heading, longitude, latitude, altitude_in_foots, indicated_airspeed, true_airspeed, current_target_waypoint[0], current_target_waypoint[1], setpoint_alt, setpoint_speed, distance_to_waypoint )

                elapsed_time = 0.0
            QtWidgets.QApplication.processEvents()
if __name__ == "__main__":
    main()