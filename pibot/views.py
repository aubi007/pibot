'''
**********************************************************************
* Filename    : views
* Description : views for server
* Author      : Cavon
* Brand       : SunFounder
* E-mail      : service@sunfounder.com
* Website     : www.sunfounder.com
* Update      : Cavon    2016-09-13    New release
**********************************************************************
'''

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import StreamingHttpResponse

import cv2
from pibot.bot import bot

def home(request):
	return render_to_response("base.html")


# yields a streaming generator from camera frames
def yield_generator(cam):
	last_ts = None			# timestamp of the last processed frame
	while True:
		(frame, ts) = cam.get_frame(bot.bot.get_status_line())
		# yield a new frame only when timestamp has changed
		if frame is not None and ts != last_ts:
			ts = last_ts
			yield(b'--frame\r\n'
				  b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
			
def livefe(request):
	try:
		print ('livefe')
		gen = yield_generator(bot.bot.str)
		return StreamingHttpResponse(gen, content_type="multipart/x-mixed-replace;boundary=frame")
	except:
		print ('error')
		pass
       
def run(request):
	debug = ''
	if 'action' in request.GET:
		action = request.GET['action']
		# ============== Back wheels =============
		if action == 'bwready':
			bot.bot.set_bw_status(0)
		elif action == 'forward':
			bot.bot.set_bw_status(1)
		elif action == 'backward':
			bot.bot.set_bw_status(-1)
		elif action == 'stop':
			bot.bot.set_bw_status(0)

		# ============== Front wheels =============
		elif action == 'fwready':
			bot.bot.set_fw_pos(0)
		elif action == 'fwleft':
			bot.bot.set_fw_pos(-40)
		elif action == 'fwright':
			bot.bot.set_fw_pos(40)
		elif action == 'fwstraight':
			bot.bot.set_fw_pos(0)
			
		# ================ Camera =================
		elif action == 'camready':
			bot.bot.cam_ready()
		elif action == "camleft":
			bot.bot.set_cam_pan(40)
		elif action == 'camright':
			bot.bot.set_cam_pan(-40)
		elif action == 'camup':
			bot.bot.set_cam_tilt(20)
		elif action == 'camdown':
			bot.bot.set_cam_tilt(-20)
		
		# ================ test commands =============
		elif action == 'screenshot':
			bot.bot.str.screenshot()
		elif action == 'test':
			bot.bot.run_test(1)
			
	# ================ Speed =================	
	if 'speed' in request.GET:
		print ('speeed')
		speed = int(request.GET['speed'])
		if speed < 0:
			speed = 0
		if speed > 100:
			speed = 100
		bot.bot.set_speed(speed)	
			
	return render_to_response("run.html")
			

	
def cali(request):
	return render_to_response("cali.html")

	if 'action' in request.GET:
		action = request.GET['action']
		# ========== Camera calibration =========
		if action == 'camcali':
			print ('"%s" command received' % action)
			cam.calibration()
		elif action == 'camcaliup':
			print ('"%s" command received' % action)
			cam.cali_up()
		elif action == 'camcalidown':
			print ('"%s" command received' % action)
			cam.cali_down()
		elif action == 'camcalileft':
			print ('"%s" command received' % action)
			cam.cali_left()
		elif action == 'camcaliright':
			print ('"%s" command received' % action)
			cam.cali_right()
		elif action == 'camcaliok':
			print ('"%s" command received' % action)
			cam.cali_ok()

		# ========= Front wheel cali ===========
		elif action == 'fwcali':
			print ('"%s" command received' % action)
			fw.calibration()
		elif action == 'fwcalileft':
			print ('"%s" command received' % action)
			fw.cali_left()
		elif action == 'fwcaliright':
			print ('"%s" command received' % action)
			fw.cali_right()
		elif action == 'fwcaliok':
			print ('"%s" command received' % action)
			fw.cali_ok()

		# ========= Back wheel cali ===========
		elif action == 'bwcali':
			print ('"%s" command received' % action)
			bw.calibration()
		elif action == 'bwcalileft':
			print ('"%s" command received' % action)
			bw.cali_left()
		elif action == 'bwcaliright':
			print ('"%s" command received' % action)
			bw.cali_right()
		elif action == 'bwcaliok':
			print ('"%s" command received' % action)
			bw.cali_ok()
		else:
			print ('command error, error command "%s" received' % action)



def connection_test(request):
	return HttpResponse('OK')