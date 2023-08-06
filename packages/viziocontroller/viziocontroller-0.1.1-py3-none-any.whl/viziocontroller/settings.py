import inspect
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

def _x_batch_process_exec_next_iter( options ):
	if len( options ) > 2:
		result = options[ 1 ]( *options[ 2 ] )
	else:
		result = options[ 1 ]()
	return result

def _x_batch_process( options ):
	batch_size = len( options[ "batch_list" ] )
	with ThreadPoolExecutor() as executor:
		# result_pool = list( tqdm( executor.map( batch_process_exec_next_iter , iter( options[ "batch_list" ] ) ) , total=batch_size ) )
		result_pool = list( executor.map( _x_batch_process_exec_next_iter , iter( options[ "batch_list" ] ) ) )
		return result_pool

# https://stackoverflow.com/q/15608987
def stack_reach( name ):
	for f in inspect.stack():
		if name in f[ 0 ].f_locals:
			return f[ 0 ].f_locals[ name ]
	return None

def get_parent_class_context():
	for f in inspect.stack():
		if "__name__" not in f[ 0 ].f_locals:
			continue
		if "viziocontroller" not in f[ 0 ].f_locals:
			continue
		return f[ 0 ].f_locals[ "viziocontroller" ]
	return False

class Settings:

	def __init__( self , options={} ):
		self.options = options
		self.this = get_parent_class_context()
		self.api = self.this.__dict__[ "API" ]

	def test( self ):
		#print( self.api )
		for f in inspect.stack():
			if "__name__" not in f[ 0 ].f_locals:
				continue
			# print( f[ 0 ].f_locals )
			print( f[ 0 ].f_locals[ "viziocontroller" ].__dict__[ "API" ].get_setting )

	def get_picture_settings( self ):
		batch_list = [
			[ "picture_mode" , self.api.get_setting , [ self , "picture" , "picture_mode" ] ] ,
			[ "backlight" , self.api.get_setting , [ self , "picture" , "backlight" ] ] ,
			[ "brightness" , self.api.get_setting , [ self , "picture" , "brightness" ] ] ,
			[ "contrast" , self.api.get_setting , [ self , "picture" , "contrast" ] ] ,
			[ "color" , self.api.get_setting , [ self , "picture" , "color" ] ] ,
			[ "tint" , self.api.get_setting , [ self , "picture" , "tint" ] ] ,
			[ "sharpness" , self.api.get_setting , [ self , "picture" , "sharpness" ] ] ,
			[ "more_picture" , self.api.get_setting , [ self , "picture" , "more_picture" ] ]
		]
		result = _x_batch_process({
			"max_workers": 3 ,
			"batch_list": batch_list ,
		})
		return {
			"picture_mode": result[ 0 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"backlight": result[ 1 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"brightness": result[ 2 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"contrast": result[ 3 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"color": result[ 4 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"tint": result[ 5 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"sharpness": result[ 6 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"more_picture": result[ 7 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
		}

	def get_audio_settings( self ):
		batch_list = [
			[ "tv_speakers" , self.api.get_setting , [ self , "audio" , "tv_speakers" ] ] ,
			[ "volume_control_display" , self.api.get_setting , [ self , "audio" , "volume_control_display" ] ] ,
			[ "surround_sound" , self.api.get_setting , [ self , "audio" , "surround_sound" ] ] ,
			[ "volume_leveling" , self.api.get_setting , [ self , "audio" , "volume_leveling" ] ] ,
			[ "balance" , self.api.get_setting , [ self , "audio" , "balance" ] ] ,
			[ "lip_sync" , self.api.get_setting , [ self , "audio" , "lip_sync" ] ] ,
			[ "digital_audio_out" , self.api.get_setting , [ self , "audio" , "digital_audio_out" ] ] ,
			[ "analog_audio_out" , self.api.get_setting , [ self , "audio" , "analog_audio_out" ] ] ,
			[ "volume" , self.api.get_setting , [ self , "audio" , "volume" ] ] ,
			[ "mute" , self.api.get_setting , [ self , "audio" , "mute" ] ] ,
			[ "equalizer" , self.api.get_setting , [ self , "audio" , "equalizer" ] ] ,
			[ "delete_audio_mode" , self.api.get_setting , [ self , "audio" , "delete_audio_mode" ] ] ,
		]
		result = _x_batch_process({
			"max_workers": 3 ,
			"batch_list": batch_list ,
		})
		return {
			"tv_speakers": result[ 0 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"volume_control_display": result[ 1 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"surround_sound": result[ 2 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"volume_leveling": result[ 3 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"balance": result[ 4 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"lip_sync": result[ 5 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"digital_audio_out": result[ 6 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"analog_audio_out": result[ 7 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"volume": result[ 8 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"mute": result[ 9 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"equalizer": result[ 10 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"delete_audio_mode": result[ 11 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
		}

	def get_network_settings( self ):
		batch_list = [
			[ "connection_type" , self.api.get_setting , [ self , "network" , "connection_type" ] ] ,
			[ "connection_status" , self.api.get_setting , [ self , "network" , "connection_status" ] ] ,
			[ "dhcp_mode" , self.api.get_setting , [ self , "network" , "dhcp_mode" ] ] ,
			[ "dhcp_mode" , self.api.get_setting , [ self , "network" , "dhcp_mode" ] ] ,
			[ "current_ssid_name" , self.api.get_setting , [ self , "network" , "current_ssid_name" ] ] ,
			[ "ip_address" , self.api.get_setting , [ self , "network" , "ip_address" ] ] ,
			[ "wireless_access_points" , self.api.get_setting , [ self , "network" , "wireless_access_points" ] ] ,
			[ "current_access_point" , self.api.get_setting , [ self , "network" , "current_access_point" ] ] ,
			[ "current_access_point" , self.api.get_setting , [ self , "network" , "current_access_point" ] ] ,
			[ "forget_wifi_network" , self.api.get_setting , [ self , "network" , "forget_wifi_network" ] ] ,
			[ "manual_setup" , self.api.get_setting , [ self , "network" , "manual_setup" ] ] ,
			[ "manual_setup_info" , self.api.get_setting , [ self , "network" , "manual_setup_info" ] ] ,
			[ "hidden_network" , self.api.get_setting , [ self , "network" , "hidden_network" ] ] ,
			[ "hidden_network_info" , self.api.get_setting , [ self , "network" , "hidden_network_info" ] ] ,
			[ "test_connection" , self.api.get_setting , [ self , "network" , "test_connection" ] ] ,
			[ "start_ap_search" , self.api.get_setting , [ self , "network" , "start_ap_search" ] ] ,
			[ "stop_ap_search" , self.api.get_setting , [ self , "network" , "stop_ap_search" ] ] ,
			[ "set_wifi_password" , self.api.get_setting , [ self , "network" , "set_wifi_password" ] ] ,
		]
		result = _x_batch_process({
			"max_workers": 3 ,
			"batch_list": batch_list ,
		})
		return {
			"connection_type": result[ 0 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"connection_status": result[ 1 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"dhcp_mode": result[ 2 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"dhcp_mode": result[ 3 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"current_ssid_name": result[ 0 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"ip_address": result[ 4 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"wireless_access_points": result[ 5 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"current_access_point": result[ 6 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"current_access_point": result[ 7 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"forget_wifi_network": result[ 8 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"manual_setup": result[ 9 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"manual_setup_info": result[ 10 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"hidden_network": result[ 11 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"hidden_network_info": result[ 12 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"test_connection": result[ 13 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"start_ap_search": result[ 14 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"stop_ap_search": result[ 15 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"set_wifi_password": result[ 16 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
		}

	def get_channel_settings( self ):
		batch_list = [
			[ "auto_channel_scan" , self.api.get_setting , [ self , "channels" , "auto_channel_scan" ] ] ,
			[ "cancel_channel_scan" , self.api.get_setting , [ self , "channels" , "cancel_channel_scan" ] ] ,
			[ "analog" , self.api.get_setting , [ self , "channels" , "analog" ] ] ,
			[ "digital" , self.api.get_setting , [ self , "channels" , "digital" ] ] ,
			[ "percent_complete" , self.api.get_setting , [ self , "channels" , "percent_complete" ] ] ,
			[ "skip_channel" , self.api.get_setting , [ self , "channels" , "skip_channel" ] ] ,
			[ "analog_audio" , self.api.get_setting , [ self , "channels" , "analog_audio" ] ] ,
			[ "digital_language" , self.api.get_setting , [ self , "channels" , "digital_language" ] ] ,
			[ "parental_controls" , self.api.get_setting , [ self , "channels" , "parental_controls" ] ] ,
			[ "current_channel" , self.api.get_setting , [ self , "channels" , "current_channel" ] ] ,
		]
		result = _x_batch_process({
			"max_workers": 3 ,
			"batch_list": batch_list ,
		})
		return {
			"auto_channel_scan": result[ 0 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"cancel_channel_scan": result[ 1 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"analog": result[ 2 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"digital": result[ 3 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"percent_complete": result[ 4 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"skip_channel": result[ 5 ] ,
			"analog_audio": result[ 6 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"digital_language": result[ 7 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"parental_controls": result[ 8 ] ,
			"current_channel": result[ 9 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
		}


	def get_timer_settings( self ):
		batch_list = [
			[ "sleep_timer" , self.api.get_setting , [ self , "timers" , "sleep_timer" ] ] ,
			[ "auto_power_off_timer" , self.api.get_setting , [ self , "timers" , "auto_power_off_timer" ] ] ,
			[ "blank_screen" , self.api.get_setting , [ self , "timers" , "blank_screen" ] ] ,
		]
		result = _x_batch_process({
			"max_workers": 3 ,
			"batch_list": batch_list ,
		})
		return {
			"sleep_timer": result[ 0 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"auto_power_off_timer": result[ 1 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			# "auto_power_off_timer": result[ 1 ] ,
			"blank_screen": result[ 2 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
		}

	def get_closed_caption_settings( self ):
		batch_list = [
			[ "closed_captions_enabled" , self.api.get_setting , [ self , "closed_captions" , "closed_captions_enabled" ] ] ,
			[ "analog_closed_captions" , self.api.get_setting , [ self , "closed_captions" , "analog_closed_captions" ] ] ,
			[ "digital_closed_captions" , self.api.get_setting , [ self , "closed_captions" , "digital_closed_captions" ] ] ,
			[ "digital_style" , self.api.get_setting , [ self , "closed_captions" , "digital_style" ] ] ,
		]
		result = _x_batch_process({
			"max_workers": 3 ,
			"batch_list": batch_list ,
		})
		return {
			"closed_captions_enabled": result[ 0 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"analog_closed_captions": result[ 1 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"digital_closed_captions": result[ 2 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"digital_style": result[ 3 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
		}

	def get_device_settings( self ):
		batch_list = [
			[ "name_input" , self.api.get_setting , [ self , "devices" , "name_input" ] ] ,
			[ "hdmi1" , self.api.get_setting , [ self , "devices" , "hdmi1" ] ] ,
			[ "hdmi2" , self.api.get_setting , [ self , "devices" , "hdmi2" ] ] ,
			[ "comp" , self.api.get_setting , [ self , "devices" , "comp" ] ] ,
			[ "tuner" , self.api.get_setting , [ self , "devices" , "tuner" ] ] ,
			[ "current_input" , self.api.get_setting , [ self , "devices" , "current_input" ] ] ,
			[ "current_inputs" , self.api.get_setting , [ self , "devices" , "current_inputs" ] ] ,
		]
		result = _x_batch_process({
			"max_workers": 3 ,
			"batch_list": batch_list ,
		})
		return {
			"name_input": result[ 0 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"hdmi1": result[ 1 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"hdmi2": result[ 2 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"comp": result[ 3 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"tuner": result[ 4 ] ,
			"current_input": result[ 5 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"current_inputs": result[ 6 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
		}

	def get_system_settings( self ):
		batch_list = [
			[ "service_check" , self.api.get_setting , [ self , "system" , "service_check" ] ] ,
			[ "system_information" , self.api.get_setting , [ self , "system" , "system_information" ] ] ,
			[ "menu_language" , self.api.get_setting , [ self , "system" , "menu_language" ] ] ,
			[ "local_time_settings" , self.api.get_setting , [ self , "system" , "local_time_settings" ] ] ,
			[ "cec" , self.api.get_setting , [ self , "system" , "cec" ] ] ,
			[ "power_mode" , self.api.get_setting , [ self , "system" , "power_mode" ] ] ,
			[ "aspect_ratio" , self.api.get_setting , [ self , "system" , "aspect_ratio" ] ] ,
			[ "input_at_power_on" , self.api.get_setting , [ self , "system" , "input_at_power_on" ] ] ,
			[ "cast_name" , self.api.get_setting , [ self , "system" , "cast_name" ] ] ,
			[ "mobile_devices" , self.api.get_setting , [ self , "system" , "mobile_devices" ] ] ,
			[ "accessibility" , self.api.get_setting , [ self , "system" , "accessibility" ] ] ,
			[ "reset_and_admin" , self.api.get_setting , [ self , "system" , "reset_and_admin" ] ] ,
		]
		result = _x_batch_process({
			"max_workers": 3 ,
			"batch_list": batch_list ,
		})
		return {
			"service_check": result[ 0 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"system_information": result[ 1 ] ,
			"menu_language": result[ 2 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"local_time_settings": result[ 3 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"cec": result[ 4 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"power_mode": result[ 5 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"aspect_ratio": result[ 6 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"input_at_power_on": result[ 7 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"cast_name": result[ 8 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"mobile_devices": result[ 9 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"accessibility": result[ 10 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"reset_and_admin": result[ 11 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
		}

	def get_cast_settings( self ):
		batch_list = [
			[ "device_name" , self.api.get_setting , [ self , "cast" , "device_name" ] ] ,
			[ "session_device_id" , self.api.get_setting , [ self , "cast" , "session_device_id" ] ] ,
			[ "google_cast_id" , self.api.get_setting , [ self , "cast" , "google_cast_id" ] ] ,
			[ "google_cast_cd" , self.api.get_setting , [ self , "cast" , "google_cast_cd" ] ] ,
			[ "google_privacy_policy" , self.api.get_setting , [ self , "cast" , "google_privacy_policy" ] ] ,
			[ "tos_accepted" , self.api.get_setting , [ self , "cast" , "tos_accepted" ] ] ,
			[ "soft_ap_config" , self.api.get_setting , [ self , "cast" , "soft_ap_config" ] ] ,
			[ "start_soft_ap" , self.api.get_setting , [ self , "cast" , "start_soft_ap" ] ] ,
			[ "stop_soft_ap" , self.api.get_setting , [ self , "cast" , "stop_soft_ap" ] ] ,
			[ "soft_ap_status" , self.api.get_setting , [ self , "cast" , "soft_ap_status" ] ] ,
			[ "soft_ap_mode" , self.api.get_setting , [ self , "cast" , "soft_ap_mode" ] ] ,
			[ "state" , self.api.get_setting , [ self , "cast" , "state" ] ] ,
		]
		result = _x_batch_process({
			"max_workers": 3 ,
			"batch_list": batch_list ,
		})
		return {
			"device_name": result[ 0 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"session_device_id": result[ 1 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"google_cast_id": result[ 2 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"google_cast_cd": result[ 3 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"google_privacy_policy": result[ 4 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"tos_accepted": result[ 5 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"soft_ap_config": result[ 6 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"start_soft_ap": result[ 7 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"stop_soft_ap": result[ 8 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"soft_ap_status": result[ 9 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"soft_ap_mode": result[ 10 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
			"state": result[ 11 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
		}

	def get_all_settings( self ):
		# Top Level Settings Categories = [ picture , audio , network , timers , channels , closed_captions , devices , system , cast ]
		return {
			"picture": self.get_picture_settings() ,
			"audio": self.get_audio_settings() ,
			"network": self.get_network_settings() ,
			"timers": self.get_timer_settings() ,
			"channels": self.get_channel_settings() ,
			"closed_captions": self.get_closed_caption_settings() ,
			"devices": self.get_device_settings() ,
			"system": self.get_system_settings() ,
			"cast": self.get_cast_settings()
		}