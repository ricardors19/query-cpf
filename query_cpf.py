# -*- coding: utf-8 -*-
"""
Simple script to get the citzen name by its CPF (Brazil's SSN)
"""
from browser import Browser
from captcha import Captcha
import time
import os

class CPF():

	def clear(self):
		os.system('cls' if os.name=='nt' else 'clear')
		
	def CPF(self,cpf=''):

		if cpf == '':
			cpf  = str(raw_input('[?] CPF: ')).strip('.').strip(' ').strip('/').strip('-')
			print('\n')
			self.api=False
		else:
			self.api=True
		
		ecount=0
		while True:
			session = Browser()
			url = 'http://www.receita.fazenda.gov.br/aplicacoes/atcta/cpf/ConsultaPublica.asp'
			url2 = 'http://www.receita.fazenda.gov.br/aplicacoes/atcta/cpf/ConsultaPublicaExibir.asp'
						
			if not self.api:
				print('[*] Connecting...')
				
			response = 	session.get_response(url)
			element = session.get_bs(response.content)
			
			if not self.api:
				print('[*] Searching for captcha image...')
			image_url = 'http://www.receita.fazenda.gov.br' + element.find('img',{'id':'imgcaptcha'})['src']
			viewstate = 'http://www.receita.fazenda.gov.br' + element.find('input',{'id':'viewstate'})['value']
			
			if not self.api:
				print('[*] Downloading captcha image...')
			
			captchac = Captcha()
	
			imgfile = session.download(image_url,'/tmp/.rcaptcha.jpg')
	
			try:
				captcha = captchac.decode(imgfile, 30)
			except Exception,e:
				if not self.api:
					print('[!] Unrecoverable error in captcha system: %s' % str(e))
					time.sleep(2)
				raise Exception('[!] Unrecoverable error in captcha system: %s' % str(e))
			
			if captcha:
				if not self.api:
					print("[*] Captcha cracked: " + captcha["text"] + '\n')
			try:
				
				dados = {'txtCpf':cpf,'captcha': captcha["text"],'viewstate':viewstate}
				response = session.post_response(url2, dados)
								
				if u'Os caracteres da imagem não foram preenchidos corretamente' in response.content.decode("iso-8859-1", "replace"):
					raise Exception('Wrong captcha')
				element = session.get_bs(response.content)				
				data = element.findAll('span',{'class':'clConteudoDados'})				
				rcpf = str(data[0]).split(':')[1].split('<')[0].strip()
				rnome = str(data[1]).split(':')[1].split('<')[0].strip()
				rsituacao = str(data[2]).split(':')[1].split('<')[0].strip()
				rdv = str(data[3]).split(':')[1].split('<')[0].strip()
				if not self.api:
					print('[+] CPF: %s' % rcpf)
					print('[+] Nome: %s' % rnome)
					print('[+] Situacao cadastral: %s' % rsituacao)
					print('[+] Digito verificador: %s' % rdv)
					raw_input()
				else:
					rdict = {'CPF': rcpf, 'Nome': rnome, 'Situacao cadastral': rsituacao, 'Digito Verificador': rdv}
					return rdict
				break
			
			except Exception as e:
				if e == 'Wrong captcha':
					captchac.report(captcha["captcha"])
				if ecount == 3:
					if not self.api:
						print("[!] Max attempts reached, giving up (maybe the CPF was incorrect?) ...")
					raise Exception("[!] Max attempts reached, giving up (maybe the CPF was incorrect?) ...")
					break	
				else:
					ecount+=1
					if not self.api:
						print('\n[!] Error: %s\n[*] Trying again... (%d/3)\n' % (str(e), ecount))
					

	def determineValue(self,value):
		import re
		cpf = re.match( r'(\d{3}[ .]?\d{3}[ .]?\d{3}[ /.-]?\d{2})', value)
		if cpf:
			return 'CPF'
		else:
			cnpj = re.match( r'(\d{2}[ .]?\d{3}[ .]?\d{3}[ /]?\d{4}[ -]?\d{2})', value)
			if cnpj:
				return 'CNPJ'

	def run(self,value=''):
		if value == '':
			while True:
				self.clear()
				print('[*] Query Receita Federal\n')
				print('1 - CPF')
				print('0 - Exit')
				option = int(input('\n[?] Select your option: '))
				print('\n')
				if option == 1:
					self.CPF()
				elif option == 0:
					break
		else:
			vtype = self.determineValue(value)
			if vtype == 'CPF':
				self.CPF(value)

query_receita = CPF()
query_receita.run()
