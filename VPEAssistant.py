'''
 Written by Chiara Ruggeri (chiara.2312@hotmail.it).
 
 This is a free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 2 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program; if not, write to the Free Software
 Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

'''
#pyinstaller --onefile --windowed --icon="tmfavicon.ico" --add-data="color-logo.jpg;." --add-data="4907157.jpg;." --add-data="add-file.png;." --add-data="add-friend.png;." --add-data="diskette.png;." --add-data="help.png;." --add-data="idea.png;." --add-data="lamp.png;." --add-data="login.png;." --add-data="old-man.png;." --add-data="pencil.png;." --add-data="people.png;." --add-data="remove-friend.png;." --add-data="schedule.png;." --add-data="shield.png;." --add-data="speaker.png;." --add-data="tmfavicon.ico;." --add-data="volunteer.png;." --add-data="smallLogo.jpg;." --add-data="warning.png;." --add-data="check.png;." VPEAssistant.py
# [cr] freepik (background)
# flaticon (icons)

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QDialog, QVBoxLayout, QGridLayout, QHBoxLayout, QFormLayout, QCheckBox, QToolBox, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox
from PyQt5.QtGui import QColor, QFontMetrics
from PyQt5.QtCore import QPropertyAnimation, QPoint, QEasingCurve, Qt
import sqlite3 as sl
import sys
import os
import time
import datetime
import sip

internalDB = None
workingDirectory = os.path.join('~', 'Documents', 'Toastmasters', 'VPEAssistant') # members' data will be saved here (e.g. C:\Users\User\Documents\Toastmasters\VPEAssistant)

# MEMBERS table indexes
ID_POS 			= 0
NAME_POS 		= 1
LASTSPEECH_POS	= 2
LASTTMOD_POS	= 3
LASTGENEVAL_POS	= 4
LASTEVAL_POS	= 5
LASTTIMER_POS	= 6
LASTGRAMM_POS	= 7
LASTAHCOUNT_POS	= 8
LASTHUM_POS		= 9
LASTTTM_POS		= 10
LASTHACKM_POS	= 11
NOTES_POS		= 12
ACTIVE_POS		= 13
MEETINGWR_POS	= 14
MENTOR_POS		= 15
NEEDMENTOR_POS	= 16

# CURRENTMEETING table indexes
CT_NAME_POS		= 1
CT_DURATION_POS	= 2
CT_DATE_POS		= 3
CT_SPEAKER1_POS	= 4
CT_SPEAKER2_POS	= 5
CT_TMOD_POS		= 6
CT_GENEVAL_POS	= 7
CT_EVAL1_POS	= 8
CT_EVAL2_POS	= 9
CT_TIMER_POS	= 10
CT_GRAMM_POS	= 11
CT_AHCOUNT_POS	= 12
CT_HUM_POS		= 13
CT_TTM_POS		= 14
CT_HACKM_POS	= 15
CT_PRES_POS		= 16

# ADDITIONALROLES table indexes
AT_NAME_POS		= 0
AT_TYPE_POS		= 1
AT_MEMBER_POS	= 2

# roles
rolesName = [('TMoD', 'lastTMOD', CT_TMOD_POS, "TMOD"), ("Timer", "lastTimer", CT_TIMER_POS, "Timer"), ("Grammarian", "lastGrammarian", CT_GRAMM_POS, "Grammarian"), ("Ah counter", "lastAhCounter", CT_AHCOUNT_POS, "AhCounter"), ("Humorist", "lastHumorist", CT_HUM_POS, "Humorist"), ("Table Topic Master", "lastTTM", CT_TTM_POS, "TTM"), ("General Evaluator", "lastGenEval", CT_GENEVAL_POS, "GenEval"), ("Hack Master", "lastHackMaster", CT_HACKM_POS, "HackMaster"), ("1st Speaker", 'lastSpeech', CT_SPEAKER1_POS, "speaker1"), ("1st Evaluator", "lastEval", CT_EVAL1_POS, "Eval1"), ("2nd Speaker", 'lastSpeech', CT_SPEAKER2_POS, "speaker2"), ("2nd Evaluator", "lastEval", CT_EVAL2_POS, "Eval2")]
rolesType = [("Speaker", 'lastSpeech', LASTSPEECH_POS), ("Evaluator", "lastEval", LASTEVAL_POS), ('TMoD', 'lastTMOD', LASTTMOD_POS), ("Timer", "lastTimer", LASTTIMER_POS), ("Grammarian", "lastGrammarian", LASTGRAMM_POS), ("Ah counter", "lastAhCounter", LASTAHCOUNT_POS), ("Humorist", "lastHumorist", LASTHUM_POS), ("Table Topic Master", "lastTTM", LASTTTM_POS), ("General Evaluator", "lastGenEval", LASTGENEVAL_POS), ("Hack Master", "lastHackMaster", LASTHACKM_POS), ("Custom", "custom", 255)]
rolesPriority = ["lastAhCounter", "lastTimer", "lastHackMaster", "lastGrammarian", "lastHumorist", "lastEval", "lastTTM", "lastTMOD", "lastGenEval"]

# background signaling
greenBackground = ['rgba(0, 255, 0, 1)', 'rgba(0, 255, 0, 0.9)', 'rgba(0, 255, 0, 0.8)', 'rgba(0, 255, 0, 0.7)', 'rgba(0, 255, 0, 0.6)', 'rgba(0, 255, 0, 0.5)', 'rgba(0, 255, 0, 0.4)', 'rgba(0, 255, 0, 0.3)', 'rgba(0, 255, 0, 0.2)', 'rgba(0, 255, 0, 0.1)']
redBackground = ['rgba(255, 0, 0, 1)', 'rgba(255, 0, 0, 0.9)', 'rgba(255, 0, 0, 0.8)', 'rgba(255, 0, 0, 0.7)', 'rgba(255, 0, 0, 0.6)', 'rgba(255, 0, 0, 0.5)', 'rgba(255, 0, 0, 0.4)', 'rgba(255, 0, 0, 0.3)', 'rgba(255, 0, 0, 0.2)', 'rgba(255, 0, 0, 0.1)']


try:
	_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s

def getTimestampFromQDate(date):
	formalDate = date.strftime('%d/%m/%Y %H:%M:%S')
	tstamp = time.mktime(datetime.datetime.strptime(formalDate, '%d/%m/%Y %H:%M:%S').timetuple())
	return tstamp

def getQDateFromTimestamp(timestamp):
	unix_timestamp = float(timestamp)
	local_datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(unix_timestamp))   # converts timestampt to local time and apply the format 
	local_date = local_datetime.split(" ")[0]   # get only the date
	d = QtCore.QDate.fromString(local_date, "yyyy-MM-dd")   # Convert date into QDate object
	return d



################### First tab #####################
##################### Agenda ######################
class Role(QtWidgets.QWidget):
	dropDown = QtCore.pyqtSignal(QtWidgets.QComboBox, str)
	selectionChanged = QtCore.pyqtSignal(QtWidgets.QComboBox)
	endSelection = QtCore.pyqtSignal(QtWidgets.QComboBox)
	currentSelection = ''

	def __init__(self, roleName, roleType):
		if getattr(sys, 'frozen', False):
			application_path = sys._MEIPASS
		elif __file__:
			application_path = os.path.dirname(__file__)
		QtWidgets.QGroupBox.__init__(self)
		self.roleName = roleName
		self.roleType = roleType
		label = QtWidgets.QLabel()
		label.setText(self.roleName)
		horizontalSpacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
		self.comboBox = ComboBox()
		self.comboBox.dropDown.connect(self.updateCombo)
		self.comboBox.popup.connect(self.popup)
		self.comboBox.currentTextChanged.connect(self.checkSelection)
		self.comboBox.hideicon.connect(self.hide)
		self.label_img = QtWidgets.QLabel(self)
		self.label_img.setPixmap(QtGui.QIcon(os.path.join(application_path, 'lamp.png')).pixmap(20,20))
		self.label_img.mousePressEvent = self.hideIcon
		self.label_img.setMaximumSize(20,20)
		self.label_img.setVisible(False)
		hbox = QHBoxLayout()
		hbox.addWidget(label)
		hbox.addItem(horizontalSpacer)
		hbox.addWidget(self.label_img, 0)
		hbox.addWidget(self.comboBox)
		self.setLayout(hbox)
		
	def getComboBox(self):
		return self.comboBox

	def getRoleType(self):
		return self.roleType

	def getRoleName(self):
		return self.roleName

	def updateCombo(self):
		self.dropDown.emit(self.comboBox, self.roleType)

	def checkSelection(self):
		if self.comboBox.currentText() != self.currentSelection:
			self.currentSelection = self.comboBox.currentText()
			self.hideIcon(None)
		self.selectionChanged.emit(self.comboBox)

	def popup(self):
		self.endSelection.emit(self.comboBox)

	def setSuggested(self, tooltip):
		self.label_img.setVisible(True)
		self.label_img.setToolTip(tooltip)

	def hideIcon(self, event):
		self.label_img.setVisible(False)

	def hide(self):
		self.label_img.setVisible(False)



# catch check/uncheck event and emit a signal
class CustomCheckbox(QCheckBox):
	checked = QtCore.pyqtSignal(QCheckBox)

	def __init__(self):
		super(CustomCheckbox, self).__init__()
		self.stateChanged.connect(self.emitEvent)

	def emitEvent(self):
		self.checked.emit(self)

# chatch showPopup event and emit a signal
class ComboBox(QtWidgets.QComboBox):
	dropDown = QtCore.pyqtSignal(QtWidgets.QComboBox)
	popup = QtCore.pyqtSignal(QtWidgets.QComboBox)
	hideicon = QtCore.pyqtSignal()

	def showPopup(self):
		self.dropDown.emit(self)
		super(ComboBox, self).showPopup()

	def hidePopup(self):
		self.popup.emit(self)
		super(ComboBox, self).hidePopup()

	def hideIcon(self):
		self.hideicon.emit()

class CreateAgenda(QtWidgets.QWidget):
	updateMembersData = QtCore.pyqtSignal()
	timer = QtCore.QTimer()
	additionalRoles = []
	disableEdit = False

	def __init__(self):
		global internalDB
		super(CreateAgenda, self).__init__()

		if getattr(sys, 'frozen', False):
			application_path = sys._MEIPASS
		elif __file__:
			application_path = os.path.dirname(__file__)

		self.timer.setSingleShot(True)

		data = internalDB.execute("SELECT * FROM CURRENTMEETING")
		meetingData = data.fetchone()

		# widgets with no agenda in progress
		self.newWidget = QtWidgets.QWidget()
		button = QtWidgets.QPushButton()
		button.clicked.connect(self.newMeeting)
		button.setText("New Meeting")
		button.setIcon(QtGui.QIcon(os.path.join(application_path, 'add-file.png')))
		verticalSpacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
		horizontalSpacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		hbox = QHBoxLayout()
		hbox.addItem(horizontalSpacer)
		hbox.addWidget(button)
		hbox.addItem(horizontalSpacer)
		vbox = QVBoxLayout()
		vbox.addItem(verticalSpacer)
		vbox.addLayout(hbox)
		vbox.addItem(verticalSpacer)
		self.newWidget.setLayout(vbox)

		# widgets with agenda in progress
		self.agendaWidget = QtWidgets.QWidget()
		self.agendaWidget.setObjectName("agendaWidget")
		self.agendaWidget.setStyleSheet('QLabel{font-size: 16px; font-weight: bold; font-family: "Monaco", "Courier New", monospace;}')
		splitter = QtWidgets.QSplitter()
		#splitter.setStyleSheet('QSplitter{ background-image: url("'+ os.path.join(application_path, 'wall.png').replace('\\', '/') + '");}')
		members = QtWidgets.QFrame()
		members.setObjectName("frameMembers")
		# QWidget#frameMembers{ background-image: url("'+ os.path.join(application_path, 'wall.png').replace('\\', '/') + '");}
		members.setStyleSheet('QWidget#frameMembers{ background-image: url("'+ os.path.join(application_path, '4907157.jpg').replace('\\', '/') + '");}')
		scrollbar = QtWidgets.QScrollArea(widgetResizable=True)
		scrollbar.setFrameShape(QtWidgets.QFrame.NoFrame)
		scrollbar.setWidget(members)
		if meetingData != None:
			self.membersList = eval(meetingData[CT_PRES_POS])
		else:
			self.membersList = dict()
		self.membersLayout = QVBoxLayout()
		self.listMembers()
		members.setLayout(self.membersLayout)
		nameAndRoles = QtWidgets.QWidget()
		label = QtWidgets.QLabel()
		label.setText("Meeting name:")
		self.lineE = QtWidgets.QLineEdit()
		if meetingData != None and meetingData[CT_NAME_POS] != None:
			self.lineE.setText(meetingData[CT_NAME_POS])
		label2 = QtWidgets.QLabel()
		label2.setText("Duration:")
		self.lineE2 = QtWidgets.QLineEdit()
		if meetingData != None and meetingData[CT_DURATION_POS] != None:
			duration = str(meetingData[CT_DURATION_POS])
			if int(duration.split('.')[1]) == 0:
				# avoid decimal if it is 0
				duration = duration.split('.')[0]
			elif len(duration.split('.')[1]) == 1 :
				# add a final 0 if there's only one decimal
				duration += '0'
			self.lineE2.setText(duration)
		# add validator for duration line edit
		reg_ex = QtCore.QRegExp("^[0-9]+\.[0-5][0-9]$")
		input_validator = QtGui.QRegExpValidator(reg_ex, self.lineE2)
		self.lineE2.setValidator(input_validator)
		label3 = QtWidgets.QLabel()
		label3.setText("Date:")
		minDate = QtCore.QDateTime(1990, 1, 1, 10, 30)
		self.dateEdit = QtWidgets.QDateEdit()
		self.dateEdit.setMinimumDateTime(minDate)
		if meetingData != None and meetingData[CT_DATE_POS] != None:
			self.dateEdit.setDate(getQDateFromTimestamp(meetingData[CT_DATE_POS]))
		hboxDetails = QHBoxLayout()
		hboxDetails.addWidget(label)
		hboxDetails.addWidget(self.lineE)
		hboxDetails.addItem(verticalSpacer)
		hboxDetails.addWidget(label2)
		hboxDetails.addWidget(self.lineE2)
		hboxDetails.addWidget(label3)
		hboxDetails.addWidget(self.dateEdit)
		self.vboxAgenda = QVBoxLayout()
		self.vboxAgenda.addLayout(hboxDetails, 5)
		# roles
		self.rolesLayout = QVBoxLayout()
		for i in range(len(rolesName)):
			role = Role(rolesName[i][0], rolesName[i][1])
			role.dropDown.connect(self.updateCombo)
			role.selectionChanged.connect(self.selectionChanged)
			role.endSelection.connect(self.endSelection)
			if meetingData != None:
				# update comboBox with available data if any
				if meetingData[rolesName[i][2]] != None:
					combo = role.getComboBox()
					combo.addItem(meetingData[rolesName[i][2]])
					combo.setCurrentText(meetingData[rolesName[i][2]])
			self.rolesLayout.addWidget(role)
		# additional roles
		aRoles = internalDB.execute("SELECT * FROM ADDITIONALROLES")
		for aRole in aRoles:
			self.additionalRoles.append((aRole[AT_NAME_POS], aRole[AT_TYPE_POS]))
			role = Role(aRole[AT_NAME_POS], aRole[AT_TYPE_POS])
			role.dropDown.connect(self.updateCombo)
			role.selectionChanged.connect(self.selectionChanged)
			role.endSelection.connect(self.endSelection)
			if aRole[AT_MEMBER_POS] != None:
				# update comboBox with available data if any
				combo = role.getComboBox()
				combo.addItem(aRole[AT_MEMBER_POS])
				combo.setCurrentText(aRole[AT_MEMBER_POS])
			self.rolesLayout.addWidget(role)
		self.supportWidget = QtWidgets.QWidget()
		self.supportWidget.setObjectName("parentWidget")
		#supportWidget.setStyleSheet('QWidget#parentWidget{ background-image: url("%s"); background-repeat: no-repeat; background-position: center; background-color: rgba(255,255,255, 1); }' % os.path.join(application_path, 'smallLogo.jpg').replace('\\', '/'))
		self.supportWidget.setStyleSheet('QWidget#parentWidget{ background-color: rgba(255,255,255, 1); }')
		scroll = QtWidgets.QScrollArea(widgetResizable=True)
		scroll.setFrameShape(QtWidgets.QFrame.NoFrame)
		scroll.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		scroll.setWidget(self.supportWidget)
		self.supportWidget.setLayout(self.rolesLayout)

		self.vboxAgenda.addWidget(scroll, 80)

		self.groupNewRole = QtWidgets.QGroupBox()
		self.groupNewRole.setTitle("Add role")
		self.groupNewRole.setStyleSheet("QGroupBox { border: 1px solid gray; border-radius: 5px; margin-top: 15px;}  QGroupBox::title {color: DarkGreen; subcontrol-origin: margin; top: 7px; left: 20px}")
		lnrole = QLabel()
		lnrole.setText("Role Name:")
		self.lineEdit = QtWidgets.QLineEdit()
		ltype = QLabel()
		ltype.setText("Role Type:")
		self.cboxrole = QtWidgets.QComboBox()
		self.cboxrole.addItem("")
		for i in range(len(rolesType)):
			self.cboxrole.addItem(rolesType[i][0])
		btn = QtWidgets.QPushButton()
		btn.clicked.connect(self.addRole)
		btn.setText("Add")
		hboxgroup = QHBoxLayout()
		hboxgroup.addWidget(lnrole)
		hboxgroup.addWidget(self.lineEdit)
		hboxgroup.addItem(horizontalSpacer)
		hboxgroup.addWidget(ltype)
		hboxgroup.addWidget(self.cboxrole)
		hboxgroup.addItem(horizontalSpacer)
		hboxgroup.addWidget(btn)
		self.groupNewRole.setLayout(hboxgroup)
		self.vboxAgenda.addWidget(self.groupNewRole, 10)

		bsuggest = QtWidgets.QPushButton()
		bsuggest.clicked.connect(self.suggestRole)
		bsuggest.setText("Suggest remaining roles")
		bsuggest.setIcon(QtGui.QIcon(os.path.join(application_path, 'idea.png')))

		bsave = QtWidgets.QPushButton()
		bsave.clicked.connect(self.saveChanges)
		bsave.setText("Save changes")
		bsave.setIcon(QtGui.QIcon(os.path.join(application_path, 'diskette.png')))

		bclose = QtWidgets.QPushButton()
		bclose.clicked.connect(self.closeMeeting)
		bclose.setText("Close meeting")
		bclose.setIcon(QtGui.QIcon(os.path.join(application_path, 'shield.png')))

		btnbox = QHBoxLayout()
		btnbox.addWidget(bsuggest)
		btnbox.addItem(horizontalSpacer)
		btnbox.addWidget(bsave)
		btnbox.addItem(horizontalSpacer)
		btnbox.addWidget(bclose)
		self.vboxAgenda.addLayout(btnbox, 5)

		nameAndRoles.setLayout(self.vboxAgenda)

		splitter.addWidget(scrollbar)
		splitter.addWidget(nameAndRoles)
		splitter.setStretchFactor(1,4)

		hboxAgenda = QHBoxLayout()
		hboxAgenda.addWidget(splitter)
		self.agendaWidget.setLayout(hboxAgenda)

		if meetingData == None:
			# no current meeting in progress, show new button
			self.newWidget.setVisible(True)
			self.agendaWidget.setVisible(False)
		else:
			# a meeting is in progress, show the agenda
			self.newWidget.setVisible(False)
			self.agendaWidget.setVisible(True)
			self.supportWidget.setStyleSheet('QWidget#parentWidget{ background-image: url("%s"); background-repeat: no-repeat; background-position: center; background-color: rgba(255,255,255, 1); }' % os.path.join(application_path, 'smallLogo.jpg').replace('\\', '/'))

		mainVbox = QVBoxLayout()
		mainVbox.addWidget(self.newWidget)
		mainVbox.addWidget(self.agendaWidget)
		self.setLayout(mainVbox)


	def newMeeting(self):
		self.newWidget.setVisible(False)
		self.anim = QPropertyAnimation(self.agendaWidget, b"pos")
		self.anim.setEasingCurve(QEasingCurve.OutInCubic)
		self.anim.setStartValue(QPoint(self.newWidget.width(), self.newWidget.height()));
		self.anim.setEndValue(QPoint(self.newWidget.x(), self.newWidget.y()))
		self.anim.setDuration(1500)
		self.anim.start()
		# if I set agendaWidget as visible now, it appears at the center of the screen and the animation
		# is ruined. Delay visibility to give time the animation to start
		self.timer.singleShot(70, QtCore.Qt.PreciseTimer, self.showAgenda)

	def showAgenda(self):
		if getattr(sys, 'frozen', False):
			application_path = sys._MEIPASS
		elif __file__:
			application_path = os.path.dirname(__file__)
		self.supportWidget.setStyleSheet('QWidget#parentWidget{ background-image: url("%s"); background-repeat: no-repeat; background-position: center; background-color: rgba(255,255,255, 1); }' % os.path.join(application_path, 'smallLogo.jpg').replace('\\', '/'))
		self.agendaWidget.setVisible(True)

	def showNMbutton(self):
		self.newWidget.setVisible(True)
		self.agendaWidget.setVisible(False)

	def addRole(self):
		roleName = str(self.lineEdit.text())
		if roleName == "":
			# mandatory field - signal error and return
			self.lineEdit.setStyleSheet("background-color: " + redBackground[0] + ";")
			self.currentObject = self.lineEdit
			self.currentBackground = redBackground
			self.backgroundIndex = 1
			# start timer to change background color
			self.timer.singleShot(100, QtCore.Qt.CoarseTimer, self.changeBackground)
			return
		if self.cboxrole.currentText() == "":
			# mandatory field - signal error and return
			self.cboxrole.setStyleSheet("background-color: " + redBackground[0] + ";")
			self.currentObject = self.cboxrole
			self.currentBackground = redBackground
			self.backgroundIndex = 1
			# start timer to change background color
			self.timer.singleShot(100, QtCore.Qt.CoarseTimer, self.changeBackground)
			return
		# role name must be unique - check uniqueness
		data = internalDB.execute("SELECT * FROM ADDITIONALROLES WHERE name = \"%s\"" % roleName)
		res = data.fetchone()
		exit = False
		for rname, rtype in self.additionalRoles:
			if rname == roleName:
				exit = True
		for rname, rtype, x, y in rolesName:
			if rname == roleName:
				exit = True
		if exit == True or res != None:
			# name already exist - do not continue
			dlg = QMessageBox(self)
			dlg.setWindowTitle("Add role")
			dlg.setText("A role with the same name is already present")
			dlg.setStandardButtons(QMessageBox.Ok)
			dlg.setIcon(QMessageBox.Warning)
			dlg.exec()
			return
		type = -1
		for rname, rtype, x in rolesType:
			if rname == self.cboxrole.currentText():
				type = rtype
				break
		role = Role(roleName, type)
		role.dropDown.connect(self.updateCombo)
		role.selectionChanged.connect(self.selectionChanged)
		role.endSelection.connect(self.endSelection)
		self.rolesLayout.addWidget(role)
		# temporary save additional role (add it to db only when user press "Save chenges" button)
		self.additionalRoles.append((roleName, type))
		# change background to signal the successful operation
		self.groupNewRole.setStyleSheet("QGroupBox { border: 1px solid gray; border-radius: 5px; margin-top: 15px; background-color: " + greenBackground[0] + ";}  QGroupBox::title {color: DarkGreen; subcontrol-origin: margin; top: 7px; left: 20px}")
		self.currentObject = self.groupNewRole
		self.currentBackground = greenBackground
		self.backgroundIndex = 1
		# start timer to change background color
		self.timer.singleShot(100, QtCore.Qt.CoarseTimer, self.changeBackground)
		

	def updateCombo(self, combob, roleType):
		self.disableEdit = True
		# refresh the list of present members
		currentSelected = combob.currentText()
		combob.clear()
		people = []
		for m in self.membersList:
			if self.membersList[m] == 1:
				# get priority if any
				data = internalDB.execute("SELECT meetingWithoutRole FROM MEMBERS WHERE name = \"%s\"" % m)
				res = data.fetchone()
				priority = res[0]
				additional = ""
				if priority > 0:
					additional = " - ! (s)he attended the last %s meeting(s) without taking a role" % priority
				# get last time this member covered this role
				if roleType != 'custom':
					data = internalDB.execute("SELECT %s FROM MEMBERS WHERE name = \"%s\"" % (roleType, m))
					res = data.fetchone()
					try:
						lastTime = res[0]
					except:
						people.append(m + " - never" + additional)
						continue
					if lastTime == None:
						people.append(m + " - never" + additional)
						continue
					# get today date as UNIX timestamp
					today = datetime.datetime.timestamp(datetime.datetime.now())
					# calculate date difference (in days)
					days = int((today - lastTime)/(60*60*24))
					people.append(m + " - " + str(days) + " days ago" + additional)
				else:
					# custom role
					people.append(m + additional)
		combob.addItem("");
		combob.addItems(people)
		# keep previous selection if any
		for p in people:
			if currentSelected in p and currentSelected != "":
				combob.setCurrentText(p)
				break
		# otherwise hide suggested icon
		else:
			combob.hideIcon()

	def endSelection(self, combob):
		self.disableEdit = False
		self.selectionChanged(combob)

	def selectionChanged(self, combob):
		if self.disableEdit:
			return
		currentSelected = combob.currentText()
		if currentSelected != "":
			try:
				# do not display last time role was covered once the selection is done
				name = str(currentSelected.split('-')[0])
				# remove final space before '-' character if any
				if name[-1] == " ":
					name = name[:-1]
				combob.addItem(name);
				combob.setCurrentText(name)
			except Exception as e:
				pass

	def presenceChanged(self, cbox):
		if cbox.isChecked():
			self.membersList[cbox.text()] = 1
		else:
			self.membersList[cbox.text()] = 0
			# check if member was assigned to a role and remove him/her if this is the case
			for i in range(self.rolesLayout.count()):
				elem = self.rolesLayout.itemAt(i).widget()
				combo = elem.getComboBox()
				if combo.currentText() == cbox.text():
					combo.clear()
					elem.hideIcon(None)

	def listMembers(self):
		global internalDB
		# clear the members list - we want to redraw the list from scratch
		for i in reversed(range(self.membersLayout.count())):
			m = self.membersLayout.takeAt(i).widget()
			self.membersLayout.removeWidget(m)
			m.setParent(None)
			sip.delete(m)
		# draw the member list
		data = internalDB.execute("SELECT * FROM MEMBERS WHERE active = 1 ORDER BY name")
		for row in data:
			member = CustomCheckbox()
			member.setText(row[NAME_POS])
			member.setStyleSheet("QCheckBox{ font-size: 18px;} QCheckBox::indicator:checked{background-color : lightgreen;} QCheckBox::indicator{border: 1px solid blue; border-radius: 8px; background-color : red;}")
			member.checked.connect(self.presenceChanged)
			if row[NOTES_POS] != None and row [NOTES_POS] != '':
				member.setToolTip(row[NOTES_POS])
			self.membersLayout.addWidget(member)
			if row[NAME_POS] in self.membersList:
				# assert previously checked boxes
				if self.membersList[row[NAME_POS]] == 1:
					member.setChecked(True)
			else:
				# add member to the members list
				self.membersList.update({row[NAME_POS] : 0})


	def suggestRole(self):
		global internalDB
		# get the list of members attending this meeting
		attendees = dict() # dictionary with {memberName: [list of roles assigned]}
		for member in self.membersList:
			if self.membersList[member] == 1:
				attendees[member] = []
		if attendees == {}:
			# there are no members - nothing to do here
			return
		# get the list of members who don't have a role and the list of roles to be suggested
		withoutARole = list(attendees.keys())
		toBeSuggested = []
		typesList = []
		for i in range(self.rolesLayout.count()):
			elem = self.rolesLayout.itemAt(i).widget()
			roleType = elem.getRoleType()
			combo = elem.getComboBox()
			memberName = combo.currentText()
			if memberName != "":
				try:
					if roleType == 'lastSpeech':
						# if it is a speaker, do not suggest it for other roles
						attendees.pop(memberName)
					if memberName in withoutARole:
						# if member has more than a role, probably his name has already been removed
						withoutARole.remove(memberName)
					attendees[memberName].append(roleType)
				except:
					pass
			else:
				# no name for this role - save this widget
				if roleType != 'lastSpeech' and roleType != "custom":
					toBeSuggested.append(elem)
					typesList.append(elem.getRoleType())
		if toBeSuggested == []:
			# there are no roles who need suggestion - nothing to do here
			return

		# order toBeSuggested roles as to have "heavy" roles before and "easy" roles after
		# in this way we have more chance to couple together easier roles to the same person
		toBeSuggestedOrdered = []
		roleTypesPriority = {'lastTMOD': 0, 'lastTTM': 1, 'lastGenEval': 2, 'lastEval': 3, "lastTimer": 4, "lastGrammarian": 5, "lastAhCounter": 6, "lastHackMaster": 7, "lastHumorist": 8}
		for role in toBeSuggested:
			type = role.getRoleType()
			priority = 255
			try:
				priority = roleTypesPriority[type]
			except:
				pass
			toBeSuggestedOrdered.append((role, priority))
		# order list
		toBeSuggestedOrdered.sort(key=lambda x: x[1])
		# rewrite toBeSuggested
		toBeSuggested = []
		for role, p in toBeSuggestedOrdered:
			toBeSuggested.append(role)


		presenceWORolePriority = True
		# assign roles to the ones who haven't it yet
		while withoutARole != []:
			# get a member who has the highest priority according to the meetingWithoutRole and the last time he covered the role we are trying to assign
			#sql = "SELECT * FROM MEMBERS WHERE name IN (%s) ORDER BY meetingWithoutRole DESC, %s ASC LIMIT 1" % (','.join('?'*len(withoutARole)), role.getRoleType())
			if presenceWORolePriority:
				# get a member who has the highest priority according to the meetingWithoutRole
				sql = "SELECT * FROM MEMBERS WHERE name IN (%s) ORDER BY meetingWithoutRole DESC LIMIT 1" % (','.join('?'*len(withoutARole)))
				data = withoutARole
				data = internalDB.execute(sql, data)
				res = data.fetchone()
				if res == None:
					# error - this should not happen
					dlg = QMessageBox(self)
					dlg.setWindowTitle("Suggest remaining roles")
					dlg.setText("Internal error - roles cannot be suggested.")
					dlg.setStandardButtons(QMessageBox.Ok)
					dlg.setIcon(QMessageBox.Critical)
					dlg.exec()
					return
				if res[MEETINGWR_POS] == 0:
					# all members had a role in previous meeting - stop seeking members by this parameter
					presenceWORolePriority = False
					continue
				# create 2 lists, one with roles never done and the other one with roles already covered
				neverDoneIndexes = [i for i in range(len(res)) if res[i] == None and i >= 2 and i <= 11]
				alreadyDoneIndexes = [i for i in range(len(res)) if res[i] != None and i >= 2 and i <= 11]
				# get an ordered list of already done roles (ordered by last time roles were covered)
				alreadyDone = []
				while alreadyDoneIndexes != []:
					min = alreadyDoneIndexes[0]
					for date in alreadyDoneIndexes:
						if res[date] < res[min]:
							min = date
					# append its role type
					for name, type, index  in rolesType:
						if index == min:
							alreadyDone.append(type)
							alreadyDoneIndexes.remove(min)
							break
				# convert neverDoneIndexes to role types
				neverDone = [] 
				for i in range(len(rolesType)):
					if rolesType[i][2] in neverDoneIndexes:
						neverDone.append(rolesType[i][1])
				# try to assign never done roles according to rolesPriority list
				exit = False
				for r in rolesPriority:
					if exit == True:
						break
					if r in neverDone and r in typesList:
						# match found - assign the role
						for i in range(len(toBeSuggested)):
							if exit == True:
								break
							if toBeSuggested[i].getRoleType() == r:
								role = toBeSuggested.pop(i) # remove from the list
								typesList.remove(r)
								member = res[NAME_POS]
								combob = role.getComboBox()
								combob.addItem(member)
								combob.setCurrentText(member)
								role.setSuggested("This member attended the last %s meeting(s) without taking a role" % str(res[MEETINGWR_POS]))
								# add the new assigned role to the member and remove member from the list of ones without a role
								try:
									attendees[member].append(role.getRoleType())
									withoutARole.remove(member)
								except:
									pass
								# exit if there are no more roles to be suggested
								if toBeSuggested == []:
									return
								# a role has been assigned for this member - quit this block of code
								exit = True
				if exit == True:
					# a role has been already assigned to this person, go on with another one
					continue
				# already done list is ordered - try to assign its first elements before
				for r in alreadyDone:
					if exit == True:
						break
					if r in typesList:
						# match found - assign the role
						for i in range(len(toBeSuggested)):
							if exit == True:
								break
							if toBeSuggested[i].getRoleType() == r:
								role = toBeSuggested.pop(i) # remove from the list
								typesList.remove(r)
								member = res[NAME_POS]
								combob = role.getComboBox()
								combob.addItem(member)
								combob.setCurrentText(member)
								role.setSuggested("This member attended the last %s meeting(s) without taking a role" % str(res[MEETINGWR_POS]))
								# add the new assigned role to the member and remove member from the list of ones without a role
								try:
									attendees[member].append(role.getRoleType())
									withoutARole.remove(member)
								except:
									pass
								# exit if there are no more roles to be suggested
								if toBeSuggested == []:
									return
								# a role has been assigned for this member - quit this block of code
								exit = True
			# presence without a role priority has ended - pick the member considering the last time he covered a role
			else:
				role = toBeSuggested.pop(0) # remove from the list
				sql = "SELECT * FROM MEMBERS WHERE name IN (%s) ORDER BY %s ASC LIMIT 1" % (','.join('?'*len(withoutARole)), role.getRoleType())
				data = withoutARole
				data = internalDB.execute(sql, data)
				res = data.fetchone()
				if res == None:
					# error - this should not happen
					dlg = QMessageBox(self)
					dlg.setWindowTitle("Suggest remaining roles")
					dlg.setText("Internal error - roles cannot be suggested.")
					dlg.setStandardButtons(QMessageBox.Ok)
					dlg.setIcon(QMessageBox.Critical)
					dlg.exec()
					return
				member = res[NAME_POS]
				combob = role.getComboBox()
				combob.addItem(member)
				combob.setCurrentText(member)
				today = int(time.time())
				lastTime = int(time.time())
				never = False
				for name, type, index in rolesType:
					if type == role.getRoleType():
						if res[index] == None:
							never = True
						else:
							lastTime = int(res[index])
				endWith = "last time he did this was %d days ago" % int((float(today)-float(lastTime))/(60*60*24))
				if never == True:
					endWith = "he/she never took this role"
				role.setSuggested("This member was not covering any role and " + endWith)
				# add the new assigned role to the member and remove member from the list of ones without a role
				try:
					attendees[member].append(role.getRoleType())
					withoutARole.remove(member)
				except:
					pass
				# exit if there are no more roles to be suggested
				if toBeSuggested == []:
					return

		# at this point all attendees already have a role
		# try to suggest the ones with less workload for the lightweight roles
		while toBeSuggested != []:
			# list the roles that cannot be done together
			mutuallyExclusiveRoles = ['lastEval', 'lastGenEval', 'lastTTM', 'lastTMOD']
			# pick a role to be suggested
			role = toBeSuggested.pop(0)
			roleType = role.getRoleType()
			# the person with less roles can take this one, whatever it is
			member = ['', 100]
			for m in attendees.keys():
				# compare the list of currently assigned roles for each member - select the one with less roles
				if len(attendees[m]) < member[1]:
					skip = False
					if roleType in mutuallyExclusiveRoles:
						# check if this person needs to be skipped because it already covers one of the hot roles
						for r in attendees[m]:
							if r in mutuallyExclusiveRoles:
								skip = True
					if not skip:
						member = [m, len(attendees[m])]
				elif len(attendees[m]) == member[1]:
					# if they have the same workload assign the role to the one who has none of the mutuallyExclusiveRoles
					try:
						oldHasIt = False
						for r in attendees[member[0]]:
							if r in mutuallyExclusiveRoles:
								oldHasIt = True
						newHasIt = False
						for r in attendees[m]:
							if r in mutuallyExclusiveRoles:
								newHasIt = True
						if oldHasIt == True and newHasIt == False:
							# assign the role only in this case, otherwise do nothing
							member = [m, len(attendees[m])]
					except:
						pass
			if member[0] == '':
				# it can happen if the member list is very short
				continue
			# here we should have our hero
			combob = role.getComboBox()
			combob.addItem(member[0])
			combob.setCurrentText(member[0])
			role.setSuggested("Someone needs to take more than a role and this role can be done with the other(s)")
			# add role to this member's list
			attendees[member[0]].append(roleType)

	
	def saveChanges(self):
		# update CURRENTMEETING table
		internalDB.execute("DELETE FROM CURRENTMEETING")
		# build insert query based on the number of available entries
		queryStringFields = 'INSERT INTO CURRENTMEETING ('
		queryStringValues = ') values('
		values = []
		if self.lineE.text() != "":
			queryStringFields += 'name, '
			queryStringValues += '?, '
			values.append(self.lineE.text())
		if self.lineE2.text() != "":
			queryStringFields += 'duration, '
			queryStringValues += '?, '
			values.append(float(self.lineE2.text()))
		date = self.dateEdit.dateTime().toPyDateTime()
		if str(date).split(" ")[0] != '2000-01-01':
			queryStringFields += 'date, '
			queryStringValues += '?, '
			tstamp = getTimestampFromQDate(date)
			values.append(int(tstamp))
		for i in range(self.rolesLayout.count()):
			if i >= len(rolesName):
				# additional roles - stop here
				break
			elem = self.rolesLayout.itemAt(i).widget()
			combo = elem.getComboBox()
			if combo.currentText() != '':
				queryStringFields += rolesName[i][3] + ', '
				queryStringValues += '?, '
				values.append(combo.currentText())
		queryStringFields += 'Presence'
		queryStringValues += '?'
		values.append(str(self.membersList))
		queryStringValues += ')'

		# insert data in CURRENTMEETING	table
		sql = queryStringFields + queryStringValues
		data = tuple(values)
		try:
			internalDB.execute(sql, data)
		except Exception as e:
			dlg = QMessageBox(self)
			dlg.setWindowTitle("Save changes")
			dlg.setText("Critical error. Data cannot be saved.")
			dlg.setStandardButtons(QMessageBox.Ok)
			dlg.setIcon(QMessageBox.Critical)
			dlg.exec()
			return

		# update ADDITIONALROLES table
		internalDB.execute("DELETE FROM ADDITIONALROLES")
		for roleName, type in self.additionalRoles:
			queryStringFields = 'INSERT INTO ADDITIONALROLES (name, type'
			queryStringValues = ') values(?, ?'
			values = [roleName, type]
			for i in range(self.rolesLayout.count()):
				elem = self.rolesLayout.itemAt(i).widget()
				if elem.getRoleName() == roleName:
					combo = elem.getComboBox()
					if combo.currentText() != '':
						queryStringFields += ', member'
						queryStringValues += ', ?'
						values.append(combo.currentText())
			queryStringValues += ')'
			sql = queryStringFields + queryStringValues
			data = tuple(values)
			internalDB.execute(sql, data)
		# clear suggested icons
		for i in range(self.rolesLayout.count()):
			elem = self.rolesLayout.itemAt(i).widget()
			elem.hideIcon(None)

		# commit changes to db only at the end
		internalDB.commit()
		dlg = QMessageBox(self)
		dlg.setWindowTitle("Save changes")
		dlg.setText("Data correctly updated.")
		dlg.setStandardButtons(QMessageBox.Ok)
		dlg.setIcon(QMessageBox.Information)
		dlg.exec()

	def closeMeeting(self):
		eName = self.lineE.text()
		eDuration = self.lineE2.text()
		if eName == '' or eDuration == '':
			# do not continue without name and duration
			dlg = QMessageBox(self)
			dlg.setWindowTitle("Close meeting")
			dlg.setText("Meeting name, duration and date must be specified before closing the meeting")
			dlg.setStandardButtons(QMessageBox.Ok)
			dlg.setIcon(QMessageBox.Critical)
			dlg.exec()
			return
		eDuration = float(eDuration)
		dlg = QMessageBox(self)
		dlg.setWindowTitle("Close meeting")
		dlg.setText("After a meeting is closed its data cannot be changed. Do you want to proceed?")
		dlg.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)
		dlg.setDefaultButton(QMessageBox.Cancel)
		dlg.setIcon(QMessageBox.Warning)
		choice = dlg.exec()
		if choice == QMessageBox.Cancel:
			return
		# update participations
		membersWithNoRoles = []
		for member in self.membersList:
			if self.membersList[member] == 1:
				# save all participants in this temporary list
				membersWithNoRoles.append(member)
				# this member attended the meeting - update its participations table
				# get member ID
				try:
					data = internalDB.execute("SELECT id FROM MEMBERS WHERE name = '%s'" % member)
					res = data.fetchone()
					if res == None:
						continue
					mID = res[0]
					# save data into mID table
					sql = 'INSERT INTO m%s (eventName, duration) values(?, ?)' % mID
					data = (eName, eDuration)
					internalDB.execute(sql, data)
				except:
					pass
		# update last roles
		for i in range(self.rolesLayout.count()):
			elem = self.rolesLayout.itemAt(i).widget()
			combo = elem.getComboBox()
			member = combo.currentText()
			if member != '':
				try:
					# this member had a role, remove him/her from the temporary list
					membersWithNoRoles.remove(member)
				except Exception as e:
					pass
				# get role type
				rtype = elem.getRoleType()
				if rtype != 'custom':
					# update last role
					# get meeting date
					tstamp = getTimestampFromQDate(self.dateEdit.dateTime().toPyDateTime())
					# update lastDate only if current meeting date is greather than the saved one (it could happen since there is no check on meeting date)
					data = internalDB.execute("SELECT %s FROM MEMBERS WHERE name = '%s'" % (rtype, member))
					res = data.fetchone()
					if res[0] != None:
						if res[0] > tstamp:
							# do not update the record
							continue
					sql = 'UPDATE MEMBERS SET %s = ? WHERE name = ?' % rtype
					data = (int(tstamp), member)
					internalDB.execute(sql, data)
				# if role is speaker, add 1 hour and half of participation
				if rtype == 'lastSpeech':
					try:
						data = internalDB.execute("SELECT id FROM MEMBERS WHERE name = '%s'" % member)
						res = data.fetchone()
						if res == None:
							continue
						mID = res[0]
						sql = 'INSERT INTO m%s (eventName, duration) values(?, ?)' % mID
						data = ("Speech preparation " + eName, 1.3)
						internalDB.execute(sql, data)
					except:
						pass
		# update meetingWithoutRole
		for member in self.membersList:
			if member in membersWithNoRoles:
				# increase priority level of members who attended without taking a role
				internalDB.execute("UPDATE MEMBERS SET meetingWithoutRole = meetingWithoutRole + 1 WHERE name = '%s'" % member)
			else:
				internalDB.execute("UPDATE MEMBERS SET meetingWithoutRole = 0 WHERE name = '%s'" % member)

		# data updated - delete temporary tables
		internalDB.execute("DELETE FROM CURRENTMEETING")
		internalDB.execute("DELETE FROM ADDITIONALROLES")
		self.membersList = {}
		self.additionalRoles = []
		for i in reversed(range(self.rolesLayout.count())):
			if i >= len(rolesName):
				# additional role - remove it from GUI
				m = self.rolesLayout.takeAt(i).widget()
				self.rolesLayout.removeWidget(m)
				m.setParent(None)
				sip.delete(m)
			else:
				# standard role - clear comboBox
				m = self.rolesLayout.itemAt(i).widget()
				combo = m.getComboBox()
				combo.setCurrentText("")
		# clear presence checkboxes
		for i in range(self.membersLayout.count()):
			elem = self.membersLayout.itemAt(i).widget()
			elem.setChecked(False)
		# clear meeting name and duration
		self.lineE.setText("")
		self.lineE2.setText("")
		# clear suggested icons
		for i in range(self.rolesLayout.count()):
			elem = self.rolesLayout.itemAt(i).widget()
			elem.hideIcon(None)
		# hide meeting panel and show "new meeting" button by using an animation
		self.anim = QPropertyAnimation(self.agendaWidget, b"pos")
		self.anim.setEasingCurve(QEasingCurve.OutInCubic)
		self.anim.setEndValue(QPoint(self.agendaWidget.width(), self.agendaWidget.height()))
		self.anim.setDuration(1500)
		self.anim.finished.connect(self.showNMbutton)
		self.anim.start()
		# update changes in db
		internalDB.commit()
		# signal data changed
		self.updateMembersData.emit()

	def changeBackground(self):
		if self.backgroundIndex == len(self.currentBackground):
			# restore default color and stop timer
			self.currentObject.setStyleSheet("")
			self.backgroundIndex = 0
			# clear text for groupNewRole only
			if self.currentObject == self.groupNewRole:
				self.groupNewRole.setStyleSheet("QGroupBox { border: 1px solid gray; border-radius: 5px; margin-top: 15px;}  QGroupBox::title {color: DarkGreen; subcontrol-origin: margin; top: 7px; left: 20px}")
				self.lineEdit.setText("")
				self.cboxrole.setCurrentText("")
			return
		if self.currentObject == self.groupNewRole:
			self.currentObject.setStyleSheet("QGroupBox { border: 1px solid gray; border-radius: 5px; margin-top: 15px; background-color: " + self.currentBackground[self.backgroundIndex] + ";}  QGroupBox::title {color: DarkGreen; subcontrol-origin: margin; top: 7px; left: 20px}")
		else:
			self.currentObject.setStyleSheet("background-color: " + self.currentBackground[self.backgroundIndex] + ";")
		self.backgroundIndex = self.backgroundIndex + 1
		nextTimer = 100
		if self.backgroundIndex >= (len(self.currentBackground) / 2): # speed up at the end
			nextTimer = 20
		self.timer.singleShot(nextTimer, QtCore.Qt.CoarseTimer, self.changeBackground)

################### Second tab #####################
############### Members management #################

class ParticipationsWindow(QtWidgets.QMainWindow):
	def __init__(self, memberID):
		global internalDB
		super(ParticipationsWindow, self).__init__()

		if getattr(sys, 'frozen', False):
			application_path = sys._MEIPASS
		elif __file__:
			application_path = os.path.dirname(__file__)

		# get member's name and set it as window's title
		data = internalDB.execute("SELECT name FROM MEMBERS WHERE id = " + str(memberID))
		res = data.fetchone()
		self.setWindowTitle(res[0])
		self.setWindowIcon(QtGui.QIcon(os.path.join(application_path, 'tmfavicon.ico')))


		label = QtWidgets.QLabel()
		label.setText("%s participation hours:" % res[0])
		label2 = QtWidgets.QLabel()
		verticalSpacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
		label3 = QtWidgets.QLabel()
		label3.setText("Participations detail")
		textEdit = QtWidgets.QTextEdit()
		textEdit.setReadOnly(True)
		hbox = QHBoxLayout()
		hbox.addWidget(label)
		hbox.addWidget(label2)
		vbox = QVBoxLayout()
		vbox.addLayout(hbox)
		vbox.addItem(verticalSpacer)
		vbox.addWidget(label3)
		vbox.addWidget(textEdit)
		mainWidget = QtWidgets.QWidget()
		mainWidget.setLayout(vbox)
		self.setCentralWidget(mainWidget)
		self.resize(mainWidget.width() + 100, mainWidget.height() + 100)

		# get member's participations
		data = internalDB.execute("SELECT * FROM m%s" % str(memberID))
		hoursNo = datetime.timedelta(hours = 0, minutes = 0, seconds = 0)
		text = ''
		for row in data:
			text += "Event: " + str(row[0]) + "\t\t- Duration: " + str(row[1]) + "\n"
			# sum hours
			durationHours = str(row[1]).split('.')[0]
			durationMinutes = str(row[1]).split('.')[1]
			if len(durationMinutes) == 1:
				# 1.30 minutes are saved as 1.3 - 3 must be modified to be 30 again in order to correctly calculate time
				durationMinutes += '0'
			hoursNo = datetime.timedelta(hours=int(hoursNo.total_seconds() // 3600), minutes=int((hoursNo.total_seconds() % 3600) // 60)) + datetime.timedelta(hours=int(durationHours), minutes=int(durationMinutes))

		# update data
		hoursStr = '{}:{}'.format(int(hoursNo.total_seconds() // 3600), int((hoursNo.total_seconds() % 3600) // 60))
		label2.setText(str(hoursStr))
		textEdit.setText(text)

		QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+Q"), self).activated.connect(self.close)
		QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+W"), self).activated.connect(self.close)


class MentorWindow(QtWidgets.QMainWindow):
	updated = QtCore.pyqtSignal(str)

	def __init__(self, memberID):
		global internalDB
		super(MentorWindow, self).__init__()

		if getattr(sys, 'frozen', False):
			application_path = sys._MEIPASS
		elif __file__:
			application_path = os.path.dirname(__file__)

		self.timer = QtCore.QTimer()
		self.timer.setSingleShot(True)
		self.id = memberID

		# get member's name and set it as window's title
		data = internalDB.execute("SELECT * FROM MEMBERS WHERE id = " + str(memberID))
		mentee = data.fetchone()
		self.setWindowTitle(mentee[NAME_POS])
		self.setWindowIcon(QtGui.QIcon(os.path.join(application_path, 'tmfavicon.ico')))

		# get members list
		data = internalDB.execute("SELECT * FROM MEMBERS WHERE active = 1 ORDER BY name")
		membersList = []
		for row in data:
			# skip current member
			if mentee[ID_POS] == row[ID_POS]:
				continue
			membersList.append(row[NAME_POS])

		label = QLabel()
		label.setText("Current mentor:")
		label2 = QLabel()
		if mentee[MENTOR_POS] != None:
			label2.setText(mentee[MENTOR_POS])
		else:
			label2.setText("None")
		self.cb = QtWidgets.QCheckBox()
		self.cb.setText("Need mentor")
		if mentee[NEEDMENTOR_POS] == 1:
			self.cb.setChecked(True)
		hbox = QHBoxLayout()
		hbox.addWidget(label)
		hbox.addWidget(label2)
		hbox.addStretch()
		hbox.addWidget(self.cb)
		label3 = QLabel()
		label3.setText("Assign mentor")
		self.combo = QtWidgets.QComboBox()
		self.combo.addItem("")
		self.combo.addItem("EXTERNAL")
		self.combo.addItems(membersList)
		self.combo.currentTextChanged.connect(self.showEdit)
		self.label4 = QLabel()
		self.label4.setText("Mentor name:")
		self.label4.setVisible(False)
		self.lineEdit = QtWidgets.QLineEdit()
		self.lineEdit.setVisible(False)
		hbox2 = QHBoxLayout()
		hbox2.addWidget(self.combo)
		hbox2.addStretch()
		hbox2.addWidget(self.label4)
		hbox2.addWidget(self.lineEdit)
		hbox2.addStretch()
		okbtn = QtWidgets.QPushButton()
		okbtn.setText("Save changes")
		okbtn.setIcon(QtGui.QIcon(os.path.join(application_path, 'diskette.png')))
		okbtn.clicked.connect(self.save)
		hbox3 = QHBoxLayout()
		hbox3.addStretch()
		hbox3.addWidget(okbtn)
		vbox = QVBoxLayout()
		vbox.addLayout(hbox)
		vbox.addStretch()
		vbox.addWidget(label3)
		vbox.addLayout(hbox2)
		vbox.addStretch()
		vbox.addLayout(hbox3)

		mainWidget = QtWidgets.QWidget()
		mainWidget.setLayout(vbox)
		self.setCentralWidget(mainWidget)
		self.resize(mainWidget.minimumSizeHint().width() + 50, mainWidget.minimumSizeHint().height() + 50)

		QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+Q"), self).activated.connect(self.close)
		QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+W"), self).activated.connect(self.close)

	def save(self):
		global internalDB
		if self.combo.currentText() == 'EXTERNAL' and self.lineEdit.text() == '':
			self.lineEdit.setStyleSheet("background-color: " + redBackground[0] + ";")
			self.currentObject = self.lineEdit
			self.currentBackground = redBackground
			self.backgroundIndex = 1
			# start timer to change background color
			self.timer.singleShot(100, QtCore.Qt.CoarseTimer, self.changeBackground)
			return
		mentor = self.combo.currentText()
		needMentor = 0
		if self.cb.isChecked():
			needMentor = 1
		if mentor == '':
			mentor = None
		elif mentor == "EXTERNAL":
			mentor = self.lineEdit.text()
			needMentor = 0
		else:
			needMentor = 0
		sql = "UPDATE MEMBERS SET mentor = ?, needMentor = ? WHERE id = ?"
		data = (mentor, needMentor, self.id)
		internalDB.execute(sql, data)
		internalDB.commit()
		dlg = QMessageBox(self)
		dlg.setWindowTitle("Save changes")
		dlg.setText("Data correctly updated.")
		dlg.setStandardButtons(QMessageBox.Ok)
		dlg.setIcon(QMessageBox.Information)
		dlg.exec()
		self.updated.emit(mentor)
		self.close()
		

	def showEdit(self, event):
		if self.combo.currentText() == 'EXTERNAL':
			self.label4.setVisible(True)
			self.lineEdit.setVisible(True)
		else:
			self.label4.setVisible(False)
			self.lineEdit.setVisible(False)

	def changeBackground(self):
		if self.backgroundIndex == len(self.currentBackground):
			# restore default color and stop timer
			self.currentObject.setStyleSheet("background-color: #FFFFFF;")
			self.backgroundIndex = 0
			return
		self.currentObject.setStyleSheet("background-color: " + self.currentBackground[self.backgroundIndex] + ";")
		self.backgroundIndex = self.backgroundIndex + 1
		nextTimer = 100
		if self.backgroundIndex >= (len(self.currentBackground) / 2): # speed up at the end
			nextTimer = 20
		self.timer.singleShot(nextTimer, QtCore.Qt.CoarseTimer, self.changeBackground)


class MentorWidgetItem(QtWidgets.QWidget):
	id = -1
	dialogs = list()

	def __init__(self, memberID):
		super(MentorWidgetItem, self).__init__()
		self.id = memberID

		self.label = QLabel()
		data = internalDB.execute("SELECT * FROM MEMBERS WHERE id = " + str(memberID))
		member = data.fetchone()
		if member[MENTOR_POS] != None:
			self.label.setText(member[MENTOR_POS])
		toolbtn = QtWidgets.QToolButton()
		toolbtn.clicked.connect(self.editMentor)
		toolbtn.setText("...")
		hbox = QHBoxLayout()
		hbox.addWidget(self.label)
		hbox.addStretch()
		hbox.addWidget(toolbtn)
		self.setLayout(hbox)

	def editMentor(self):
		spawnedWindow = MentorWindow(self.id)
		spawnedWindow.updated.connect(self.updateLabel)
		self.dialogs.append(spawnedWindow)
		spawnedWindow.show()

	def updateLabel(self, mentor):
		if mentor == None:
			mentor = ''
		self.label.setText(mentor)

class DateWidgetItem(QtWidgets.QWidget):
	id = -1
	dbIndex = -1
	initDate = None
	currentBackground = redBackground
	backgroundIndex = 0
	timer = QtCore.QTimer()

	def __init__(self, memberID, index, date):
		super(DateWidgetItem, self).__init__()
		self.id = memberID
		self.dbIndex = index
		self.initDate = date

		self.dateEdit = QtWidgets.QLineEdit()
		self.dateEdit.setText(self.initDate)
		self.dateEdit.setEnabled(False)
		self.dateEdit.setStyleSheet(" border: none; background-color: rgba(255,255,255, 0);")
		# add validator for date line edit
		reg_ex = QtCore.QRegExp("^(0?[1-9]|[12][0-9]|3[01])[\/](0?[1-9]|1[012])[\/]\d{4}$")
		input_validator = QtGui.QRegExpValidator(reg_ex, self.dateEdit)
		self.dateEdit.setValidator(input_validator)
		self.timer.setSingleShot(True)

		self.toolbtn = QtWidgets.QToolButton()
		self.toolbtn.clicked.connect(self.editDate)
		self.toolbtn.setText("...")
		hbox = QHBoxLayout()
		hbox.addWidget(self.dateEdit)
		hbox.addStretch()
		hbox.addWidget(self.toolbtn)
		self.setLayout(hbox)

	def editDate(self):
		if getattr(sys, 'frozen', False):
			application_path = sys._MEIPASS
		elif __file__:
			application_path = os.path.dirname(__file__)

		if self.dateEdit.isEnabled() == False:
			# allow editing
			self.dateEdit.setEnabled(True)
			self.toolbtn.setText("")
			self.toolbtn.setIcon(QtGui.QIcon(os.path.join(application_path, 'check.png')))
		else:
			# save data
			self.dateEdit.setEnabled(False)
			self.toolbtn.setText("...")
			self.toolbtn.setIcon(QtGui.QIcon())
			try:
				dbColumn = ''
				for rname, rtype, index in rolesType:
					if index == self.dbIndex:
						dbColumn = rtype
						break
				if dbColumn == '':
					# this should not happen
					raise Exception("db column not found")
				newDate = self.dateEdit.text()
				if newDate == '':
					internalDB.execute("UPDATE MEMBERS SET %s = ? WHERE id = ?" % dbColumn, (None, str(self.id)))
					self.initDate = ''
					internalDB.commit()
					return
				parsedDate = datetime.datetime.strptime(newDate, '%d/%m/%Y')
				tstamp = getTimestampFromQDate(parsedDate)
				internalDB.execute("UPDATE MEMBERS SET %s = ? WHERE id = ?" % dbColumn, (tstamp, str(self.id)))
				self.initDate = newDate
				internalDB.commit()
			except Exception as e:
				# if an error occurs, restore the last valid date
				# start timer to change background color
				self.timer.singleShot(100, QtCore.Qt.CoarseTimer, self.signalError)

	def signalError(self):
		if self.backgroundIndex == len(self.currentBackground):
			# restore default color and stop timer
			self.dateEdit.setStyleSheet("border: none; background-color: rgba(255,255,255, 0);")
			self.backgroundIndex = 0
			# restore last valid date
			self.dateEdit.setText(self.initDate)
			return
		self.dateEdit.setStyleSheet("background-color: " + self.currentBackground[self.backgroundIndex] + ";")
		self.backgroundIndex = self.backgroundIndex + 1
		nextTimer = 100
		if self.backgroundIndex >= (len(self.currentBackground) / 2): # speed up at the end
			nextTimer = 20
		self.timer.singleShot(nextTimer, QtCore.Qt.CoarseTimer, self.signalError)

# Shows member information in Members management tab
class MemberDetail(QtWidgets.QWidget):
	id = -1
	backgroundIndex = 0
	currentObject = None
	currentBackground = []
	timer = QtCore.QTimer()
	dialogs = list()
	suicide = QtCore.pyqtSignal(int)

	def __init__(self, memberID):
		global internalDB
		super(MemberDetail, self).__init__()
		self.id = memberID

		if getattr(sys, 'frozen', False):
			application_path = sys._MEIPASS
		elif __file__:
			application_path = os.path.dirname(__file__)


		# query member information from db
		data = internalDB.execute("SELECT * FROM MEMBERS WHERE id = " + str(memberID))
		res = data.fetchone()

		self.table = QTableWidget()
		self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers) # disable cell editing
		self.table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection) # disable cell selection
		self.table.setFocusPolicy(Qt.NoFocus) # disable cell focus
		self.table.setColumnCount(11)
		self.table.setRowCount(2)
		self.table.setItem(0, 0, QTableWidgetItem("Last Speech"))
		self.table.setItem(0, 1, QTableWidgetItem("Last TMOD"))
		self.table.setItem(0, 2, QTableWidgetItem("Last GenEval"))
		self.table.setItem(0, 3, QTableWidgetItem("Last Eval"))
		self.table.setItem(0, 4, QTableWidgetItem("Last Timer"))
		self.table.setItem(0, 5, QTableWidgetItem("Last Grammarian"))
		self.table.setItem(0, 6, QTableWidgetItem("Last Ah Counter"))
		self.table.setItem(0, 7, QTableWidgetItem("Last Humorist"))
		self.table.setItem(0, 8, QTableWidgetItem("Last TTM"))
		self.table.setItem(0, 9, QTableWidgetItem("Last Hack Master"))
		self.table.setItem(0, 10, QTableWidgetItem("Mentor"))

		date = ''
		if res[LASTSPEECH_POS] != None:
			date = getQDateFromTimestamp(res[LASTSPEECH_POS]).toString('dd/MM/yyyy')
		#self.table.setItem(1, 0, QTableWidgetItem(date))
		self.table.setCellWidget(1, 0, DateWidgetItem(self.id, LASTSPEECH_POS, date))

		date = ''
		if res[LASTTMOD_POS] != None:
			date = getQDateFromTimestamp(res[LASTTMOD_POS]).toString('dd/MM/yyyy')
		#self.table.setItem(1, 1, QTableWidgetItem(date))
		self.table.setCellWidget(1, 1, DateWidgetItem(self.id, LASTTMOD_POS, date))

		date = ''
		if res[LASTGENEVAL_POS] != None:
			date = getQDateFromTimestamp(res[LASTGENEVAL_POS]).toString('dd/MM/yyyy')
		#self.table.setItem(1, 2, QTableWidgetItem(date))
		self.table.setCellWidget(1, 2, DateWidgetItem(self.id, LASTGENEVAL_POS, date))

		date = ''
		if res[LASTEVAL_POS] != None:
			date = getQDateFromTimestamp(res[LASTEVAL_POS]).toString('dd/MM/yyyy')
		#self.table.setItem(1, 3, QTableWidgetItem(date))
		self.table.setCellWidget(1, 3, DateWidgetItem(self.id, LASTEVAL_POS, date))

		date = ''
		if res[LASTTIMER_POS] != None:
			date = getQDateFromTimestamp(res[LASTTIMER_POS]).toString('dd/MM/yyyy')
		#self.table.setItem(1, 4, QTableWidgetItem(date))
		self.table.setCellWidget(1, 4, DateWidgetItem(self.id, LASTTIMER_POS, date))

		date = ''
		if res[LASTGRAMM_POS] != None:
			date = getQDateFromTimestamp(res[LASTGRAMM_POS]).toString('dd/MM/yyyy')
		#self.table.setItem(1, 5, QTableWidgetItem(date))
		self.table.setCellWidget(1, 5, DateWidgetItem(self.id, LASTGRAMM_POS, date))

		date = ''
		if res[LASTAHCOUNT_POS] != None:
			date = getQDateFromTimestamp(res[LASTAHCOUNT_POS]).toString('dd/MM/yyyy')
		#self.table.setItem(1, 6, QTableWidgetItem(date))
		self.table.setCellWidget(1, 6, DateWidgetItem(self.id, LASTAHCOUNT_POS, date))

		date = ''
		if res[LASTHUM_POS] != None:
			date = getQDateFromTimestamp(res[LASTHUM_POS]).toString('dd/MM/yyyy')
		#self.table.setItem(1, 7, QTableWidgetItem(date))
		self.table.setCellWidget(1, 7, DateWidgetItem(self.id, LASTHUM_POS, date))

		date = ''
		if res[LASTTTM_POS] != None:
			date = getQDateFromTimestamp(res[LASTTTM_POS]).toString('dd/MM/yyyy')
		#self.table.setItem(1, 8, QTableWidgetItem(date))
		self.table.setCellWidget(1, 8, DateWidgetItem(self.id, LASTTTM_POS, date))

		date = ''
		if res[LASTHACKM_POS] != None:
			date = getQDateFromTimestamp(res[LASTHACKM_POS]).toString('dd/MM/yyyy')
		#self.table.setItem(1, 9, QTableWidgetItem(date))
		self.table.setCellWidget(1, 9, DateWidgetItem(self.id, LASTHACKM_POS, date))

		mentor = MentorWidgetItem(self.id)
		self.table.setCellWidget(1, 10, mentor)

		#Table will fit the screen horizontally
		self.table.horizontalHeader().setStretchLastSection(True)
		self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		self.table.horizontalHeader().setVisible(False)
		self.table.verticalHeader().setVisible(False)
		self.table.setMaximumHeight(self.table.minimumSizeHint().height())
		self.table.setRowHeight(1, mentor.minimumSizeHint().height())

		label = QtWidgets.QLabel()
		label.setText("Notes")
		self.textEdit = QtWidgets.QTextEdit()
		self.textEdit.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
		notes = ""
		if res[NOTES_POS] != None:
			notes = str(res[NOTES_POS])
		self.textEdit.setText(notes)
		buttonEdit = QtWidgets.QPushButton()
		buttonEdit.clicked.connect(self.updateNotes)
		buttonEdit.setText("Update Notes")
		buttonEdit.setIcon(QtGui.QIcon(os.path.join(application_path, 'pencil.png')))
		notebox = QHBoxLayout()
		notebox.addWidget(self.textEdit)
		notebox.addWidget(buttonEdit)
		self.timer.setSingleShot(True)


		# groupbox participation
		groupPart = QtWidgets.QGroupBox()
		groupPart.setTitle("Add participation")
		groupPart.setStyleSheet("QGroupBox { border: 1px solid gray; border-radius: 5px; margin-top: 15px; }  QGroupBox::title {subcontrol-origin: margin; top: 7px; left: 20px}")
		label2 = QtWidgets.QLabel()
		label2.setText("Event name")
		self.textEdit2 = QtWidgets.QLineEdit()
		self.textEdit2.setPlaceholderText("Special meeting")
		label3 = QtWidgets.QLabel()
		label3.setText("Event duration (hours)")
		self.textEdit3 = QtWidgets.QLineEdit()
		self.textEdit3.setPlaceholderText("1.30")
		# add validator for hours text edit
		reg_ex = QtCore.QRegExp("^[0-9]+\.[0-5][0-9]$")
		input_validator = QtGui.QRegExpValidator(reg_ex, self.textEdit3)
		self.textEdit3.setValidator(input_validator)
		button = QtWidgets.QPushButton()
		button.clicked.connect(self.addParticipation)
		button.setText("Add")
		grid = QGridLayout()
		grid.addWidget(label2, 0, 0)
		grid.addWidget(label3, 0, 1)
		grid.addWidget(self.textEdit2, 1, 0)
		grid.addWidget(self.textEdit3, 1, 1)
		grid.addWidget(button, 1, 2)
		groupPart.setLayout(grid)

		button2 = QtWidgets.QPushButton()
		button2.clicked.connect(self.deleteMember)
		button2.setText("Delete Member")
		button2.setIcon(QtGui.QIcon(os.path.join(application_path, 'warning.png')))
		button3 = QtWidgets.QPushButton()
		button3.clicked.connect(self.showParticipation)
		button3.setText("Show Participations")
		button3.setIcon(QtGui.QIcon(os.path.join(application_path, 'volunteer.png')))
		verticalSpacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
		verticalSpacer2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
		vboxbtn = QVBoxLayout()
		vboxbtn.addItem(verticalSpacer)
		vboxbtn.addWidget(button3)
		vboxbtn.addWidget(button2)
		vboxbtn.addItem(verticalSpacer2)
		hbox2 = QHBoxLayout()
		hbox2.addWidget(groupPart)
		hbox2.addLayout(vboxbtn)

		vbox = QVBoxLayout()
		vbox.addWidget(self.table)
		vbox.addItem(verticalSpacer2)
		vbox.addWidget(label)
		vbox.addLayout(notebox)
		vbox.addItem(verticalSpacer2)
		vbox.addLayout(hbox2)
		self.setLayout(vbox)

	def setParentHeigh(self):
		# make sure the content of this widget is not shrinked
		# this is done by setting the minimum height to the scroll area that QToolBox adds when this widget is added to it
		parent = self.parent()
		if parent != None:
			gparent = parent.parent()
			if gparent != None:
				gparent.setMinimumHeight(370)

	def updateData(self):
		global internalDB
		# take updated data from db
		data = internalDB.execute("SELECT * FROM MEMBERS WHERE id = " + str(self.id))
		res = data.fetchone()

		date = ''
		if res[LASTSPEECH_POS] != None:
			date = getQDateFromTimestamp(res[LASTSPEECH_POS]).toString('dd/MM/yyyy')
		self.table.item(1,0).setText(date)		
		date = ''
		if res[LASTTMOD_POS] != None:
			date = getQDateFromTimestamp(res[LASTTMOD_POS]).toString('dd/MM/yyyy')
		self.table.item(1,1).setText(date)
		date = ''
		if res[LASTGENEVAL_POS] != None:
			date = getQDateFromTimestamp(res[LASTGENEVAL_POS]).toString('dd/MM/yyyy')
		self.table.item(1,2).setText(date)
		date = ''
		if res[LASTEVAL_POS] != None:
			date = getQDateFromTimestamp(res[LASTEVAL_POS]).toString('dd/MM/yyyy')
		self.table.item(1,3).setText(date)
		date = ''
		if res[LASTTIMER_POS] != None:
			date = getQDateFromTimestamp(res[LASTTIMER_POS]).toString('dd/MM/yyyy')
		self.table.item(1,4).setText(date)
		date = ''
		if res[LASTGRAMM_POS] != None:
			date = getQDateFromTimestamp(res[LASTGRAMM_POS]).toString('dd/MM/yyyy')
		self.table.item(1,5).setText(date)
		date = ''
		if res[LASTAHCOUNT_POS] != None:
			date = getQDateFromTimestamp(res[LASTAHCOUNT_POS]).toString('dd/MM/yyyy')
		self.table.item(1,6).setText(date)
		date = ''
		if res[LASTHUM_POS] != None:
			date = getQDateFromTimestamp(res[LASTHUM_POS]).toString('dd/MM/yyyy')
		self.table.item(1,7).setText(date)
		date = ''
		if res[LASTTTM_POS] != None:
			date = getQDateFromTimestamp(res[LASTTTM_POS]).toString('dd/MM/yyyy')
		self.table.item(1,8).setText(date)
		date = ''
		if res[LASTHACKM_POS] != None:
			date = getQDateFromTimestamp(res[LASTHACKM_POS]).toString('dd/MM/yyyy')
		self.table.item(1,9).setText(date)

	def addParticipation(self):
		global internalDB
		eName = str(self.textEdit2.text())
		eDuration = str(self.textEdit3.text())
		if eName == "":
			# mandatory field - signal error and return
			self.textEdit2.setStyleSheet("background-color: " + redBackground[0] + ";")
			self.currentObject = self.textEdit2
			self.currentBackground = redBackground
			self.backgroundIndex = 1
			# start timer to change background color
			self.timer.singleShot(100, QtCore.Qt.CoarseTimer, self.changeBackground)
			return
		if eDuration == "":
			# mandatory field - signal error and return
			self.textEdit3.setStyleSheet("background-color: " + redBackground[0] + ";")
			self.currentObject = self.textEdit3
			self.currentBackground = redBackground
			self.backgroundIndex = 1
			# start timer to change background color
			self.timer.singleShot(100, QtCore.Qt.CoarseTimer, self.changeBackground)
			return
		# convert participation to float
		eDuration = float(eDuration)
		# save data into mID table
		sql = 'INSERT INTO m%s (eventName, duration) values(?, ?)' % self.id
		data = (eName, eDuration)
		internalDB.execute(sql, data)
		internalDB.commit()
		# done - signal the event by changing background for a while
		self.textEdit2.setStyleSheet("background-color: " + greenBackground[0] + ";")
		self.textEdit3.setStyleSheet("background-color: " + greenBackground[0] + ";")
		self.backgroundIndex = 1
		# start timer to change background color
		self.timer.singleShot(100, QtCore.Qt.CoarseTimer, self.addPartDone)

	def showParticipation(self):
		spawnedWindow = ParticipationsWindow(self.id)
		self.dialogs.append(spawnedWindow)
		spawnedWindow.show()

	def deleteMember(self):
		# get member name
		data = internalDB.execute("SELECT name FROM MEMBERS WHERE id = " + str(self.id))
		name = data.fetchone()[0]
		dlg = QMessageBox(self)
		dlg.setWindowTitle("Delete member")
		dlg.setText("You are going to remove %s from this club. Are you sure?" % name)
		dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
		dlg.setDefaultButton(QMessageBox.No)
		dlg.setIcon(QMessageBox.Warning)
		choice = dlg.exec()
		if choice == QMessageBox.No:
			return
		# goodbye my friend
		internalDB.execute("UPDATE MEMBERS SET active = 0, mentor = ?, needMentor = 1 WHERE id = ?", (None, str(self.id)))
		# if this member has mentees, they need to have another mentor now
		mentees = internalDB.execute("SELECT id FROM MEMBERS WHERE mentor = ?", (name,))
		for mentee in mentees:
			internalDB.execute("UPDATE MEMBERS SET mentor = ?, needMentor = 1 WHERE id = ?", (None, str(mentee[0])))
		# kill yourself
		self.suicide.emit(self.id)
		internalDB.commit()

	def getID(self):
		return self.id

	def updateNotes(self):
		global internalDB
		# get notes content
		newNotes = str(self.textEdit.toPlainText())
		# update notes in db
		sql = "UPDATE MEMBERS SET notes = ? WHERE id = ?"
		data = (newNotes, self.id)
		internalDB.execute(sql, data)
		internalDB.commit()
		# change textEdit background to signal the successful operation
		self.textEdit.setStyleSheet("background-color: " + greenBackground[0] + ";")
		self.currentObject = self.textEdit
		self.currentBackground = greenBackground
		self.backgroundIndex = 1
		# start timer to change background color
		self.timer.singleShot(100, QtCore.Qt.CoarseTimer, self.changeBackground)

	def changeBackground(self):
		if self.backgroundIndex == len(self.currentBackground):
			# restore default color and stop timer
			self.currentObject.setStyleSheet("background-color: #FFFFFF;")
			self.backgroundIndex = 0
			return
		self.currentObject.setStyleSheet("background-color: " + self.currentBackground[self.backgroundIndex] + ";")
		self.backgroundIndex = self.backgroundIndex + 1
		nextTimer = 100
		if self.backgroundIndex >= (len(self.currentBackground) / 2): # speed up at the end
			nextTimer = 20
		self.timer.singleShot(nextTimer, QtCore.Qt.CoarseTimer, self.changeBackground)

	def addPartDone(self):
		if self.backgroundIndex == len(greenBackground):
			# restore default color and delete inserted strings
			self.textEdit2.setStyleSheet("background-color: #FFFFFF;")
			self.textEdit3.setStyleSheet("background-color: #FFFFFF;")
			self.textEdit2.setText("")
			self.textEdit3.setText("")
			self.backgroundIndex = 0
			return
		self.textEdit2.setStyleSheet("background-color: " + greenBackground[self.backgroundIndex] + ";")
		self.textEdit3.setStyleSheet("background-color: " + greenBackground[self.backgroundIndex] + ";")
		self.backgroundIndex = self.backgroundIndex + 1
		nextTimer = 100
		if self.backgroundIndex >= (len(greenBackground) / 2): # speed up at the end
			nextTimer = 20
		self.timer.singleShot(nextTimer, QtCore.Qt.CoarseTimer, self.addPartDone)


class ManageMembers(QtWidgets.QWidget):
	timer = QtCore.QTimer()
	redBackground = ['rgba(255, 0, 0, 1)', 'rgba(255, 0, 0, 0.9)', 'rgba(255, 0, 0, 0.8)', 'rgba(255, 0, 0, 0.7)', 'rgba(255, 0, 0, 0.6)', 'rgba(255, 0, 0, 0.5)', 'rgba(255, 0, 0, 0.4)', 'rgba(255, 0, 0, 0.3)', 'rgba(255, 0, 0, 0.2)', 'rgba(255, 0, 0, 0.1)']

	def __init__(self):
		global internalDB
		super(ManageMembers, self).__init__()
		if getattr(sys, 'frozen', False):
			application_path = sys._MEIPASS
		elif __file__:
			application_path = os.path.dirname(__file__)

		self.timer.setSingleShot(True)

		# plus button
		self.addIcon = QtGui.QIcon(os.path.join(application_path, 'add-friend.png'))
		self.removeIcon = QtGui.QIcon(os.path.join(application_path, 'remove-friend.png'))
		self.label_img = QtWidgets.QLabel(self)
		self.label_img.setPixmap(self.addIcon.pixmap(40,40))
		self.label_img.setMaximumSize(50, 50)
		self.label_img.mousePressEvent = self.addMember

		# groupbox new member
		self.groupMember = QtWidgets.QGroupBox()
		self.groupMember.setTitle("Add new member")
		self.groupMember.setObjectName("gmember")
		color = self.groupMember.palette().color(QtGui.QPalette.Base)
		self.groupMember.setStyleSheet("QWidget#gmember{background-color: rgb(%d, %d, %d)} QGroupBox { border: 1px solid gray; border-radius: 5px; margin-top: 15px; margin-bottom: 15px; }  QGroupBox::title {color: DarkGreen; subcontrol-origin: margin; top: 7px; left: 20px}" % (color.red(), color.green(), color.blue()))
		label = QtWidgets.QLabel()
		label.setText("Name")
		self.checkBox2 = QtWidgets.QCheckBox()
		self.checkBox2.setText("Last Speech")
		self.checkBox2.stateChanged.connect(self.checkboxChanged)
		self.checkBox2.setChecked(False)
		self.checkBox3 = QtWidgets.QCheckBox()
		self.checkBox3.setText("Last TMOD")
		self.checkBox3.stateChanged.connect(self.checkboxChanged)
		self.checkBox3.setChecked(False)
		self.checkBox4 = QtWidgets.QCheckBox()
		self.checkBox4.setText("Last GenEval")
		self.checkBox4.stateChanged.connect(self.checkboxChanged)
		self.checkBox4.setChecked(False)
		self.checkBox5 = QtWidgets.QCheckBox()
		self.checkBox5.setText("Last Eval")
		self.checkBox5.stateChanged.connect(self.checkboxChanged)
		self.checkBox5.setChecked(False)
		self.checkBox6 = QtWidgets.QCheckBox()
		self.checkBox6.setText("Last Timer")
		self.checkBox6.stateChanged.connect(self.checkboxChanged)
		self.checkBox6.setChecked(False)
		self.checkBox7 = QtWidgets.QCheckBox()
		self.checkBox7.setText("Last Grammarian")
		self.checkBox7.stateChanged.connect(self.checkboxChanged)
		self.checkBox7.setChecked(False)
		self.checkBox8 = QtWidgets.QCheckBox()
		self.checkBox8.setText("Last Ah Counter")
		self.checkBox8.stateChanged.connect(self.checkboxChanged)
		self.checkBox8.setChecked(False)
		self.checkBox9 = QtWidgets.QCheckBox()
		self.checkBox9.setText("Last Humorist")
		self.checkBox9.stateChanged.connect(self.checkboxChanged)
		self.checkBox9.setChecked(False)
		self.checkBox10 = QtWidgets.QCheckBox()
		self.checkBox10.setText("Last TTM")
		self.checkBox10.stateChanged.connect(self.checkboxChanged)
		self.checkBox10.setChecked(False)
		self.checkBox11 = QtWidgets.QCheckBox()
		self.checkBox11.setText("Last Hack Master")
		self.checkBox11.stateChanged.connect(self.checkboxChanged)
		self.checkBox11.setChecked(False)
		label12 = QtWidgets.QLabel()
		label12.setText("Notes")
		minDate = QtCore.QDateTime(1990, 1, 1, 10, 30)
		self.textEdit = QtWidgets.QLineEdit()
		self.textEdit.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
		self.textEdit2 = QtWidgets.QDateEdit()
		self.textEdit2.setEnabled(False)
		self.textEdit2.setMinimumDateTime(minDate)
		self.textEdit3 = QtWidgets.QDateEdit()
		self.textEdit3.setEnabled(False)
		self.textEdit3.setMinimumDateTime(minDate)
		self.textEdit4 = QtWidgets.QDateEdit()
		self.textEdit4.setEnabled(False)
		self.textEdit4.setMinimumDateTime(minDate)
		self.textEdit5 = QtWidgets.QDateEdit()
		self.textEdit5.setEnabled(False)
		self.textEdit5.setMinimumDateTime(minDate)
		self.textEdit6 = QtWidgets.QDateEdit()
		self.textEdit6.setEnabled(False)
		self.textEdit6.setMinimumDateTime(minDate)
		self.textEdit7 = QtWidgets.QDateEdit()
		self.textEdit7.setEnabled(False)
		self.textEdit7.setMinimumDateTime(minDate)
		self.textEdit8 = QtWidgets.QDateEdit()
		self.textEdit8.setEnabled(False)
		self.textEdit8.setMinimumDateTime(minDate)
		self.textEdit9 = QtWidgets.QDateEdit()
		self.textEdit9.setEnabled(False)
		self.textEdit9.setMinimumDateTime(minDate)
		self.textEdit10 = QtWidgets.QDateEdit()
		self.textEdit10.setEnabled(False)
		self.textEdit10.setMinimumDateTime(minDate)
		self.textEdit11 = QtWidgets.QDateEdit()
		self.textEdit11.setEnabled(False)
		self.textEdit11.setMinimumDateTime(minDate)
		self.textEdit12 = QtWidgets.QLineEdit()
		self.textEdit12.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
		self.pushButton = QtWidgets.QPushButton()
		self.pushButton.setObjectName(_fromUtf8("pushButton"))
		self.pushButton.clicked.connect(self.newMember)
		self.pushButton.setText("Add")
		grid = QGridLayout()
		grid.addWidget(label, 0, 0)
		grid.addWidget(self.checkBox2, 0, 1)
		grid.addWidget(self.checkBox3, 0, 2)
		grid.addWidget(self.checkBox4, 0, 3)
		grid.addWidget(self.checkBox5, 0, 4)
		grid.addWidget(self.checkBox6, 0, 5)
		grid.addWidget(self.checkBox7, 0, 6)
		grid.addWidget(self.checkBox8, 0, 7)
		grid.addWidget(self.checkBox9, 0, 8)
		grid.addWidget(self.checkBox10, 0, 9)
		grid.addWidget(self.checkBox11, 0, 10)
		grid.addWidget(label12, 0, 11)
		grid.addWidget(self.textEdit, 1, 0)
		grid.addWidget(self.textEdit2, 1, 1)
		grid.addWidget(self.textEdit3, 1, 2)
		grid.addWidget(self.textEdit4, 1, 3)
		grid.addWidget(self.textEdit5, 1, 4)
		grid.addWidget(self.textEdit6, 1, 5)
		grid.addWidget(self.textEdit7, 1, 6)
		grid.addWidget(self.textEdit8, 1, 7)
		grid.addWidget(self.textEdit9, 1, 8)
		grid.addWidget(self.textEdit10, 1, 9)
		grid.addWidget(self.textEdit11, 1, 10)
		grid.addWidget(self.textEdit12, 1, 11)
		grid.addWidget(self.pushButton, 1, 12)
		self.groupMember.setLayout(grid)
		
		self.scrollbarAddm = QtWidgets.QScrollArea(widgetResizable=True)
		self.scrollbarAddm.setFrameShape(QtWidgets.QFrame.NoFrame)
		#self.scrollbarAddm.verticalScrollBar().setEnabled(False)
		self.scrollbarAddm.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.scrollbarAddm.setWidget(self.groupMember)
		self.scrollbarAddm.setVisible(False) # do not show at startup

		# toobox - members detail
		self.toolbox = QToolBox()
		self.toolbox.setObjectName("toolbox")
		color = self.toolbox.palette().color(QtGui.QPalette.Base)
		styleSheet = """
				QWidget#toolbox{background-color: rgb(%d, %d, %d)}
				QToolBox::tab {
					border: 1px solid #C4C4C3;
					border-bottom-color: rgb(73, 172, 255);
				}
				QToolBox::tab:selected {
					background-color: rgb(73, 172, 255);
					border-bottom-style: none;
				}
			 """ % (color.red(), color.green(), color.blue())

		self.toolbox.setStyleSheet(styleSheet)
		with internalDB:
			data = internalDB.execute("SELECT * FROM MEMBERS WHERE active = 1 ORDER BY name")
			for row in data:
				member = MemberDetail(row[ID_POS])
				member.setStyleSheet("")
				member.suicide.connect(self.removeMember)
				self.toolbox.addItem(member, str(row[NAME_POS]))
				member.setParentHeigh()

		scrollbarMember = QtWidgets.QScrollArea(widgetResizable=True)
		scrollbarMember.setFrameShape(QtWidgets.QFrame.NoFrame)
		scrollbarMember.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		scrollbarMember.setWidget(self.toolbox)

		vbox = QVBoxLayout()
		vbox.addWidget(self.label_img, 5)
		vbox.addWidget(self.scrollbarAddm, 15)
		vbox.addWidget(scrollbarMember, 80)
		self.setLayout(vbox)

	def updateMembersData(self):
		for i in range(self.toolbox.count()):
			self.toolbox.widget(i).updateData()

	def checkboxChanged(self):
		if self.checkBox2.isChecked():
			self.textEdit2.setEnabled(True)
		else:
			self.textEdit2.setEnabled(False)
		if self.checkBox3.isChecked():
			self.textEdit3.setEnabled(True)
		else:
			self.textEdit3.setEnabled(False)
		if self.checkBox4.isChecked():
			self.textEdit4.setEnabled(True)
		else:
			self.textEdit4.setEnabled(False)
		if self.checkBox5.isChecked():
			self.textEdit5.setEnabled(True)
		else:
			self.textEdit5.setEnabled(False)
		if self.checkBox6.isChecked():
			self.textEdit6.setEnabled(True)
		else:
			self.textEdit6.setEnabled(False)
		if self.checkBox7.isChecked():
			self.textEdit7.setEnabled(True)
		else:
			self.textEdit7.setEnabled(False)
		if self.checkBox8.isChecked():
			self.textEdit8.setEnabled(True)
		else:
			self.textEdit8.setEnabled(False)
		if self.checkBox9.isChecked():
			self.textEdit9.setEnabled(True)
		else:
			self.textEdit9.setEnabled(False)
		if self.checkBox10.isChecked():
			self.textEdit10.setEnabled(True)
		else:
			self.textEdit10.setEnabled(False)
		if self.checkBox11.isChecked():
			self.textEdit11.setEnabled(True)
		else:
			self.textEdit11.setEnabled(False)

	def addMember(self, event):
		if self.scrollbarAddm.isVisible():
			self.scrollbarAddm.setVisible(False)
			self.label_img.setPixmap(self.addIcon.pixmap(40,40))
		else:
			self.scrollbarAddm.setVisible(True)
			self.label_img.setPixmap(self.removeIcon.pixmap(45,45))
		
	def newMember(self):
		global internalDB

		if str(self.textEdit.text()) == '':
			# member name is the only mandatory field - do not continue if it is not present
			# signal the error by changing background for a while
			self.textEdit.setStyleSheet("background-color: " + redBackground[0] + ";")
			self.backgroundIndex = 1
			self.timer.singleShot(100, QtCore.Qt.CoarseTimer, self.changeTEditBackground)
			return
		else:
			self.textEdit.setStyleSheet("border: 1px solid gray;")

		# build query string
		queryStringFields = 'INSERT INTO MEMBERS (name'
		queryStringValues = ') values(?'
		values = [str(self.textEdit.text())]
		if self.textEdit2.isEnabled():
			queryStringFields += ', lastSpeech'
			queryStringValues += ', ?'
			tstamp = getTimestampFromQDate(self.textEdit2.dateTime().toPyDateTime())
			values.append(int(tstamp))
		if self.textEdit3.isEnabled():
			queryStringFields += ', lastTMOD'
			queryStringValues += ', ?'
			tstamp = getTimestampFromQDate(self.textEdit3.dateTime().toPyDateTime())
			values.append(int(tstamp))
		if self.textEdit4.isEnabled():
			queryStringFields += ', lastGenEval'
			queryStringValues += ', ?'
			tstamp = getTimestampFromQDate(self.textEdit4.dateTime().toPyDateTime())
			values.append(int(tstamp))
		if self.textEdit5.isEnabled():
			queryStringFields += ', lastEval'
			queryStringValues += ', ?'
			tstamp = getTimestampFromQDate(self.textEdit5.dateTime().toPyDateTime())
			values.append(int(tstamp))
		if self.textEdit6.isEnabled():
			queryStringFields += ', lastTimer'
			queryStringValues += ', ?'
			tstamp = getTimestampFromQDate(self.textEdit6.dateTime().toPyDateTime())
			values.append(int(tstamp))
		if self.textEdit7.isEnabled():
			queryStringFields += ', lastGrammarian'
			queryStringValues += ', ?'
			tstamp = getTimestampFromQDate(self.textEdit7.dateTime().toPyDateTime())
			values.append(int(tstamp))
		if self.textEdit8.isEnabled():
			queryStringFields += ', lastAhCounter'
			queryStringValues += ', ?'
			tstamp = getTimestampFromQDate(self.textEdit8.dateTime().toPyDateTime())
			values.append(int(tstamp))
		if self.textEdit9.isEnabled():
			queryStringFields += ', lastHumorist'
			queryStringValues += ', ?'
			tstamp = getTimestampFromQDate(self.textEdit9.dateTime().toPyDateTime())
			values.append(int(tstamp))
		if self.textEdit10.isEnabled():
			queryStringFields += ', lastTTM'
			queryStringValues += ', ?'
			tstamp = getTimestampFromQDate(self.textEdit10.dateTime().toPyDateTime())
			values.append(int(tstamp))
		if self.textEdit11.isEnabled():
			queryStringFields += ', lastHackMaster'
			queryStringValues += ', ?'
			tstamp = getTimestampFromQDate(self.textEdit11.dateTime().toPyDateTime())
			values.append(int(tstamp))
		if str(self.textEdit12.text()) != '':
			queryStringFields += ', notes'
			queryStringValues += ', ?'
			values.append(str(self.textEdit12.text()))

		queryStringValues += ')'

		# insert member data in MEMBERS database
		sql = queryStringFields + queryStringValues
		data = [tuple(values)]
		with internalDB:
			internalDB.executemany(sql, data)

		# retrieve the just inserted item in order to get the unique ID
		data = internalDB.execute("SELECT * FROM MEMBERS ORDER BY id DESC LIMIT 1")
		res = data.fetchone()

		# create a new table, specific for the member, that will host participation information
		try:
			with internalDB:
				internalDB.execute("""
					CREATE TABLE m%s (
						eventName TEXT NOT NULL,
						duration REAL NOT NULL
					);
					""" % str(res[ID_POS]))
		except Exception as e:
			# critical error - delete just inserted member since we cannot continue
			try:
				internalDB.execute("DELETE FROM MEMBERS WHERE id = %s" % str(res[ID_POS]))
			except:
				pass
			dlg = QMessageBox(self)
			dlg.setWindowTitle("Add new member")
			dlg.setText("Internal error - member cannot be added.")
			dlg.setStandardButtons(QMessageBox.Ok)
			dlg.setIcon(QMessageBox.Critical)
			dlg.exec()
			return

		member = MemberDetail(res[ID_POS])
		member.suicide.connect(self.removeMember)
		self.toolbox.addItem(member, str(self.textEdit.text()))
		member.setParentHeigh()

		# member has been added - hide new member groupbox and show the just added member
		self.checkBox2.setChecked(False)
		self.checkBox3.setChecked(False)
		self.checkBox4.setChecked(False)
		self.checkBox5.setChecked(False)
		self.checkBox6.setChecked(False)
		self.checkBox7.setChecked(False)
		self.checkBox8.setChecked(False)
		self.checkBox9.setChecked(False)
		self.checkBox10.setChecked(False)
		self.checkBox11.setChecked(False)
		self.textEdit12.setText("")
		self.textEdit.setText("")
		self.addMember(None)
		self.toolbox.setCurrentWidget(member)
		# commit data only at the end
		internalDB.commit()

	def reinstateMember(self, mID, mName):
		member = MemberDetail(mID)
		member.suicide.connect(self.removeMember)
		self.toolbox.addItem(member, mName)
		member.setParentHeigh()

	def removeMember(self, mID):
		for i in range(self.toolbox.count()):
			widget = self.toolbox.widget(i)
			if widget.getID() == mID:
				# remove this widget
				self.toolbox.removeItem(i)
				return

	def changeTEditBackground(self):
		if self.backgroundIndex == len(redBackground):
			# restore default color and stop timer
			self.textEdit.setStyleSheet("background-color: #FFFFFF;")
			self.backgroundIndex = 0
			return
		self.textEdit.setStyleSheet("background-color: " + redBackground[self.backgroundIndex] + ";")
		self.backgroundIndex = self.backgroundIndex + 1
		nextTimer = 100
		if self.backgroundIndex >= (len(redBackground) / 2): # speed up at the end
			nextTimer = 20
		self.timer.singleShot(nextTimer, QtCore.Qt.CoarseTimer, self.changeTEditBackground)


################### Third tab #####################
############### Speakers priority #################
class CustomListWidgetItem(QtWidgets.QWidget):
	def __init__(self):
		super(CustomListWidgetItem, self).__init__()

		if getattr(sys, 'frozen', False):
			application_path = sys._MEIPASS
		elif __file__:
			application_path = os.path.dirname(__file__)

		self.textQVBoxLayout = QVBoxLayout()
		self.textUpQLabel    = QtWidgets.QLabel()
		self.textDownQLabel  = QtWidgets.QLabel()
		self.textQVBoxLayout.addWidget(self.textUpQLabel)
		self.textQVBoxLayout.addWidget(self.textDownQLabel)
		self.allQHBoxLayout  = QHBoxLayout()
		self.setLayout(self.textQVBoxLayout)
		# setStyleSheet
		self.textUpQLabel.setStyleSheet('''
			color: rgb(0, 0, 205); font-size: 14px; font-weight: bold;
		''')
		self.textDownQLabel.setStyleSheet('''
			font-style: oblique;
		''')

	def setTextUp (self, text):
		self.textUpQLabel.setText(text)

	def setTextDown (self, text):
		self.textDownQLabel.setText(text)



class SpeakersPriority(QtWidgets.QWidget):
	def __init__(self):
		super(SpeakersPriority, self).__init__()

		if getattr(sys, 'frozen', False):
			application_path = sys._MEIPASS
		elif __file__:
			application_path = os.path.dirname(__file__)

		self.list = QtWidgets.QListWidget()
		self.list.setObjectName("speakerList")
		self.list.setStyleSheet('QWidget#speakerList{background-image: url("%s"); background-repeat: no-repeat; background-position: center; background-color: rgba(255,255,255, 1); }' % os.path.join(application_path, 'color-logo.jpg').replace('\\', '/'))
		self.update()
		scrollbar = QtWidgets.QScrollArea(widgetResizable=True)
		scrollbar.setWidget(self.list)
		#print("connected")
		#self.verticalScrollBar = scrollbar.verticalScrollBar()
		#self.verticalScrollBar.sliderMoved.connect(self.updateBackground)
		
		vbox = QVBoxLayout()
		vbox.addWidget(scrollbar)
		self.setLayout(vbox)

	def update(self):
		global internalDB
		# query member information from db
		data = internalDB.execute("SELECT * FROM MEMBERS WHERE active = 1 ORDER BY lastSpeech")

		# clear previous data
		self.list.clear()

		# add updated data
		i = 0
		for row in data:
			item = QtWidgets.QListWidgetItem(self.list)
			customItem = CustomListWidgetItem()
			item.setSizeHint(customItem.sizeHint())
			lastSpeech = "never"
			if row[LASTSPEECH_POS] != None:
				lastSpeech = getQDateFromTimestamp(row[LASTSPEECH_POS]).toString('dd/MM/yyyy')
			customItem.setTextUp(row[NAME_POS])
			customItem.setTextDown("last speech: " + lastSpeech)
			if i < 3:
				item.setBackground(QtGui.QColor(255, 87, 51, 170))
			elif i < 6:
				item.setBackground(QtGui.QColor(255, 125, 51, 170))
			elif i < 9:
				item.setBackground(QtGui.QColor(255, 209, 51, 170))
			#self.list.insertItem(i, item)
			self.list.addItem(item)
			self.list.setItemWidget(item, customItem)
			i = i + 1

	#def updateBackground(self):
	#	print("called")
	#	self.list.setStyleSheet('QWidget#speakerList{background-image: url("%s"); background-repeat: no-repeat; background-position: center; background-color: rgba(255,255,255, 1); }' % os.path.join(application_path, 'color-logo.jpg').replace('\\', '/'))

################### Fourth tab #####################
##################### Mentors ######################
class Mentors(QtWidgets.QWidget):
	def __init__(self):
		super(Mentors, self).__init__()

		if getattr(sys, 'frozen', False):
			application_path = sys._MEIPASS
		elif __file__:
			application_path = os.path.dirname(__file__)

		label = QLabel()
		label.setText("Members who still need a mentor:")
		self.list = QtWidgets.QListWidget()
		scrollbar = QtWidgets.QScrollArea(widgetResizable=True)
		scrollbar.setWidget(self.list)
		
		label2 = QLabel()
		label2.setText("Current mentors:")
		self.tree = QtWidgets.QTreeWidget()
		self.tree.setHeaderHidden(True)
		scrollbar2 = QtWidgets.QScrollArea(widgetResizable=True)
		scrollbar2.setWidget(self.tree)
		#self.tree.setHeaderLabels(("Mentors",))
		self.update()

		vbox = QVBoxLayout()
		vbox.addWidget(label)
		vbox.addWidget(scrollbar)
		verticalSpacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
		vbox.addItem(verticalSpacer)
		vbox.addWidget(label2)
		vbox.addWidget(scrollbar2)
		self.setLayout(vbox)
		self.setStyleSheet("QLabel{font-size: 16px;}")

	def update(self):
		global internalDB
		# clear list
		self.list.clear()
		# get members who need a mentor
		data = internalDB.execute("SELECT name FROM MEMBERS WHERE active = 1 AND needMentor = 1 ORDER BY name")
		for name in data:
			item = QtWidgets.QListWidgetItem(self.list)
			item.setText(name[0])
			self.list.addItem(item)

		if self.list.count() != 0:
			self.list.setStyleSheet("background-color: rgba(255, 87, 51, 0.3);")
		else:
			self.list.setStyleSheet("")

		# clear tree
		self.tree.clear()
		# get members list
		data = internalDB.execute("SELECT name FROM MEMBERS WHERE active = 1 ORDER BY name")
		for name in data:
			# for each member, state his mentees
			menteesData = internalDB.execute("SELECT name FROM MEMBERS WHERE active = 1 AND mentor = ? ORDER BY name", (name[0],))
			mentees = []
			for mentee in menteesData:
				mentees.append(mentee[0])
			if mentees == []:
				# this member has no mentees - skip
				continue
			# this member has mentees - add him to the tree
			parent = QtWidgets.QTreeWidgetItem(self.tree)
			parent.setText(0, name[0])
			for mentee in mentees:
				# add his mentees
				child = QtWidgets.QTreeWidgetItem(parent)
				child.setText(0, mentee)


################### Fifth tab #####################
################## Old members ####################
class OldListWidgetItem(QtWidgets.QWidget):
	triggerUpdate = QtCore.pyqtSignal(int, str)

	def __init__(self, memberID, memberName):
		super(OldListWidgetItem, self).__init__()
		self.id = memberID
		self.name = memberName
		self.dialogs = list()

		if getattr(sys, 'frozen', False):
			application_path = sys._MEIPASS
		elif __file__:
			application_path = os.path.dirname(__file__)

		self.nameLabel = QLabel()
		self.nameLabel.setStyleSheet('''
			color: rgb(0, 0, 205); font-size: 14px; font-weight: bold;
		''')
		self.nameLabel.setText(memberName)
		toolbtn = QtWidgets.QToolButton()
		toolbtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
		toolbtn.setText("Show Participations")
		toolbtn.clicked.connect(self.showParticipation)
		toolbtn.setIcon(QtGui.QIcon(os.path.join(application_path, 'volunteer.png')))
		toolbtn1 = QtWidgets.QToolButton()
		toolbtn1.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
		toolbtn1.setText("Reinstate Member")
		toolbtn1.clicked.connect(self.bringAlive)
		toolbtn1.setIcon(QtGui.QIcon(os.path.join(application_path, 'login.png')))
		hbox = QHBoxLayout()
		hbox.addStretch()
		hbox.addWidget(toolbtn)
		hbox.addWidget(toolbtn1)
		vbox = QVBoxLayout()
		vbox.addWidget(self.nameLabel)
		vbox.addLayout(hbox)
		self.setLayout(vbox)

	def showParticipation(self):
		spawnedWindow = ParticipationsWindow(self.id)
		self.dialogs.append(spawnedWindow)
		spawnedWindow.show()

	def bringAlive(self):
		dlg = QMessageBox(self)
		dlg.setWindowTitle("Reinstate Member")
		dlg.setText("%s will be added again to the member lists. Do you want to proceed?" % self.name)
		dlg.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)
		dlg.setDefaultButton(QMessageBox.Cancel)
		dlg.setIcon(QMessageBox.Warning)
		choice = dlg.exec()
		if choice == QMessageBox.Cancel:
			return
		# welcome back
		internalDB.execute("UPDATE MEMBERS SET active = 1 WHERE id = " + str(self.id))
		internalDB.commit()
		self.triggerUpdate.emit(self.id, self.name)


class OldMembers(QtWidgets.QWidget):
	reinstateMember = QtCore.pyqtSignal(int, str)

	def __init__(self):
		super(OldMembers, self).__init__()

		if getattr(sys, 'frozen', False):
			application_path = sys._MEIPASS
		elif __file__:
			application_path = os.path.dirname(__file__)

		self.list = QtWidgets.QListWidget()
		#self.list.setAutoFillBackground(True)
		self.list.setObjectName("listObject")
		self.list.setStyleSheet('QWidget#listObject{background-image: url("%s"); background-repeat: no-repeat; background-position: center; background-color: rgba(255,255,255, 1); } QListWidget::item {background-color: rgba(224,224,224, 0.3); border-bottom: 1px solid gray }' % os.path.join(application_path, 'color-logo.jpg').replace('\\', '/'))
		self.update()
		scrollbar = QtWidgets.QScrollArea(widgetResizable=True)
		scrollbar.setWidget(self.list)
		self.update()
		
		vbox = QVBoxLayout()
		vbox.addWidget(scrollbar)
		self.setLayout(vbox)
		
	def update(self):
		global internalDB
		# query member information from db
		data = internalDB.execute("SELECT * FROM MEMBERS WHERE active = 0 ORDER BY name")

		# clear previous data
		self.list.clear()

		# add updated data
		for row in data:
			item = QtWidgets.QListWidgetItem(self.list)
			customItem = OldListWidgetItem(row[ID_POS], row[NAME_POS])
			customItem.triggerUpdate.connect(self.reinstate)
			item.setSizeHint(customItem.sizeHint())		
			self.list.addItem(item)
			self.list.setItemWidget(item, customItem)

	def reinstate(self, memberID, memberName):
		# update this list
		self.update()
		# update Member management tab
		self.reinstateMember.emit(memberID, memberName)


'''
Main GUI class
'''
class mainWindow(QtWidgets.QMainWindow):

	def __init__(self):
		super(mainWindow, self).__init__()

		if getattr(sys, 'frozen', False):
			application_path = sys._MEIPASS
		elif __file__:
			application_path = os.path.dirname(__file__)


		self.setWindowTitle("VPE Assistant")
		self.setWindowIcon(QtGui.QIcon(os.path.join(application_path, 'tmfavicon.ico')))

		self.tab1 = CreateAgenda()
		self.tab1.updateMembersData.connect(self.updateMembersTab)
		self.tab2 = ManageMembers()
		self.tab3 = SpeakersPriority()
		self.tab4 = Mentors()
		self.tab5 = OldMembers()
		self.tab5.reinstateMember.connect(self.reinstateMember)

		tabs = QtWidgets.QTabWidget()
		index = tabs.addTab(self.tab1, "Agenda")
		tabs.setTabIcon(index, QtGui.QIcon(os.path.join(application_path, 'schedule.png')))
		index = tabs.addTab(self.tab2, "Members management")
		tabs.setTabIcon(index, QtGui.QIcon(os.path.join(application_path, 'people.png')))
		index = tabs.addTab(self.tab3, "Speakers priority")
		tabs.setTabIcon(index, QtGui.QIcon(os.path.join(application_path, 'speaker.png')))
		index = tabs.addTab(self.tab4, "Mentors")
		tabs.setTabIcon(index, QtGui.QIcon(os.path.join(application_path, 'help.png')))
		index = tabs.addTab(self.tab5, "Previous members")
		tabs.setTabIcon(index, QtGui.QIcon(os.path.join(application_path, 'old-man.png')))
		tabs.currentChanged.connect(self.tabSelected)

		self.setCentralWidget(tabs)
		self.showMaximized()

		QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+Q"), self).activated.connect(QtCore.QCoreApplication.quit)
		QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+W"), self).activated.connect(QtCore.QCoreApplication.quit)


	def tabSelected(self, index):
		if index == 0:
			self.tab1.listMembers()
		elif index == 2:
			self.tab3.update()
		elif index == 3:
			self.tab4.update()
		elif index == 4:
			self.tab5.update()

	def updateMembersTab(self):
		self.tab2.updateMembersData()

	def reinstateMember(self, memberID, memberName):
		self.tab2.reinstateMember(memberID, memberName)


if __name__ == "__main__":
	# create the working folder if it doesn't exist yet
	if not os.path.exists(os.path.expanduser(workingDirectory)):
		os.makedirs(os.path.expanduser(workingDirectory))
	internalDB = sl.connect(os.path.expanduser(os.path.join(workingDirectory, 'membersData.db')))
	# create tables if they do not exist yet
	try:
		with internalDB:
			internalDB.execute("""
				CREATE TABLE MEMBERS (
					id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
					name TEXT NOT NULL,
					lastSpeech INTEGER,
					lastTMOD INTEGER,
					lastGenEval INTEGER,
					lastEval INTEGER,
					lastTimer INTEGER,
					lastGrammarian INTEGER,
					lastAhCounter INTEGER,
					lastHumorist INTEGER,
					lastTTM INTEGER,
					lastHackMaster INTEGER,
					notes TEXT,
					active INTEGER DEFAULT 1,
					meetingWithoutRole INTEGER DEFAULT 0,
					mentor TEXT,
					needMentor INTEGER DEFAULT 1
				);
			""")
	except sl.OperationalError:
		# exception is raised if table already exists
		pass

	try:
		with internalDB:
			internalDB.execute("""
				CREATE TABLE CURRENTMEETING (
					id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
					name TEXT,
					duration REAL,
					date INTEGER,
					speaker1 TEXT,
					speaker2 TEXT,
					TMOD TEXT,
					GenEval TEXT,
					Eval1 TEXT,
					Eval2 TEXT,
					Timer TEXT,
					Grammarian TEXT,
					AhCounter TEXT,
					Humorist TEXT,
					TTM TEXT,
					HackMaster TEXT,
					Presence TEXT
				);
			""")
	except sl.OperationalError as e:
		# exception is raised if table already exists
		pass

	try:
		with internalDB:
			internalDB.execute("""
				CREATE TABLE ADDITIONALROLES (
					name TEXT NOT NULL PRIMARY KEY,
					type INTEGER NOT NULL,
					member TEXT
				);
			""")
	except sl.OperationalError as e:
		# exception is raised if table already exists
		pass

	app = QtWidgets.QApplication(sys.argv)
	wt = mainWindow()
	wt.show()
	sys.exit(app.exec_())