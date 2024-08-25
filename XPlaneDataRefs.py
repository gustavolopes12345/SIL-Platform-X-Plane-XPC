# X-Plane Data Refs

# All X-Plane data refs can be found on the website below
# https://developer.x-plane.com/datarefs/

XPlaneDREFs = [
'sim/flightmodel/position/theta',\
'sim/flightmodel/position/phi',\
'sim/flightmodel/position/psi',\
'sim/flightmodel/position/alpha',\
'sim/flightmodel/position/latitude',\
'sim/flightmodel/position/longitude',\
'sim/flightmodel/misc/h_ind',\
'sim/flightmodel/position/elevation',\
'sim/flightmodel/controls/elv_trim',\
'sim/flightmodel/controls/ail_trim',\
'sim/flightmodel/controls/rud_trim',\
'sim/flightmodel/engine/ENGN_thro_use',\
'sim/flightmodel/controls/flaprqst',\
'sim/flightmodel/controls/sbrkrqst',\
'sim/aircraft/parts/acf_gear_deploy',\
'sim/flightmodel/controls/parkbrake',\
'sim/cockpit2/gauges/indicators/heading_electric_deg_mag_pilot',\
'sim/flightmodel/position/indicated_airspeed',\
'sim/flightmodel/position/true_airspeed',\
'sim/flightmodel/position/groundspeed',\
'sim/flightmodel/position/magnetic_variation',\
'sim/flightmodel/position/P',\
'sim/flightmodel/position/Q',\
'sim/flightmodel/position/R',\
'sim/flightmodel/position/vh_ind',\
'sim/cockpit2/gauges/indicators/airspeed_kts_pilot',\
'sim/flightmodel/failures/onground_any',\
]

dataRef_Pitch = 0 # The pitch relative to the plane normal to the Y axis in degrees - OpenGL coordinates
dataRef_Roll = 1 # The roll of the aircraft in degrees - OpenGL coordinates
dataRef_Heading	= 2 # The true heading of the aircraft in degrees from the Z axis - OpenGL coordinates
dataRef_AngleOfAttack = 3 # The pitch relative to the flown path (angle of attack)
dataRef_Latitude  = 4 # The latitude of the aircraft
dataRef_Longitude = 5 # The longitude of the aircraft
dataRef_Altitude_Meters = 6 # The elevation above MSL of the aircraft
dataRef_Altitude_Foots = 7 # The elevation above MSL of the aircraft
dataRef_Elevator_trim = 8 # Elevation Trim, -1 = max nose down, 1 = max nose up
dataRef_Aileron_trim = 0 # Current Aileron Trim, -1 = max left, 1 = max right
dataRef_Rudder_trim = 10 # Rudder Trim, -1 = max left, 1 = max right
dataRef_Throttle_trim = 11 # Throttle (per engine) when overridden by you, plus with thrust vectors - use override_throttles to change
dataRef_Flap_trim = 12 # Requested flap deployment, 0 = off, 1 = max
dataRef_Speedbrake_trim = 13 # Speed Brake, -0.5 = armed, 0 = off, 1 = max deployment
dataRef_Landing_gear = 14 # Landing gear deployment, 0.0->1.0
dataRef_Parking_Brake = 15 # Parking Brake, 1 = max
dataRef_Magnetic_Heading = 16 # Indicated magnetic heading, in degrees. Source: electric gyro. Side: Pilot
dataRef__indicated_airspeed = 17 # Air speed indicated - this takes into account air density and wind direction
dataRef__true_airspeed = 18 # Air speed true - this does not take into account air density at altitude!
dataRef__groundspeed = 19 # The ground speed of the aircraft
dataRef__Magnetic_Variation = 20 # The local magnetic variation
dataRef__P = 21 # The roll rotation rates (relative to the flight)
dataRef__Q = 22 # The pitch rotation rates (relative to the flight)
dataRef__R = 23 # The yaw rotation rates (relative to the flight)
dataRef__vertical_speed = 24 # VVI (vertical velocity in meters per second)
dataRef__airspeed_kts_pilot = 25 # Indicated airspeed in knots, pilot. Writeable with override_IAS
dataRef__onground = 26 # User Aircraft is on the ground when this is set to 1