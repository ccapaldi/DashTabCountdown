# A simple test for Linux Frame Buffer
# Imports fb (frame buffer) module and uses it as lvgl display driver
# then show a button on screen.

DEBUG = False

import lvgl as lv
lv.init()
import fb
fb.init()
import _thread
import utime


disp_buf1 = lv.disp_buf_t()
buf1_1 = bytearray(320*10)
lv.disp_buf_init(disp_buf1, buf1_1, None, len(buf1_1)//4)

disp_drv = lv.disp_drv_t()
lv.disp_drv_init(disp_drv)
disp_drv.buffer = disp_buf1
disp_drv.flush_cb = fb.flush
#disp_drv.hor_res = fb.fill
#disp_drv.ver_res = fb.map
lv.disp_drv_register(disp_drv)


import xpt7603
touch = xpt7603.xpt7603()
touch.init()

indev_drv = lv.indev_drv_t()
lv.indev_drv_init(indev_drv) 
indev_drv.type = lv.INDEV_TYPE.POINTER;
indev_drv.read_cb = touch.read;
lv.indev_drv_register(indev_drv);

# Load the screen
scr = lv.obj()
lv.scr_load(scr)
#
# Start of thread code
thCount=30
threadRunning=False
# create objects
#Thread function
MY_THREAD=_thread
# This routine lets you set the start count to any value
def setCount(newCount):
	global thCount
	
	print("resetting the count to " + str(newCount))
	#set the new count value and reset the counter
	thCount=newCount

	
	
def th_func(delay,id):
	# thCount is what the thread gets set to 
	
	global thCount, threadRunning

	thCounter=1

	print("Starting thread for "+str(thCount))
	threadRunning=True
	
	while thCounter <= thCount:
		utime.sleep(1)
		print("Count=" + str(thCount))
		thCount -= 1
		
	
	
	threadRunning=False
	# action to perform 
	tv.set_tab_act(0,True)	
	print('Thread finished')

#
# End of thread code
def startThread():
	global thCount
	MY_THREAD.start_new_thread(th_func,(thCount, 1))
	
	
def on_tabchange(obj, event):
	global tabChanged, threadRunning
	
	if event == lv.EVENT.VALUE_CHANGED:
		print('You changed the tab')
		print('Threadrunning='+str(threadRunning))
		# we will demonstrate a new countdown start value by using 35
		setCount(35)
		
		# We do not want to start a thread if one is already running
		# Changing he global thCount value will automaticaly reset a running thread
		
		if threadRunning == False:
			print("Starting a new thread")
			startThread()
		else:
			print("Thread already running")


tv=lv.tabview(lv.scr_act())
tv.set_event_cb(on_tabchange)
tab1=tv.add_tab("Tab1")
tab2=tv.add_tab("Tab2")
tab3=tv.add_tab("Tab3")

lbl = lv.label(tab1)
lbl.set_text("This is the first tab\n\n"
				"If the content\n"
				"of a tab\n"
				"become too long\n"
				"the it \n"
				"automatically\n\n"
				"become\n\n"
				"scrollable.")

lbl = lv.label(tab2)
lbl.set_text("This is tab2")
lbl = lv.label(tab3)
lbl.set_text("Tab3")
# To demonstrate I will display the third tab and start the countdown thread
tv.set_tab_act(3,True)
startThread()

print('starting main loop and first thread')



while True:
	#Main program loop
	#MY_THREAD.start_new_thread(th_func,(thCount, 1))
	pass