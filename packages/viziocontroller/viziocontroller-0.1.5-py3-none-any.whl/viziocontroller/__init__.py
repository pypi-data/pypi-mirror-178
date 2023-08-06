#!/usr/bin/env python3

# Based on https://github.com/vkorn/pyvizio

from .discover import Discover
from .api import API
from .settings import Settings
from pprint import pprint
import sys
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from wakeonlan import send_magic_packet

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

class VizioController:

	def __init__( self , options={} ):
		self.options = options
		if "mac_address" not in options:
			print("you have to send the mac adress of the tv")
			sys.exit( 1 )
		if "ip" not in options:
			self.discover = Discover( options )
			self.ip = self.discover.find_tv()
			options["ip"] = self.ip
			print( "IP == " )
			print( options["ip"] )
		else:
			self.ip = options["ip"]
		if "request_token" in options:
			if "code_displayed_on_tv" in options:
				self.api = API(options)
				options["access_token"] = self.api.pairing_stage_2( self.ip , options["request_token"] , options["code_displayed_on_tv"] )
				print( "access_token == " )
				print( str( options["access_token"] ) )
				sys.exit( 1 )
		if "access_token" not in options:
			self.api = API(options)
			request_token = self.api.pairing_stage_1( self.ip )
			print( "request_token ==" )
			print( str( request_token ) )
			print( f"Ok , now rerun this and set request_token and code_displayed_on_tv" )
			sys.exit( 1 )
		if "always_wakeup" in options:
			if options[ "always_wakeup" ] == True:
				send_magic_packet( self.options[ "mac_address" ] )

		self.api = API( options )
		self.settings = Settings( options )
		# print( "Retrieving Current Settings" )
		# self.current_volume = self.api.get_volume()
		# self.audio_settings = self.api.get_audio_settings()
		# self.audio_settings_options = self.api.get_all_audio_settings_options()
		# self.current_input = self.api.get_current_input()
		# self.available_inputs = self.api.get_available_inputs()
		# self.current_app = self.api.get_current_app()
		# self.settings_types = self.api.get_settings_types()
		# self.settings = {}
		# for index , setting in enumerate( self.settings_types["ITEMS"] ):
		# 	options = self.api.get_all_settings_for_type( setting["CNAME"] )
		# 	options = [ x["CNAME"] for x in options["ITEMS"] ]
		# 	self.settings[setting["CNAME"]] = {}
		# 	for option_index , option in enumerate( options ):
		# 		self.settings[setting["CNAME"]][ option ] = self.api.get_setting( setting["CNAME"] , option )
		# pprint( self.settings )
		# print( f"IP == {self.ip}" )

	def get_status( self ):
		try:
			batch_list = [
				[ "power_state" , self.api.get_power_state ] ,
				[ "volume" , self.api.get_volume ] ,
				[ "input" , self.api.get_current_input ] ,
				[ "app" , self.api.get_current_app ] ,
			]
			result = _x_batch_process({
				"max_workers": 3 ,
				"batch_list": batch_list ,
			})
			return {
				"power": result[ 0 ][ "ITEMS" ][ 0 ][ "VALUE" ] ,
				"volume": result[ 1 ] ,
				"input": result[ 2 ][ "name" ] ,
				"app": result[ 3 ][ "ITEM" ][ "VALUE" ][ "APP_ID" ] ,
			}
		except Exception as e:
			print( e )
			return "API SERVER OFFLINE"

	def set_volume( self , target_level ):
		current_volume = self.api.get_volume()
		volume_difference = ( current_volume - target_level )
		volume_difference_absolute = abs( volume_difference )
		print( f"Current Volume === {current_volume}" )
		print( f"Difference to Target [{target_level}] === {volume_difference_absolute}" )
		if current_volume > target_level:
			for i in range( 0 , volume_difference ):
				self.api.volume_down()
				print( f"Current Volume === {self.api.get_volume()}" )
		elif current_volume < target_level:
			for i in range( 0 , volume_difference_absolute ):
				self.api.volume_up()
				print( f"Current Volume === {self.api.get_volume()}" )
