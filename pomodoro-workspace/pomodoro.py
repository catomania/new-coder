"""
Pomodoro timer, the idea came from here: http://newcoder.io/gui/extended/

Pomodoro application - a timer for productivity, where you work for 25 minutes, and take a break for 5 minutes.
You'd have a least a start button widget, perhaps a widget reflecting the time countdown.

The alarm sound is actually a new tab that loads which play's FKA Twig's Two Weeks music video.
"""

# countdown timers: http://stackoverflow.com/questions/10596988/making-a-countdown-timer-with-python-and-tkinter
# http://www.tkdocs.com/tutorial/firstexample.html

from Tkinter import *
import ttk, time, webbrowser

# used for pausing and resuming countdowns
pause = False 

# used for exiting a loop and ending the program
let_me_quit = False

# countdowns in seconds
my_countdown_seconds = []
twenty_five_minutes = 1500

short_break_seconds = [300]

# to record the last function that was called
last_function_called = []

# quit button
def quit_me():
	global let_me_quit
	let_me_quit= True
	raise SystemExit

# main 25:00 timer
def count_down():

	# set a last_function_called value
	del last_function_called[:] # you can still clear out an already empty list
	last_function_called.append("count_down")

	# make sure that you're counting down from the top if you're starting at 00:00, otherwise resume mid-countdown
	#  is it not-pythonic to not have an "else" statement after an if statement?
	# what if you're coming back from a short break?
	get_label = type_of_activity.get()
	
	if get_label == "Break Time" or get_label == "Not Started":
		del my_countdown_seconds[:]
		my_countdown_seconds.append(twenty_five_minutes)
	
	elif not get_label:
		my_countdown_seconds.append(twenty_five_minutes)
	
	# else: get the time left on the label and proceed from there after coming back from a pause
	else:
		get_time = str(timer_display.get())
		timer_minutes = get_time.split(":")
		del my_countdown_seconds[:]
		my_countdown_seconds.append(int(timer_minutes[0]) * 60 + int(timer_minutes[1]))
	
	# "work time" loop
	for t in range(int(my_countdown_seconds[-1]), -1, -1): # get and update current range
		if last_function_called[0] == "pause":
			break

		if let_me_quit is True:
			raise SystemExit
		
		# break the loop if reset is called
		if last_function_called[0] == "reset":
			break

		ta = "Work Time"	
		type_of_activity.set(ta)

		sf = "{:02d}:{:02d}".format(*divmod(t, 60))
		timer_display.set(sf)
		time.sleep(1)
		root.update() # http://stackoverflow.com/questions/11303200/python-tkinter-loop-in-label

		my_countdown_seconds.append(t-1) # not the most efficient way to go about it

		# once you're down w/ work time, it's time for a short break! 
		if my_countdown_seconds[-1] == 0:
			webbrowser.get('firefox').open_new_tab("https://www.youtube.com/watch?v=3yDP9MKVhZc")
				# once loop is done, call short break
			del short_break_seconds[:]
			short_break_seconds.append(300)
			short_break()

def short_break():
	del last_function_called[:]
	last_function_called.append("short_break")

	# countdown loop for the short break
	for t in range(int(short_break_seconds[-1]), -1, -1): # do a logic test to see if other timers are running?
		if last_function_called[0] == "pause":
			break

		if let_me_quit is True:
			raise SystemExit
		
		# break the loop if reset is called
		if last_function_called[0] == "reset":
			break

		# update the label to say that we're in our short break loop
		ta = "Break Time"
		type_of_activity.set(ta)
		
		# display the time left in our short break cycle
		sf = "{:02d}:{:02d}".format(*divmod(t, 60))
		timer_display.set(sf)
		short_break_seconds.append(t-1)
		time.sleep(1)
		root.update()

	# once short break is done, go back to the 25 minute countdown
	if short_break_seconds[-1] == 0:
		del my_countdown_seconds[:]
		my_countdown_seconds.append(twenty_five_minutes)
		count_down()

def timer_reset():
	# if you hit the reset button first when app is opened, add nothing to the "last function called" list
	if not last_function_called:
		pass
	else:
		del last_function_called[:]
		last_function_called.append("reset")

	del short_break_seconds[:]
	short_break_seconds.append(300)

	del my_countdown_seconds[:]
	my_countdown_seconds.append(twenty_five_minutes)

	# call default view
	default_view()

def pause_or_resume():

	global pause

	get_label = type_of_activity.get() # no label, short, long, not started

	# pause if I hit this a second time not in succession
	if not get_label:
		count_down()
	
	elif get_label == "Not Started":
		count_down()

	elif get_label ==  "Work Time":
		pause = True
		del last_function_called[:]		
		last_function_called.append("pause") # break time paused or work time paused?
		type_of_activity.set("Work Time: Paused")

	elif get_label == "Break Time":
		pause = True
		del last_function_called[:]		
		last_function_called.append("pause") # break time paused or work time paused?
		type_of_activity.set("Break Time: Paused")

	elif get_label == "Work Time: Paused":
		pause = False
		count_down()

	elif get_label == "Break Time: Paused":
		pause = False
		short_break()


def default_view():
	# set 0 time and say "not started"
	not_started = "Not Started"	
	type_of_activity.set(not_started)
	timer_display.set("00:00")
	root.update()

root = Tk() # no parent needed to be passed as a parameter for the root window
root.title("Pomodoro Me")

# build the Timer window and widgets

mainframe = ttk.Frame(root, padding="3 3 12 12") # when creating a widget, parent must be passed as parameter
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

timer_display = StringVar()
type_of_activity = StringVar()
padding_hack = str(" ") * 30

# padding?
ttk.Label(mainframe, text=padding_hack).grid(column=2, row=3, sticky=W) # hacky workaround for space for 2nd col
ttk.Label(mainframe, textvariable=timer_display).grid(column=2, row=2, sticky=W)
ttk.Label(mainframe, textvariable=type_of_activity).grid(column=2, row=3, sticky=W)#, sticky=(W, E))
ttk.Button(mainframe, text="Start Timer", command=count_down).grid(column=3, row=3, sticky=W)
ttk.Button(mainframe, text="Pause", command=pause_or_resume).grid(column=3, row=7, sticky=W)
ttk.Button(mainframe, text="Reset", command=timer_reset).grid(column=3, row=8, sticky=W)

ttk.Label(mainframe, text="Timer:").grid(column=1, row=2, sticky=E)
ttk.Label(mainframe, text="Time Remaining").grid(column=3, row=2, sticky=W)

# other buttons: short, long, reset timer
# quit button

ttk.Button(mainframe, text="Quit", command=quit_me).grid(column=3, row=6, sticky=W)
for child in mainframe.winfo_children(): child.grid_configure(padx=15, pady=10)

root.bind('<Return>', count_down)
root.mainloop()