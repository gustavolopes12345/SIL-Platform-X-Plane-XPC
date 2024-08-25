import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import InfiniteLine
import pyqtgraph as pg
import numpy as np
import PID
import styles as st
from GUI_Classes import PIDControllerUI, SetPointReferenceUI, WaypointUI, MplCanvas

class RealTimeGraph(QtWidgets.QMainWindow):
    def __init__(self, altitude_PID, speed_PID, guidance_PID, setpoint_alt, setpoint_speed, target_waypoint_array):
        super().__init__()

        self.timeC = 0
        self.pitch = 0
        self.roll = 0
        self.yaw = 0
        self.heading_angle = 0
        self.longitude = 0
        self.latitude = 0
        self.altitude = 0
        self.indicated_airspeed = 0
        self.true_airspeed = 0
        self.target_latitude = 0
        self.target_longitude = 0
        self.target_altitude = 0
        self.target_speed = 0
        self.distance_to_waypoint = 0

        self.time_data = []
        self.altitude_data_list = []
        self.pitch_data_list = []
        self.roll_data_list = []
        self.yaw_data_list = []
        self.longitude_data_list = []
        self.latitude_data_list = []
        self.speed_data_list = []

        self.pid_altitude_window = PIDControllerUI("altitude", altitude_PID)
        self.pid_speed_window = PIDControllerUI("speed", speed_PID)
        self.pid_guidance_window = PIDControllerUI("guidance", guidance_PID)

        self.altitude_reference_window = SetPointReferenceUI("altitude", setpoint_alt)
        self.speed_reference_window = SetPointReferenceUI("speed", setpoint_speed)
        self.new_waypoint_window = WaypointUI(target_waypoint_array)
        
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Aircraft Control Panel")
        self.central_widget = QtWidgets.QWidget()
        self.central_widget.setStyleSheet("background-color: #aec6cf;")
        self.setCentralWidget(self.central_widget)
        
        
        #The graphical interface layout consists of a 4x4 matrix, each position will be identified in the code
        layout = QtWidgets.QGridLayout(self.central_widget)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 1)
        layout.setColumnStretch(3, 1)
        layout.setRowStretch(0, 1)  
        layout.setRowStretch(1, 1)  
        layout.setRowStretch(2, 1)  
        layout.setRowStretch(3, 1) 

        # Positions in the Layout (row and column):
        
        #   +-----+-----+-----+-----+
        #   | 0,0 | 0,1 | 0,2 | 0,3 |
        #   +-----+-----+-----+-----+
        #   | 1,0 | 1,1 | 1,2 | 1,3 |
        #   +-----+-----+-----+-----+
        #   | 2,0 | 2,1 | 2,2 | 2,3 |
        #   +-----+-----+-----+-----+
        #   | 3,0 | 3,1 | 3,2 | 3,3 |
        #   +-----+-----+-----+-----+

        #--------------Row 0, Column 0 --------------
        self.image_label = QtWidgets.QLabel()
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)
        self.image_label.setPixmap(QtGui.QPixmap("C:/DELL-G7-15/TCC_IC/XPlaneConnect-master/Python3/src/Imagens/unifespLogo.png"))
        self.image_label.setScaledContents(True)
        layout.addWidget(self.image_label, 0, 0, 1, 1)

        #--------------Row 0, Column 1 and 2 --------------
        self.title_label = QtWidgets.QLabel("AIRCRAFT USER INTERFACE")
        fontTitle = QtGui.QFont('Arial', 24)
        fontTitle.setBold(True)  
        self.title_label.setFont(fontTitle)
        self.title_label.setStyleSheet("color: black; border: 2px solid black;")
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.title_label, 0, 1, 1, 2)

        #--------------Row 0, Column 3 --------------
        self.altitude_plot = pg.PlotWidget()
        self.altitude_plot.setTitle("Altitude")
        self.altitude_plot.setLabel('left', "Altitude (ft)")
        self.altitude_plot.setLabel('bottom', "Time (s)")
        self.altitude_data = self.altitude_plot.plot([], [])
        self.altitude_plot.setMouseEnabled(x=True, y=True)
        layout.addWidget(self.altitude_plot, 0, 3, 1, 1)



        #--------------Row 1, Column 0 --------------
        self.status_label = QtWidgets.QLabel()
        self.status_label.setFont(QtGui.QFont('Arial', 12))
        self.status_label.setStyleSheet("border: 2px solid black;")
        layout.addWidget(self.status_label, 1, 0, 1, 1)

        #--------------Row 1 and 2, Column 1 and 2 --------------

        self.map_container = QtWidgets.QWidget()
        self.map_container.setStyleSheet("border: 2px solid black; background-color: #aec6cf;")

        self.map_canvas = MplCanvas(self.map_container, width=5, height=4, dpi=100)
        container_layout = QtWidgets.QVBoxLayout(self.map_container)
        container_layout.addWidget(self.map_canvas)

        layout.addWidget(self.map_container, 1, 1, 2, 2)


        
        #--------------Row 1, Column 3 --------------
        self.pitch_plot = pg.PlotWidget()
        self.pitch_plot.setTitle("Pitch Deflection")
        self.pitch_plot.setLabel('left', "Pitch (°)")
        self.pitch_plot.setLabel('bottom', "Time (s)")
        self.pitch_data = self.pitch_plot.plot(self.time_data, self.pitch_data_list)
        self.pitch_plot.setMouseEnabled(x=True, y=True)
        layout.addWidget(self.pitch_plot, 1, 3, 1, 1)

        #--------------Row 2, Column 3 --------------
        self.roll_plot = pg.PlotWidget()
        self.roll_plot.setTitle("Roll Deflection")
        self.roll_plot.setLabel('left', "Roll (°)")
        self.roll_plot.setLabel('bottom', "Time (s)")
        self.roll_data = self.roll_plot.plot([], [])
        self.roll_plot.setMouseEnabled(x=True, y=True)
        layout.addWidget(self.roll_plot, 2, 3, 1, 1)

        #--------------Row 3, Column 2 --------------
        self.speed_plot = pg.PlotWidget()
        self.speed_plot.setTitle("Speed")
        self.speed_plot.setLabel('left', "Indicated Airspeed (kias)")
        self.speed_plot.setLabel('bottom', "Time (s)")
        self.speed_data = self.speed_plot.plot([], [])
        self.speed_plot.setMouseEnabled(x=True, y=True)
        layout.addWidget(self.speed_plot, 3, 2, 1, 1)

        #--------------Row 3, Column 3 --------------
        self.yaw_plot = pg.PlotWidget()
        self.yaw_plot.setTitle("Yaw Deflection")
        self.yaw_plot.setLabel('left', "Yaw (°)")
        self.yaw_plot.setLabel('bottom', "Time (s)")
        self.yaw_data = self.yaw_plot.plot([], [])
        self.yaw_plot.setMouseEnabled(x=True, y=True)
        layout.addWidget(self.yaw_plot, 3, 3, 1, 1)

        #--------------Row 2, Column 0 --------------

        self.controller_gains_label = QtWidgets.QLabel()
        self.controller_gains_label.setFont(QtGui.QFont('Arial', 12))
        self.controller_gains_label.setStyleSheet("border: 2px solid black;")
        layout.addWidget(self.controller_gains_label, 2, 0, 1, 1)

        
        #--------------Row 3, Column 0 --------------


        self.pid_group_box = QtWidgets.QGroupBox()
        self.pid_group_box.setStyleSheet(st.group_box_buttons_style)
        pid_layout = QtWidgets.QVBoxLayout(self.pid_group_box)

        title_label = QtWidgets.QLabel("PID Controllers")
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_label.setFont(QtGui.QFont('Arial', 14, QtGui.QFont.Bold))
        pid_layout.addWidget(title_label)

        layout.addWidget(self.pid_group_box, 3, 0, 1, 1)

        self.btn_altitude = QtWidgets.QPushButton("PID Altitude")
        self.btn_altitude.setStyleSheet(st.button_style)
        pid_layout.addWidget(self.btn_altitude)

        self.btn_speed = QtWidgets.QPushButton("PID Speed")
        self.btn_speed.setStyleSheet(st.button_style)
        pid_layout.addWidget(self.btn_speed)

        self.btn_guidance = QtWidgets.QPushButton("PID Guidance")
        self.btn_guidance.setStyleSheet(st.button_style)
        pid_layout.addWidget(self.btn_guidance)

        self.btn_altitude.clicked.connect(lambda: self.open_pid_window("altitude"))
        self.btn_speed.clicked.connect(lambda: self.open_pid_window("speed"))
        self.btn_guidance.clicked.connect(lambda: self.open_pid_window("guidance"))
  
        #--------------Row 3, Column 1 --------------
        self.reference_group_box = QtWidgets.QGroupBox()
        self.reference_group_box.setStyleSheet(st.group_box_buttons_style)
        reference_layout = QtWidgets.QVBoxLayout(self.reference_group_box)

        title_reference_label = QtWidgets.QLabel("References")
        title_reference_label.setAlignment(QtCore.Qt.AlignCenter)
        title_reference_label.setFont(QtGui.QFont('Arial', 14, QtGui.QFont.Bold))
        reference_layout.addWidget(title_reference_label)

        layout.addWidget(self.reference_group_box, 3, 1, 1 ,1)

        self.btn_altitude_reference = QtWidgets.QPushButton("Altitude Reference")
        self.btn_altitude_reference.setStyleSheet(st.button_style)
        reference_layout.addWidget(self.btn_altitude_reference)

        self.btn_speed_reference = QtWidgets.QPushButton("Speed Reference")
        self.btn_speed_reference.setStyleSheet(st.button_style)
        reference_layout.addWidget(self.btn_speed_reference)

        self.btn_new_waypoint = QtWidgets.QPushButton("New Waypoint")
        self.btn_new_waypoint.setStyleSheet(st.button_style)
        reference_layout.addWidget(self.btn_new_waypoint)

        self.btn_altitude_reference.clicked.connect(lambda: self.open_reference_window("altitude_reference"))
        self.btn_speed_reference.clicked.connect(lambda: self.open_reference_window("speed_reference"))
        self.btn_new_waypoint.clicked.connect(lambda: self.open_reference_window("new_waypoint")) 

    def open_pid_window(self, pid_type):
        if pid_type == "altitude":
            self.pid_altitude_window.show()
        elif pid_type == "speed":
            self.pid_speed_window.show()
        elif pid_type == "guidance":
            self.pid_guidance_window.show()

    def open_reference_window(self, reference_window):
        if reference_window == "altitude_reference":
            self.altitude_reference_window.show() 
        elif reference_window == "speed_reference":
            self.speed_reference_window.show()
        elif reference_window == "new_waypoint":
            self.new_waypoint_window.show()

    def update_data(self, timeC, pitch, roll, yaw, heading_angle, longitude, latitude, altitude, indicated_airspeed, true_airspeed, target_latitude, target_longitude, target_altitude, target_speed, distance_to_waypoint):
        """
        Updates the data presented in the graphical interface
        """ 
        self.timeC = timeC
        self.pitch = pitch
        self.roll = roll
        self.yaw = yaw
        self.heading_angle = heading_angle
        self.longitude = longitude
        self.latitude = latitude
        self.altitude = altitude
        self.indicated_airspeed = indicated_airspeed
        self.true_airspeed = true_airspeed
        self.target_latitude = target_latitude
        self.target_longitude = target_longitude
        self.target_altitude = self.altitude_reference_window.setpoint
        self.target_speed = self.speed_reference_window.setpoint
        self.distance_to_waypoint = distance_to_waypoint

        # To avoid problems with RAM memory, all arrays will only have a maximum of 2400 elements, 2 minutes of simulation considering that the frequency is 20hz. 20Hz*120sg = 2400 valores a cada 2min
        if(len(self.time_data)<2400):
            self.time_data.append(timeC)
            self.altitude_data_list.append(altitude)
            self.pitch_data_list.append(pitch)
            self.roll_data_list.append(roll)
            self.yaw_data_list.append(yaw)
            self.longitude_data_list.append(longitude)
            self.latitude_data_list.append(latitude)
            self.speed_data_list.append(indicated_airspeed)

        else:
            self.time_data.pop(0)
            self.time_data.append(timeC)

            self.altitude_data_list.pop(0)
            self.altitude_data_list.append(altitude)

            self.pitch_data_list.pop(0)
            self.pitch_data_list.append(pitch)

            self.roll_data_list.pop(0)
            self.roll_data_list.append(roll)

            self.yaw_data_list.pop(0)
            self.yaw_data_list.append(yaw)

            self.longitude_data_list.pop(0)
            self.longitude_data_list.append(longitude)

            self.latitude_data_list.pop(0)
            self.latitude_data_list.append(latitude)

            self.speed_data_list.pop(0)
            self.speed_data_list.append(indicated_airspeed)

        status_text = (
            "<p style='text-align: center; font-size: 14pt; font-weight: bold;'>Aircraft Metrics</p>"
            "<p style='text-align: left;'>"
            f"Time: {self.timeC:.3f}s<br>"
            f"Pitch: {self.pitch:.3f}°<br>"
            f"Roll: {self.roll:.3f}°<br>"
            f"Yaw: {self.yaw:.3f}°<br>"
            f"Heading Angle: {self.heading_angle:.3f}°<br>"
            f"Latitude: {self.latitude:.6f}°<br>"
            f"Longitude: {self.longitude:.6f}°<br>"
            f"Altitude: {self.altitude:.3f} ft<br>"
            f"Indicated Airspeed: {self.indicated_airspeed:.3f} kias<br>"
            f"True Airspeed: {self.true_airspeed:.3f} ktas"
            "</p>"
        )
        self.status_label.setText(status_text)

        controller_gains_text = (
            "<p style='text-align: center; font-size: 14pt; font-weight: bold;'>Controller Gains and Target Waypoint</p>"
            "<p style='text-align: left;'>"
            f"Altitude Kp gain: {self.pid_altitude_window.pid_controller.Kp:.3f}&nbsp;&nbsp;&nbsp;&nbsp; Target Longitude: {self.target_longitude:.6f}°<br>"
            f"Altitude Ki gain: {self.pid_altitude_window.pid_controller.Ki:.3f}&nbsp;&nbsp;&nbsp;&nbsp; Target Latitude: {self.target_latitude:.6f}°<br>"
            f"Altitude Kd gain: {self.pid_altitude_window.pid_controller.Kd:.3f}&nbsp;&nbsp;&nbsp;&nbsp; Target Altitude: {self.target_altitude:.3f} ft<br>"
            f"Speed Kp gain: {self.pid_speed_window.pid_controller.Kp:.3f}&nbsp;&nbsp;&nbsp;&nbsp; Target Speed: {self.target_speed:.3f} kias<br>"
            f"Speed Ki gain: {self.pid_speed_window.pid_controller.Ki:.3f}&nbsp;&nbsp;&nbsp;&nbsp; Distance to waypoint: {self.distance_to_waypoint:.3f} m<br>"
            f"Speed Kd gain: {self.pid_speed_window.pid_controller.Kd:.3f}<br>"
            f"Guidance Kp gain: {self.pid_guidance_window.pid_controller.Kp:.3f}<br>"
            f"Guidance Ki gain: {self.pid_guidance_window.pid_controller.Ki:.3f}<br>"
            f"Guidance Kd gain: {self.pid_guidance_window.pid_controller.Kd:.3f}<br>"
            "</p>"
        )
        self.controller_gains_label.setText(controller_gains_text)

        self.altitude_data.setData(self.time_data, self.altitude_data_list)
        self.pitch_data.setData(self.time_data, self.pitch_data_list)
        self.roll_data.setData(self.time_data, self.roll_data_list)
        self.yaw_data.setData(self.time_data, self.yaw_data_list)
        self.speed_data.setData(self.time_data, self.speed_data_list)

        self.map_canvas.axes.cla()
        self.map_canvas.axes.set_title("Airplane Position - 3D", fontdict={'fontsize': 14, 'fontweight': 'bold', 'fontname': 'Arial'})
        self.map_canvas.axes.set_xlabel("Longitude (°)")
        self.map_canvas.axes.set_ylabel("Latitude (°)")
        self.map_canvas.axes.set_zlabel("Altitude (ft)")
        self.map_canvas.axes.plot(self.longitude_data_list[:-1], self.latitude_data_list[:-1], self.altitude_data_list[:-1], 'b-')
        self.map_canvas.axes.plot([self.longitude_data_list[-1]], [self.latitude_data_list[-1]], [self.altitude_data_list[-1]], 'ro', markersize=8)
        self.map_canvas.draw()


