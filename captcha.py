# -*- coding: utf-8 -*-

'''
Created on Sep 24, 2013

@author: kamushadenes
'''
import deathbycaptcha
import time



class Captcha():

	def __init__(self):
		self.captchasystem="deathbycaptcha"
		self.method="SocketClient"
		self.report_incorrect_captcha=True
		self.username="YOUR_USERNAME"
		self.password="YOUR_PASSWORD"

	def auth(self,username,password):
		print('[*] Captcha: Trying ' + self.method + ' method...')
		while True:
			try:
				if self.method == 'SocketClient':
					return deathbycaptcha.SocketClient(username, password)
				else:
					return deathbycaptcha.HttpClient(username, password)
			except Exception as e:
				print(str(e))
				if self.method == 'SocketClient':
					self.newmethod = 'HttpClient'
				elif self.method == 'HttpClient':
				   self.newmethod = 'SocketClient'
				print('[*] Captcha: Method ' + self.method + ' failed, trying ' + self.newmethod + ' ...')
				self.method = self.newmethod
	
	def report(self, captcha):
		if self.report_incorrect_captcha:
			self.client = self.auth(self.username,self.password)
			print('\n[*] Reporting incorrectly solved captcha, if this is happening too often, consider disabling it to prevent ban...')
			return self.client.report(captcha)
		

	def decode(self, filepath, timeout):
		ecount=0
		while True:
			
			print('[*] Captcha: using ' + self.captchasystem)
			self.client = self.auth(self.username,self.password)
			try:
				print('[*] Captcha: current balance: ' + str(self.client.get_balance()))
				print('[*] Cracking captcha...')
				return self.client.decode(filepath, timeout)
			except Exception as e:
				print(str(e))
				ecount+=1
				if ecount == 3:
					print('\n[!] Too many errors, giving up...')
					time.sleep(2)
					raise Exception('Unrecoverable error in captcha system')
				else:
					if self.method == 'SocketClient':
						self.newmethod = 'HttpClient'
					elif self.method == 'HttpClient':
				   		self.newmethod = 'SocketClient'
					print('\n[!] Captcha: Method ' + self.method + ' failed, trying ' + self.newmethod + ' (%d/3) ...\n' % ecount)
					self.method = self.newmethod
