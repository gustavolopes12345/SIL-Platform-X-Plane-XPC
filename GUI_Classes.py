from PyQt5 import QtWidgets, QtGui, QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import PID

class PIDControllerUI(QtWidgets.QWidget):
    settings_updated = QtCore.pyqtSignal()
    def __init__(self, pid_type, pid_controller):
        super().__init__()
        self.pid_type = pid_type
        self.pid_controller = pid_controller

        self.setupUI()

    def setupUI(self):
        self.setWindowTitle(f"PID {self.pid_type.capitalize()} Configuration")
        self.setGeometry(100, 100, 300, 200) 

        layout = QtWidgets.QVBoxLayout(self)

        label = QtWidgets.QLabel(f"PID {self.pid_type.capitalize()} Settings")
        label.setFont(QtGui.QFont('Arial', 14))
        label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(label)

        self.kp_input = self.create_input_field("Proportional Gain (Kp):")
        self.ki_input = self.create_input_field("Integral Gain (Ki):")
        self.kd_input = self.create_input_field("Derivative Gain (Kd):")

        self.confirm_button = QtWidgets.QPushButton("Confirm")
        self.confirm_button.clicked.connect(self.confirm_settings)
        layout.addWidget(self.confirm_button)

    def create_input_field(self, label_text):
        """ Helper function to create a labeled input field. """
        layout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel(label_text)
        input_field = QtWidgets.QLineEdit()
        input_field.setValidator(QtGui.QDoubleValidator())
        layout.addWidget(label)
        layout.addWidget(input_field)
        self.layout().addLayout(layout)
        return input_field

    def confirm_settings(self):
        """ Slot to handle the confirmation of settings. """
        try:
            self.pid_controller.Kp = float(self.kp_input.text())
            self.pid_controller.Ki = float(self.ki_input.text())
            self.pid_controller.Kd = float(self.kd_input.text())

            self.settings_updated.emit() 
            QtWidgets.QMessageBox.information(self, "Success", f"PID {self.pid_type} settings updated successfully!")
        except ValueError:
            QtWidgets.QMessageBox.critical(self, "Input Error", "Please enter valid numeric values for all gains.")
        finally:
            self.close()

class SetPointReferenceUI(QtWidgets.QWidget):
    settings_updated = QtCore.pyqtSignal()
    def __init__(self, reference_name, setpoint):
        super().__init__()
        self.reference_name = reference_name
        self.setpoint = setpoint

        self.setupUI()

    def setupUI(self):
        self.setWindowTitle(f"New Waypoint")
        self.setGeometry(100, 100, 300, 200) 

        layout = QtWidgets.QVBoxLayout(self)

        label = QtWidgets.QLabel(f"New {self.reference_name.capitalize()} SetPoint")
        label.setFont(QtGui.QFont('Arial', 14))
        label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(label)

        self.input_reference = self.create_input_field("Enter New Reference:")

        self.confirm_button = QtWidgets.QPushButton("Confirm")
        self.confirm_button.clicked.connect(self.confirm_settings)
        layout.addWidget(self.confirm_button)

    def create_input_field(self, label_text):
        """ Helper function to create a labeled input field. """
        layout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel(label_text)
        input_field = QtWidgets.QLineEdit()
        input_field.setValidator(QtGui.QDoubleValidator())
        layout.addWidget(label)
        layout.addWidget(input_field)
        self.layout().addLayout(layout)
        return input_field

    def confirm_settings(self):
        """ Slot to handle the confirmation of settings. """
        try:
            self.setpoint = float(self.input_reference.text())
            self.settings_updated.emit() 
            QtWidgets.QMessageBox.information(self, "Success", f"New Setpoint added!")
        except ValueError:
            QtWidgets.QMessageBox.critical(self, "Input Error", "Please enter valid numeric values for setpoint.")
        finally:
            self.close() 

class WaypointUI(QtWidgets.QWidget):
    settings_updated = QtCore.pyqtSignal()
    def __init__(self, target_waypoint_array):
        super().__init__()
        self.target_waypoint_array = target_waypoint_array

        self.setupUI()

    def setupUI(self):
        self.setWindowTitle(f"New Waypoint")
        self.setGeometry(100, 100, 300, 200) 

        layout = QtWidgets.QVBoxLayout(self)

        label = QtWidgets.QLabel(f"New Waypoint")
        label.setFont(QtGui.QFont('Arial', 14))
        label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(label)

        self.new_latitude = self.create_input_field("New Latitude:")
        self.new_longitude = self.create_input_field("New Longitude:")

        self.confirm_button = QtWidgets.QPushButton("Confirm")
        self.confirm_button.clicked.connect(self.confirm_settings)
        layout.addWidget(self.confirm_button)

    def create_input_field(self, label_text):
        """ Helper function to create a labeled input field. """
        layout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel(label_text)
        input_field = QtWidgets.QLineEdit()
        input_field.setValidator(QtGui.QDoubleValidator())
        layout.addWidget(label)
        layout.addWidget(input_field)
        self.layout().addLayout(layout)
        return input_field

    def confirm_settings(self):
        """ Slot to handle the confirmation of settings. """
        try:
            new_latitude_reference = float(self.new_latitude.text())
            new_longitude_reference = float(self.new_longitude.text())
            new_waypoint = (new_latitude_reference, new_longitude_reference)

            self.target_waypoint_array.append(new_waypoint)
            self.settings_updated.emit() 
            QtWidgets.QMessageBox.information(self, "Success", f"New waypoint added!")
        except ValueError:
            QtWidgets.QMessageBox.critical(self, "Input Error", "Please enter valid numeric values for latitude and longitude.")
        finally:
            self.close() 

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111, projection='3d')
        self.axes.set_facecolor('#aec6cf')
        fig.patch.set_facecolor('#aec6cf')
        super(MplCanvas, self).__init__(fig)
