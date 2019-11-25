import sys
import json

import PyQt5

from PyQt5 import QtWidgets
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QDate, QLocale, Qt
from PyQt5.QtGui import QFont, QTextCharFormat
import matplotlib.pyplot as plt
# #caution, not all imports are used
#problem: years don't get accounted (unique month?)



class Window(QtWidgets.QMainWindow):
	def __init__(self):
		super(Window, self).__init__()
		self.setGeometry(50,50,555,350)
		self.setWindowTitle("geheim")
		#self.setWindowIcon(QtWidgets.QIcon("pythonlogo.png")

		
		#stuff for main menu
		extract_action = QtWidgets.QAction("random sentence", self)
		#extract_action.setShortcut("Ctrl+Q")
		#extract_action.setStatusTip("Leave App")
		extract_action.triggered.connect(self.test)

		#new tab in main menu bar
		test_task = QtWidgets.QAction("test", self)
		test_task.triggered.connect(self.test)

		#tab for calc avg
		calc_avg_task = QtWidgets.QAction("Calculate average", self)
		calc_avg_task.triggered.connect(self.calc_avg)

		quit_action = QtWidgets.QAction("Quit", self)
		quit_action.triggered.connect(self.close_application)

		self.months = {
		1:"january", 2:"february", 3:"march", 4:"april", 5:"may", 6:"june", 
		7:"july", 8:"august", 9:"september",10:"october", 11:"november", 12:"december"
		}




		self.statusBar()

		main_menu = self.menuBar()

		#File
		fileMenu = main_menu.addMenu("&File")        
		fileMenu.addAction(extract_action)


		#months menu
		month_menu = main_menu.addMenu("&Month")
		for v in self.months.values():
			v_task = QtWidgets.QAction(v, self)
			v_task.triggered.connect(self.monthly_spent)
			month_menu.addAction(v_task)
		

		#Test
		testMenu = main_menu.addMenu("&Test")
		testMenu.addAction(test_task)
		testMenu.addAction(calc_avg_task)
		testMenu.addAction(quit_action)




		#create dictionary to keep record of dates and money spent
		self.calendar_dict = {}

		self.BACKGROUNDCOLOR = QtGui.QColor(186, 255, 148)



		# self.path = "c:/users/admin/desktop/uni/pyhton/gui"
		self.path = "/home/stefan/projects/money_tracker"
		self.calendar_data = self.path + "/calendar_data"

		
		self.home()


	def home(self):



		#calendar (previously in init function)
		self.calendar = QtWidgets.QCalendarWidget(self)
		#set stylesheet here
		self.calendar.resize(300, 300)
		self.calendar.move(10, 30)
		#what is to happen if the user selects a date by clickingon it (date_change contains funtionality)
		self.calendar.clicked[QtCore.QDate].connect(self.date_change)


		#create textbox to enter stuff
		self.textbox = QtWidgets.QTextEdit(self)
		self.textbox.move(330, 30)
		self.textbox.resize(210, 120)



		#create textbox to display stugg
		self.displaybox = QtWidgets.QTextEdit(self)
		self.displaybox.move(330, 160)
		self.displaybox.resize(210, 40)
		self.displaybox.setReadOnly(True)



		#add buttons 
		self.add_button("test", self.test, [100, 40], [330, 290]) #formerly edit
		self.add_button("Save", self.save_file, [100, 40], [440, 290])

		#add avg and sum button
		self.add_button("calc avg", self.calc_avg, [100, 40], [330, 210])
		self.add_button("calc sum", self.calc_sum, [100, 40], [440, 210])


		# self.sel_date = str(self.calendar.selectedDate())
		self.date_change()

		self.mark_entrys()

		self.show()



	def close_application(self):
		sys.exit()





	def test(self):
		print("test:")
		#write stuff here
		# for i in range(1, 13):
		# 	print(i, self.month_length(i))
		# print(self.get_unique_month(self.sel_date))
		cal_dict = self.load_dict()
		self.plot_spendings(self.get_month(self.sel_date), cal_dict)
		print("test end")

	def date_change(self):
		#clear textbox
		# self.textbox.clear()


		self.sel_date = str(self.calendar.selectedDate())
		print(self.sel_date)


		#load stuff here
		try:
			entry = self.load_value(self.sel_date)
			text = str(entry)
			self.textbox.setText(text + " €")
		except KeyError:
			# print("no value available yet")
			self.textbox.setText("no entry available yet")

	def add_button(self, label, f, size, pos): 
		btn = QtWidgets.QPushButton(label, self)
		btn.clicked.connect(f)
		btn.resize(size[0], size[1])
		btn.move(pos[0], pos[1]) 




	def save_file(self):

		text = self.textbox.toPlainText()

		entry = float(text.replace(" €", ""))
		# self.edit_dict(self.sel_date, text)
		print(self.sel_date, entry)

		self.edit_dict(self.sel_date, entry)


		# file.write(text) #del
		# file.close() #del

	def print_calendar_dict(self):
		print(self.calendar_dict)


	#TODO load date? (date change)

	#edit dicts or add new keys
	def edit_dict(self, key, data):
	    # file = open("c:/users/admin/desktop/test2", "r")
	    file = open(self.calendar_data, "r")
	    content = json.load(file)
	    content[key] = data
	    toBeSaved = json.dumps(content, indent = True)
	    file = open(self.calendar_data, "w")
	    file.write(toBeSaved)
	    file.close()
	    self.mark_entrys()




	def load_value(self, key):
		file = open(self.calendar_data, "r")
		content = json.load(file)
		data = content[key]
		file.close()
		# data = float(data)
		print(type(data))
		return data

	def load_dict(self):
		file = open(self.calendar_data, "r")
		content = json.load(file)
		cal_dict = content
		file.close()
		return cal_dict


	def calc_avg(self):
		cal_dict = self.load_dict()
		values = [v for v in cal_dict.values()]
		return (sum(values)/len(values))


	def get_month(self, date): #idea: create unique month with year as metadata
		return int(date.split(",")[1])
		# return int(date.split("(")[1].split(",")[0] + date.split(",")[1])
		# return int(date.split(",")[1] + str(self.get_year(date)))


	def get_unique_month(self, date):
		return int(date.split(",")[1] + str(self.get_year(date)))



	def get_year(self, date):
		return int(date.split("(")[1].split(",")[0])



	def get_vanilla_date(self, date):
		return date.split("(")[1].replace(")", "")



	def list_spendings_month(self, month): #account for year also
		cal_dict = self.load_dict()
		values = []
		for k in cal_dict.keys():
			if self.get_month(k) == month: # and (self.get_year(k) == year)#and year == year
				v = cal_dict[k]
				values.append(v)
		# return values
		return values



	def list_spendings_total(self):
		cal_dict = self.load_dict()
		values = [v for v in cal_dict.values()]
		return values



	def monthly_spent(self, month):
		# cal_dict = self.load_dict()
		# values = []
		# for v in cal_dict.values():
		# 	if self.get_month() == month:
		# 		values.append(v)
		values = self.list_spendings_month(month)
		return sum(values)


#TODO enable user to plot spendings over the course of a month
	def plot_spendings(self, month, dict):
		l = [x for x in range(self.month_length(month))]
		print(list(dict.keys()))
		# print(l)
		ml = list(map(lambda x: dict[x] if x in list(dict.keys()) else 0, l)) 
		# print(ml)
		plt.plot(l, ml, "bs")
		# plt.show()

		# values = self.list_spendings_month(month)
		# plt.plot([x for x in range(len(values))], values)
		# plt.show()



# >>> def plot_spendings(m, d):
# 	l = [x for x in range(len(m))]
# 	ml = list(map( lambda x: d[x] if x in list(d.keys()) else 0, l))
# 	plt.plot(l, ml, "bs")
# 	plt.show()


	#TODO display stuff (use: my_text_edit.setReadOnly(True))
	def display(self, data):
		self.displaybox.setText(str(data))


	def calc_avg(self): #
		current_month = self.get_month(self.sel_date)
		current_year = self.get_year(self.sel_date)
		length = len(self.list_spendings_month(current_month))
		if length == 0:
			out = "no money spent yet"
		else:
			result = round(sum(self.list_spendings_month(current_month))/self.month_length(current_month), 2)
			out = (
			"average sum in " 
			+ self.months[current_month] 
			+ ": "
			# + str(sum(self.list_spendings_month(current_month))/self.month_length(current_month))
			+ str(result)
			+ " €")

		self.display(out)



	def calc_sum(self):
		self.display("total sum in " 
			+ self.months[self.get_month(self.sel_date)] 
			+ ": "
			+ str(sum(self.list_spendings_month(self.get_month(self.sel_date)))) 
			+ " €")


	#TODO paint cell if entry exists
	#solution re-implement calendar widget and overwrite paint cell lol
	#alternative idea: select multiple dates?
	
	# def value_entered_check(self, date): #not used
	# 	cal_dict = self.load_dict()
	# 	keys = [k for k in cal_dict.keys()]
	# 	#return keys[0] #returns str
	# 	for i in range(len(keys)):
	# 		if keys[i] == date:
	# 			return True
	# 	return False



	def mark_entry(self, date):

		value_entered_format = QTextCharFormat()
		value_entered_format.setBackground(self.BACKGROUNDCOLOR) #formerly Qt.green

		constr_date = self.get_vanilla_date(date)

		y, m, d = int(constr_date.split()[0].replace(",", "")), int(constr_date.split()[1].replace(",", "")), int(constr_date.split()[2].replace(",", ""))
		# print(y,m,d)

		self.calendar.setDateTextFormat(QDate(y, m, d), value_entered_format)



	def mark_entrys(self):
		cal_dict = self.load_dict()
		for k in cal_dict.keys():
			# print(cal_dict[k])
			if cal_dict[k] != 0.0:
				self.mark_entry(k)


	def month_length(self, month):
		if (month == 1) or (month ==3) or (month ==5) or (month ==7) or (month ==8) or (month ==10) or (month ==12):
			length = 31
		elif month == 2:
			length = 28 
		else:
			length = 30
		return length



		












def main():  
	app = QtWidgets.QApplication(sys.argv)
	GUI = Window()
	sys.exit(app.exec_())







main()
