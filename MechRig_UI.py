import sys
from PySide.QtGui import *
from PySide.QtCore import *
import pymel.all as pm


if "MechRig_UI_Functions" in sys.modules:
    reload(sys.modules["MechRig_UI_Functions"])
else:
    import MechRig_UI_Functions

import MechRig_UI_Functions as uifun


import pymel.all as pm
class MechRigUI(QWidget):
    ''' An example of PySide absolute positioning; the main window
        inherits from QWidget, a convenient widget for an empty window. '''
    def __init__(self):
        
        # Initialize the object as a QWidget
        QWidget.__init__(self)
        
        # We have to set the size of the main window
        # ourselves, since we control the entire layout
        self.setMinimumSize(719, 768)
        self.setWindowTitle('Rig UI')
        
        self.combo_box_index = pm.getAttr("Global_control.controller_visibility_status")
        self.ikfk_status = uifun.read_initial_values()
        print self.ikfk_status
        
        self.switch_button_label = QLabel(self)
        self.switch_button_label.setGeometry(QRect(280, 40, 151, 20))
        self.switch_button_label.setText("Switch controllers")
        self.switch_button_label.setAlignment(Qt.AlignCenter)
        self.switch_font = QFont()
        self.switch_font.setPointSize(10)
        self.switch_font.setUnderline(True)
        self.switch_button_label.setFont(self.switch_font)
        
        self.l_frame = QFrame(self)
        self.l_frame.setGeometry(QRect(30, 50, 181, 81))
        self.l_frame.setFrameShape(QFrame.StyledPanel)
        self.l_frame.setFrameShadow(QFrame.Raised)
        
        self.l_arm_fk_push_button = QPushButton(self.l_frame)
        self.l_arm_fk_push_button.setGeometry(QRect(10, 10, 75, 23))
        self.l_arm_fk_push_button.setText("Left arm FK")
        self.l_arm_fk_push_button.clicked.connect(lambda: uifun.switch_button(self.l_arm_slider, "FK"))
        self.l_arm_fk_push_button.clicked.connect(lambda: uifun.reveal_controllers(combo_object = self.reveal_control_combo_box, part = "left_arm", mode = "fk"))
        
        
        self.l_leg_fk_push_button = QPushButton(self.l_frame)
        self.l_leg_fk_push_button.setGeometry(QRect(10, 50, 75, 23))
        self.l_leg_fk_push_button.setText("Left leg FK")
        self.l_leg_fk_push_button.clicked.connect(lambda: uifun.switch_button(self.l_leg_slider, "FK"))
        self.l_leg_fk_push_button.clicked.connect(lambda: uifun.reveal_controllers(combo_object = self.reveal_control_combo_box, part = "left_leg", mode = "fk"))
        
        self.l_arm_ik_push_button = QPushButton(self.l_frame)
        self.l_arm_ik_push_button.setGeometry(QRect(100, 10, 75, 23))
        self.l_arm_ik_push_button.setText("Left arm IK")
        self.l_arm_ik_push_button.clicked.connect(lambda: uifun.switch_button(self.l_arm_slider, "IK"))
        self.l_arm_ik_push_button.clicked.connect(lambda: uifun.reveal_controllers(combo_object = self.reveal_control_combo_box, part = "left_arm", mode = "ik"))
        
        self.l_leg_ik_push_button = QPushButton(self.l_frame)
        self.l_leg_ik_push_button.setGeometry(QRect(100, 50, 75, 23))
        self.l_leg_ik_push_button.setText("Left leg IK")
        self.l_leg_ik_push_button.clicked.connect(lambda: uifun.switch_button(self.l_leg_slider, "IK"))
        self.l_leg_ik_push_button.clicked.connect(lambda: uifun.reveal_controllers(combo_object = self.reveal_control_combo_box, part = "left_leg", mode = "ik"))
        

        self.r_frame = QFrame(self)
        self.r_frame.setGeometry(QRect(510, 50, 181, 81))
        self.r_frame.setFrameShape(QFrame.StyledPanel)
        self.r_frame.setFrameShadow(QFrame.Raised)
        
        self.r_arm_fk_push_button = QPushButton(self.r_frame)
        self.r_arm_fk_push_button.setGeometry(QRect(10, 10, 75, 23))
        self.r_arm_fk_push_button.setText("Right arm FK")
        self.r_arm_fk_push_button.clicked.connect(lambda: uifun.switch_button(self.r_arm_slider, "FK"))
        self.r_arm_fk_push_button.clicked.connect(lambda: uifun.reveal_controllers(combo_object = self.reveal_control_combo_box, part = "right_arm", mode = "fk"))
        
        self.r_leg_fk_push_button = QPushButton(self.r_frame)
        self.r_leg_fk_push_button.setGeometry(QRect(10, 50, 75, 23))
        self.r_leg_fk_push_button.setText("Right leg FK")
        self.r_leg_fk_push_button.clicked.connect(lambda: uifun.switch_button(self.r_leg_slider, "FK"))
        self.r_leg_fk_push_button.clicked.connect(lambda: uifun.reveal_controllers(combo_object = self.reveal_control_combo_box, part = "right_leg", mode = "fk"))
        
        self.r_arm_ik_push_button = QPushButton(self.r_frame)
        self.r_arm_ik_push_button.setGeometry(QRect(100, 10, 75, 23))
        self.r_arm_ik_push_button.setText("Right arm IK")
        self.r_arm_ik_push_button.clicked.connect(lambda: uifun.switch_button(self.r_arm_slider, "IK"))
        self.r_arm_ik_push_button.clicked.connect(lambda: uifun.reveal_controllers(combo_object = self.reveal_control_combo_box, part = "right_arm", mode = "ik"))
        
        self.r_leg_ik_push_button = QPushButton(self.r_frame)
        self.r_leg_ik_push_button.setGeometry(QRect(100, 50, 75, 23))
        self.r_leg_ik_push_button.setText("Right leg IK")
        self.r_leg_ik_push_button.clicked.connect(lambda: uifun.switch_button(self.r_leg_slider, "IK"))
        self.r_leg_ik_push_button.clicked.connect(lambda: uifun.reveal_controllers(combo_object = self.reveal_control_combo_box, part = "right_leg", mode = "ik"))
        
        self.arm_fk_push_button = QPushButton(self)
        self.arm_fk_push_button.setGeometry(QRect(280, 70, 75, 23))
        self.arm_fk_push_button.setText("Arm FK")
        self.arm_fk_push_button.clicked.connect(lambda: uifun.switch_button(self.l_arm_slider, "FK"))
        self.arm_fk_push_button.clicked.connect(lambda: uifun.switch_button(self.r_arm_slider, "FK"))
        self.arm_fk_push_button.clicked.connect(lambda: uifun.reveal_controllers(combo_object = self.reveal_control_combo_box, part = "left_arm", mode = "fk"))
        self.arm_fk_push_button.clicked.connect(lambda: uifun.reveal_controllers(combo_object = self.reveal_control_combo_box, part = "right_arm", mode = "fk"))
        
        self.arm_ik_push_button = QPushButton(self)
        self.arm_ik_push_button.setGeometry(QRect(360, 70, 75, 23))
        self.arm_ik_push_button.setText("Arm IK")
        self.arm_ik_push_button.clicked.connect(lambda: uifun.switch_button(self.l_arm_slider, "IK"))
        self.arm_ik_push_button.clicked.connect(lambda: uifun.switch_button(self.r_arm_slider, "IK"))
        self.arm_ik_push_button.clicked.connect(lambda: uifun.reveal_controllers(combo_object = self.reveal_control_combo_box, part = "left_arm", mode = "ik"))
        self.arm_ik_push_button.clicked.connect(lambda: uifun.reveal_controllers(combo_object = self.reveal_control_combo_box, part = "right_arm", mode = "ik"))
        
        self.leg_fk_push_button = QPushButton(self)
        self.leg_fk_push_button.setGeometry(QRect(280, 100, 75, 23))
        self.leg_fk_push_button.setText("Leg FK")
        self.leg_fk_push_button.clicked.connect(lambda: uifun.switch_button(self.l_leg_slider, "FK"))
        self.leg_fk_push_button.clicked.connect(lambda: uifun.switch_button(self.r_leg_slider, "FK"))
        self.leg_fk_push_button.clicked.connect(lambda: uifun.reveal_controllers(combo_object = self.reveal_control_combo_box, part = "left_leg", mode = "fk"))
        self.leg_fk_push_button.clicked.connect(lambda: uifun.reveal_controllers(combo_object = self.reveal_control_combo_box, part = "right_leg", mode = "fk"))
        
        self.leg_ik_push_button = QPushButton(self)
        self.leg_ik_push_button.setGeometry(QRect(360, 100, 75, 23))
        self.leg_ik_push_button.setText("Leg IK")
        self.leg_ik_push_button.clicked.connect(lambda: uifun.switch_button(self.l_leg_slider, "IK"))
        self.leg_ik_push_button.clicked.connect(lambda: uifun.switch_button(self.r_leg_slider, "IK"))
        self.leg_ik_push_button.clicked.connect(lambda: uifun.reveal_controllers(combo_object = self.reveal_control_combo_box, part = "left_leg", mode = "ik"))
        self.leg_ik_push_button.clicked.connect(lambda: uifun.reveal_controllers(combo_object = self.reveal_control_combo_box, part = "right_leg", mode = "ik"))
        
        self.list_label = QLabel(self)
        self.list_label.setGeometry(QRect(10, 170, 261, 20))
        self.list_label.setText("Controllers list")
        self.list_label.setAlignment(Qt.AlignCenter)
        self.list_font = QFont()
        self.list_font.setPointSize(10)
        self.list_font.setUnderline(True)
        self.list_label.setFont(self.list_font)
        
        self.list_widget = QListWidget(self)
        self.list_widget.setGeometry(QRect(10, 200, 256, 371))
        uifun.append_controller_list(self.list_widget)
        self.list_widget.itemClicked.connect(lambda: uifun.select_controller(self.list_widget))
        
        self.blend_label = QLabel(self)
        self.blend_label.setGeometry(QRect(280, 170, 191, 20))
        self.blend_label.setText("Blend controllers")
        self.blend_label.setAlignment(Qt.AlignCenter)
        self.blend_font = QFont()
        self.blend_font.setPointSize(10)
        self.blend_font.setUnderline(True)
        self.blend_label.setFont(self.blend_font)
        
        
        self.blend_frame = QFrame(self)
        self.blend_frame.setGeometry(QRect(280, 200, 191, 371))
        self.blend_frame.setFrameShape(QFrame.StyledPanel)
        self.blend_frame.setFrameShadow(QFrame.Raised)
        
        self.blend_fk_label = QLabel(self.blend_frame)
        self.blend_fk_label.setGeometry(QRect(10, 40, 16, 16))
        self.blend_fk_label.setText("FK")
        blend_fk_font = QFont()
        blend_fk_font.setPointSize(10)
        self.blend_fk_label.setFont(blend_fk_font)
        
        self.blend_ik_label = QLabel(self.blend_frame)
        self.blend_ik_label.setGeometry(QRect(160, 40, 16, 16))
        self.blend_ik_label.setText("IK")
        blend_ik_font = QFont()
        blend_ik_font.setPointSize(10)
        self.blend_ik_label.setFont(blend_ik_font)
        
        self.l_arm_slider_label = QLabel(self.blend_frame)
        self.l_arm_slider_label.setText("Left Arm")
        self.l_arm_slider_label.setGeometry(QRect(70, 40, 46, 16))
        self.l_arm_slider_label.setAlignment(Qt.AlignCenter)
        self.l_arm_slider = QSlider(self.blend_frame)
        self.l_arm_slider.setGeometry(QRect(10, 70, 171, 19))
        self.l_arm_slider.setOrientation(Qt.Horizontal)
        self.l_arm_slider.setMaximum(100)
        self.l_arm_slider_display = QLineEdit(self.blend_frame)
        self.l_arm_slider_display.setGeometry(QRect(80, 90, 30, 20))
        self.l_arm_slider_display.setText("0")
        self.l_arm_slider_display.setAlignment(Qt.AlignCenter)
        self.l_arm_slider.valueChanged.connect(lambda :uifun.slider_value_change(self.l_arm_slider, self.l_arm_slider_display, "l_arm_ikfk"))
        self.l_arm_slider_display.returnPressed.connect(lambda: uifun.slider_text_change(self.l_arm_slider_display, self.l_arm_slider))
        self.l_arm_slider.valueChanged.connect(lambda: uifun.set_controller(joints_list = "left_arm", slider_object = self.l_arm_slider))
        
        
        self.r_arm_slider_label = QLabel(self.blend_frame)
        self.r_arm_slider_label.setText("Right Arm")
        self.r_arm_slider_label.setGeometry(QRect(70, 130, 48, 16))
        self.r_arm_slider_label.setAlignment(Qt.AlignCenter)
        self.r_arm_slider = QSlider(self.blend_frame)
        self.r_arm_slider.setGeometry(QRect(10, 150, 171, 19))
        self.r_arm_slider.setOrientation(Qt.Horizontal)
        self.r_arm_slider.setMaximum(100)
        self.r_arm_slider_display = QLineEdit(self.blend_frame)
        self.r_arm_slider_display.setGeometry(QRect(80, 170, 30, 20))
        self.r_arm_slider_display.setText("0")
        self.r_arm_slider_display.setAlignment(Qt.AlignCenter)
        self.r_arm_slider.valueChanged.connect(lambda :uifun.slider_value_change(self.r_arm_slider, self.r_arm_slider_display, "r_arm_ikfk"))
        self.r_arm_slider_display.returnPressed.connect(lambda: uifun.slider_text_change(self.r_arm_slider_display, self.r_arm_slider))
        self.r_arm_slider.valueChanged.connect(lambda: uifun.set_controller(joints_list = "right_arm", slider_object = self.r_arm_slider))
        
        self.l_leg_slider_label = QLabel(self.blend_frame)
        self.l_leg_slider_label.setText("Left Leg")
        self.l_leg_slider_label.setGeometry(QRect(70, 210, 46, 16))
        self.l_leg_slider_label.setAlignment(Qt.AlignCenter)        
        self.l_leg_slider = QSlider(self.blend_frame)
        self.l_leg_slider.setGeometry(QRect(10, 230, 171, 19))
        self.l_leg_slider.setOrientation(Qt.Horizontal)
        self.l_leg_slider.setMaximum(100)
        self.l_leg_slider_display = QLineEdit(self.blend_frame)
        self.l_leg_slider_display.setGeometry(QRect(80, 250, 30, 20))
        self.l_leg_slider_display.setText("0")
        self.l_leg_slider_display.setAlignment(Qt.AlignCenter)
        self.l_leg_slider.valueChanged.connect(lambda :uifun.slider_value_change(self.l_leg_slider, self.l_leg_slider_display, "l_leg_ikfk"))
        self.l_leg_slider_display.returnPressed.connect(lambda: uifun.slider_text_change(self.l_leg_slider_display, self.l_leg_slider))
        self.l_leg_slider.valueChanged.connect(lambda: uifun.set_controller(joints_list = "left_leg", slider_object = self.l_leg_slider))
        
        self.r_leg_slider_label = QLabel(self.blend_frame)
        self.r_leg_slider_label.setText("Right Leg")
        self.r_leg_slider_label.setGeometry(QRect(70, 290, 46, 16))
        self.r_leg_slider_label.setAlignment(Qt.AlignCenter) 
        self.r_leg_slider = QSlider(self.blend_frame)
        self.r_leg_slider.setGeometry(QRect(10, 310, 171, 19))
        self.r_leg_slider.setOrientation(Qt.Horizontal)
        self.r_leg_slider.setMaximum(100)
        self.r_leg_slider_display = QLineEdit(self.blend_frame)
        self.r_leg_slider_display.setGeometry(QRect(80, 330, 30, 20))
        self.r_leg_slider_display.setText("0")
        self.r_leg_slider_display.setAlignment(Qt.AlignCenter)
        self.r_leg_slider.valueChanged.connect(lambda :uifun.slider_value_change(self.r_leg_slider, self.r_leg_slider_display, "r_leg_ikfk"))
        self.r_leg_slider_display.returnPressed.connect(lambda: uifun.slider_text_change(self.r_leg_slider_display, self.r_leg_slider))
        self.r_leg_slider.valueChanged.connect(lambda: uifun.set_controller(joints_list = "right_leg", slider_object = self.r_leg_slider))
        
        self.switch_all_fk_push_button = QPushButton(self)
        self.switch_all_fk_push_button.setGeometry(QRect(500, 170, 201, 23))
        self.switch_all_fk_push_button.setText("Switch all to FK")
        self.switch_all_fk_push_button.clicked.connect(lambda: uifun.switch_button(self.all_control_blend_slider, "FK"))
        self.switch_all_fk_push_button.clicked.connect(lambda: uifun.reveal_controllers(combo_object = self.reveal_control_combo_box, part = "left_arm", mode = "fk"))
        self.switch_all_fk_push_button.clicked.connect(lambda: uifun.reveal_controllers(combo_object = self.reveal_control_combo_box, part = "right_arm", mode = "fk"))
        self.switch_all_fk_push_button.clicked.connect(lambda: uifun.reveal_controllers(combo_object = self.reveal_control_combo_box, part = "left_leg", mode = "fk"))
        self.switch_all_fk_push_button.clicked.connect(lambda: uifun.reveal_controllers(combo_object = self.reveal_control_combo_box, part = "right_leg", mode = "fk"))
        self.switch_all_fk_push_button.clicked.connect(lambda: uifun.set_controller(slider_object = self.all_control_blend_slider, controller = "FK", joints_list = "all"))

        self.switch_all_ik_push_button = QPushButton(self)
        self.switch_all_ik_push_button.setGeometry(QRect(500, 200, 201, 23))
        self.switch_all_ik_push_button.setText("Switch all to IK")
        self.switch_all_ik_push_button.clicked.connect(lambda: uifun.switch_button(self.all_control_blend_slider, "IK"))
        self.switch_all_ik_push_button.clicked.connect(lambda: uifun.reveal_controllers(combo_object = self.reveal_control_combo_box, part = "left_arm", mode = "ik"))
        self.switch_all_ik_push_button.clicked.connect(lambda: uifun.reveal_controllers(combo_object = self.reveal_control_combo_box, part = "right_arm", mode = "ik"))
        self.switch_all_ik_push_button.clicked.connect(lambda: uifun.reveal_controllers(combo_object = self.reveal_control_combo_box, part = "left_leg", mode = "ik"))
        self.switch_all_ik_push_button.clicked.connect(lambda: uifun.reveal_controllers(combo_object = self.reveal_control_combo_box, part = "right_leg", mode = "ik"))
        self.switch_all_ik_push_button.clicked.connect(lambda: uifun.set_controller(slider_object = self.all_control_blend_slider, controller = "IK", joints_list = "all"))

        self.all_control_blend = QLabel(self)
        self.all_control_blend.setGeometry(QRect(550, 260, 111, 20))
        self.all_control_blend_font = QFont()
        self.all_control_blend_font.setPointSize(9)
        self.all_control_blend_font.setUnderline(True)
        self.all_control_blend.setFont(self.all_control_blend_font)
        self.all_control_blend.setText("All control blend")

        self.all_control_blend_fk = QLabel(self)
        self.all_control_blend_fk.setGeometry(QRect(520, 280, 16, 16))
        self.all_control_blend_fk_font = QFont()
        self.all_control_blend_fk_font.setPointSize(10)
        self.all_control_blend_fk.setFont(self.all_control_blend_fk_font)
        self.all_control_blend_fk.setText("FK")
        self.all_control_blend_ik = QLabel(self)
        self.all_control_blend_ik.setGeometry(QRect(680, 280, 16, 16))
        self.all_control_blend_ik_font = QFont()
        self.all_control_blend_ik_font.setPointSize(10)
        self.all_control_blend_ik.setFont(self.all_control_blend_ik_font)
        self.all_control_blend_ik.setText("IK")
        self.all_control_blend_slider = QSlider(self)
        self.all_control_blend_slider.setGeometry(QRect(520, 300, 171, 19))
        self.all_control_blend_slider.setOrientation(Qt.Horizontal)
        self.all_control_blend_slider.setMaximum(100)
        self.all_control_blend_slider_display = QLineEdit(self)
        self.all_control_blend_slider_display.setGeometry(QRect(590, 320, 30, 20))

        self.all_control_blend_slider_display.setAlignment(Qt.AlignCenter)
        self.all_control_blend_slider_display.setText("0")
        self.all_control_blend_slider.valueChanged.connect(lambda :uifun.full_blend_slider_change(self.all_control_blend_slider, self.l_arm_slider))
        self.all_control_blend_slider.valueChanged.connect(lambda :uifun.full_blend_slider_change(self.all_control_blend_slider, self.r_arm_slider))
        self.all_control_blend_slider.valueChanged.connect(lambda :uifun.full_blend_slider_change(self.all_control_blend_slider, self.l_leg_slider))
        self.all_control_blend_slider.valueChanged.connect(lambda :uifun.full_blend_slider_change(self.all_control_blend_slider, self.r_leg_slider))
        self.all_control_blend_slider.valueChanged.connect(lambda :uifun.slider_value_change(self.all_control_blend_slider, self.all_control_blend_slider_display, "all_blend_ikfk"))
        self.all_control_blend_slider_display.returnPressed.connect(lambda: uifun.slider_text_change(self.all_control_blend_slider_display, self.all_control_blend_slider))

        self.snap_fk_ik_label = QLabel(self)
        self.snap_fk_ik_label.setGeometry(QRect(515, 380, 161, 20))
        self.snap_fk_ik_label_font = QFont()
        self.snap_fk_ik_label_font.setPointSize(10)
        self.snap_fk_ik_label_font.setUnderline(True)
        self.snap_fk_ik_label.setFont(self.snap_fk_ik_label_font)
        self.snap_fk_ik_label.setAlignment(Qt.AlignCenter)
        self.snap_fk_ik_label.setText("Snap FK to IK position")
        
        self.l_arm_fk_ik_push_button = QPushButton(self)
        self.l_arm_fk_ik_push_button.setGeometry(QRect(500, 410, 95, 23))
        self.l_arm_fk_ik_push_button.setText("Left Arm Fk to IK")
        self.l_arm_fk_ik_push_button.clicked.connect(lambda: uifun.snap_controllers(joint_list = "left_arm", snap_control = "fk_to_ik"))
        
        self.r_arm_fk_ik_push_button = QPushButton(self)
        self.r_arm_fk_ik_push_button.setGeometry(QRect(600, 410, 95, 23))
        self.r_arm_fk_ik_push_button.setText("Right Arm Fk to IK")
        self.r_arm_fk_ik_push_button.clicked.connect(lambda: uifun.snap_controllers(joint_list = "right_arm", snap_control = "fk_to_ik"))
        
        self.l_leg_fk_ik_push_button = QPushButton(self)
        self.l_leg_fk_ik_push_button.setGeometry(QRect(500, 440, 95, 23))
        self.l_leg_fk_ik_push_button.setText("Left Leg Fk to IK")
        self.l_leg_fk_ik_push_button.clicked.connect(lambda: uifun.snap_controllers(joint_list = "left_leg", snap_control = "fk_to_ik"))
        
        self.r_leg_fk_ik_push_button = QPushButton(self)
        self.r_leg_fk_ik_push_button.setGeometry(QRect(600, 440, 95, 23))
        self.r_leg_fk_ik_push_button.setText("Right Leg Fk to IK")
        self.r_leg_fk_ik_push_button.clicked.connect(lambda: uifun.snap_controllers(joint_list = "right_leg", snap_control = "fk_to_ik"))

        self.snap_ik_fk_label = QLabel(self)
        self.snap_ik_fk_label.setGeometry(QRect(520, 470, 161, 20))
        self.snap_ik_fk_label_font = QFont()
        self.snap_ik_fk_label_font.setPointSize(10)
        self.snap_ik_fk_label_font.setUnderline(True)
        self.snap_ik_fk_label.setFont(self.snap_ik_fk_label_font)
        self.snap_ik_fk_label.setAlignment(Qt.AlignCenter)
        self.snap_ik_fk_label.setText("Snap IK to FK position")

        self.l_arm_ik_fk_push_button = QPushButton(self)
        self.l_arm_ik_fk_push_button.setGeometry(QRect(495, 500, 100, 23))
        self.l_arm_ik_fk_push_button.setText("Left Arm IK to FK")
        self.l_arm_ik_fk_push_button.clicked.connect(lambda: uifun.snap_controllers(joint_list = "left_arm", snap_control = "ik_to_fk"))

        self.r_arm_ik_fk_push_button = QPushButton(self)
        self.r_arm_ik_fk_push_button.setGeometry(QRect(600, 500, 100, 23))
        self.r_arm_ik_fk_push_button.setText("Right Arm IK to FK")
        self.r_arm_ik_fk_push_button.clicked.connect(lambda: uifun.snap_controllers(joint_list = "right_arm", snap_control = "ik_to_fk"))

        self.l_leg_ik_fk_push_button = QPushButton(self)
        self.l_leg_ik_fk_push_button.setGeometry(QRect(495, 530, 100, 23))
        self.l_leg_ik_fk_push_button.setText("Left Leg IK to FK")
        self.l_leg_ik_fk_push_button.clicked.connect(lambda: uifun.snap_controllers(joint_list = "left_leg", snap_control = "ik_to_fk"))

        self.r_leg_ik_fk_push_button = QPushButton(self)
        self.r_leg_ik_fk_push_button.setGeometry(QRect(600, 530, 100, 23))
        self.r_leg_ik_fk_push_button.setText("Right Leg IK to FK")
        self.r_leg_ik_fk_push_button.clicked.connect(lambda: uifun.snap_controllers(joint_list = "right_leg", snap_control = "ik_to_fk"))

        self.reveal_control_combo_box = QComboBox(self)
        self.reveal_control_combo_box.setGeometry(QRect(250, 10, 211, 22))
        self.reveal_control_combo_box.setObjectName("comboBox")
        self.reveal_control_combo_box.addItem("Reveal switched controllers")
        self.reveal_control_combo_box.addItem("Reveal all FK controllers")
        self.reveal_control_combo_box.addItem("Reveal all IK controllers")
        self.reveal_control_combo_box.addItem("Reveal all FK controllers only")
        self.reveal_control_combo_box.addItem("Reveal all IK controllers only")
        self.reveal_control_combo_box.addItem("Reveal all controllers")
        self.reveal_control_combo_box.addItem("Hide all controllers")
        self.reveal_control_combo_box.setCurrentIndex(self.combo_box_index)
        self.reveal_control_combo_box.currentIndexChanged.connect(lambda :uifun.reveal_controllers(combo_object = self.reveal_control_combo_box, part=None, mode=None))
        
        self.h_line = QFrame(self)
        self.h_line.setGeometry(QRect(-10, 580, 731, 16))
        self.h_line.setFrameShape(QFrame.HLine)
        self.h_line.setFrameShadow(QFrame.Sunken)
        
        self.v_line = QFrame(self)
        self.v_line.setGeometry(QRect(443, 620, 20, 151))
        self.v_line.setFrameShape(QFrame.VLine)
        self.v_line.setFrameShadow(QFrame.Sunken)
        
        self.key_controller_label = QLabel(self)
        self.key_controller_label.setGeometry(QRect(10, 590, 441, 31))
        self.key_controllers_font = QFont()
        self.key_controllers_font.setPointSize(13)
        self.key_controllers_font.setUnderline(True)
        self.key_controller_label.setFont(self.key_controllers_font)
        self.key_controller_label.setAlignment(Qt.AlignCenter)
        self.key_controller_label.setText("Key controllers")
        
        self.key_ikfk_label = QLabel(self)
        self.key_ikfk_label.setGeometry(QRect(460, 590, 261, 31))
        self.key_ikfk_label_font = QFont()
        self.key_ikfk_label_font.setPointSize(13)
        self.key_ikfk_label_font.setUnderline(True)
        self.key_ikfk_label.setFont(self.key_ikfk_label_font)
        self.key_ikfk_label.setAlignment(Qt.AlignCenter)
        self.key_ikfk_label.setText("Key IK/FK Blend/Switch")
        
        self.key_current_selection_push_button = QPushButton(self)
        self.key_current_selection_push_button.setGeometry(QRect(160, 630, 121, 31))
        self.key_current_selection_push_button.setText("Current selection")
        self.key_current_selection_push_button.clicked.connect(lambda: uifun.set_key(mode = "SELECTION"))
        
        self.key_l_arm_fk_push_button = QPushButton(self)
        self.key_l_arm_fk_push_button.setGeometry(QRect(10, 670, 91, 31))
        self.key_l_arm_fk_push_button.setText("L Arm FK")
        self.key_l_arm_fk_push_button.clicked.connect(lambda: uifun.set_key(mode = "FK", side = "left", part = "arm"))
        
        self.key_l_arm_ik_push_button = QPushButton(self)
        self.key_l_arm_ik_push_button.setGeometry(QRect(110, 670, 91, 31))
        self.key_l_arm_ik_push_button.setText("L Arm IK")
        self.key_l_arm_ik_push_button.clicked.connect(lambda: uifun.set_key(mode = "IK", side = "left", part = "arm"))
        
        self.key_l_leg_fk_push_button = QPushButton(self)
        self.key_l_leg_fk_push_button.setGeometry(QRect(10, 710, 91, 31))
        self.key_l_leg_fk_push_button.setText("L Leg FK")
        self.key_l_leg_fk_push_button.clicked.connect(lambda: uifun.set_key(mode = "FK", side = "left", part = "leg"))
        
        self.key_l_leg_ik_push_button = QPushButton(self)
        self.key_l_leg_ik_push_button.setGeometry(QRect(110, 710, 91, 31))
        self.key_l_leg_ik_push_button.setText("L Leg IK")
        self.key_l_leg_ik_push_button.clicked.connect(lambda: uifun.set_key(mode = "IK", side = "left", part = "leg"))
        
        self.key_r_arm_fk_push_button = QPushButton(self)
        self.key_r_arm_fk_push_button.setGeometry(QRect(230, 670, 91, 31))
        self.key_r_arm_fk_push_button.setText("R Arm FK")
        self.key_r_arm_fk_push_button.clicked.connect(lambda: uifun.set_key(mode = "FK", side = "right", part = "arm"))
        
        self.key_r_arm_ik_push_button = QPushButton(self)
        self.key_r_arm_ik_push_button.setGeometry(QRect(330, 670, 91, 31))
        self.key_r_arm_ik_push_button.setText("R Arm IK")
        self.key_r_arm_ik_push_button.clicked.connect(lambda: uifun.set_key(mode = "IK", side = "right", part = "arm"))
        
        self.key_r_leg_fk_push_button = QPushButton(self)
        self.key_r_leg_fk_push_button.setGeometry(QRect(230, 710, 91, 31))
        self.key_r_leg_fk_push_button.setText("R Leg FK")
        self.key_r_leg_fk_push_button.clicked.connect(lambda: uifun.set_key(mode = "FK", side = "right", part = "leg"))
        
        self.key_r_leg_ik_push_button = QPushButton(self)
        self.key_r_leg_ik_push_button.setGeometry(QRect(330, 710, 91, 31))
        self.key_r_leg_ik_push_button.setText("R Leg IK")
        self.key_r_leg_ik_push_button.clicked.connect(lambda: uifun.set_key(mode = "IK", side = "right", part = "leg"))
        
        
        self.key_l_arm_ikfk_blend_push_button = QPushButton(self)
        self.key_l_arm_ikfk_blend_push_button.setGeometry(QRect(500, 670, 91, 31))
        self.key_l_arm_ikfk_blend_push_button.setText("L Arm IK/FK")
        self.key_l_arm_ikfk_blend_push_button.clicked.connect(lambda: pm.setKeyframe("Global_control.l_arm_ikfk"))
        
        self.key_r_arm_ikfk_blend_push_button = QPushButton(self)
        self.key_r_arm_ikfk_blend_push_button.setGeometry(QRect(600, 670, 91, 31))
        self.key_r_arm_ikfk_blend_push_button.setText("R Arm IK/FK")
        self.key_r_arm_ikfk_blend_push_button.clicked.connect(lambda: pm.setKeyframe("Global_control.r_arm_ikfk"))
        
        self.key_l_leg_ikfk_blend_push_button = QPushButton(self)
        self.key_l_leg_ikfk_blend_push_button.setGeometry(QRect(500, 710, 91, 31))
        self.key_l_leg_ikfk_blend_push_button.setText("L Leg IK/FK")
        self.key_l_leg_ikfk_blend_push_button.clicked.connect(lambda: pm.setKeyframe("Global_control.l_leg_ikfk"))
        
        self.key_r_leg_ikfk_blend_push_button = QPushButton(self)
        self.key_r_leg_ikfk_blend_push_button.setGeometry(QRect(600, 710, 91, 31))
        self.key_r_leg_ikfk_blend_push_button.setText("R Leg IK/FK")
        self.key_r_leg_ikfk_blend_push_button.clicked.connect(lambda: pm.setKeyframe("Global_control.r_leg_ikfk"))
             
        self.key_all_ikfk_blend_push_button = QPushButton(self)
        self.key_all_ikfk_blend_push_button.setGeometry(QRect(500, 630, 191, 31))
        self.key_all_ikfk_blend_push_button.setText("All control IK/FK")
        self.key_all_ikfk_blend_push_button.clicked.connect(lambda: pm.setKeyframe("Global_control.all_blend_ikfk"))
        
        
        
        
        self.all_control_blend_slider.setValue(self.ikfk_status[0]*100)
        self.l_arm_slider.setValue(self.ikfk_status[1]*100)
        self.r_arm_slider.setValue(self.ikfk_status[2]*100)
        self.l_leg_slider.setValue(self.ikfk_status[3]*100)
        self.r_leg_slider.setValue(self.ikfk_status[4]*100)
        
    def run(self):
        qt_app = QApplication.instance()
        if qt_app == None:
            qt_app = QApplication(sys.argv)
        frame = MechRigUI()
        frame.show()
        qt_app.exec_()

# Create an instance of the application window and run it
#app = MechRigUI()
#app.run()

