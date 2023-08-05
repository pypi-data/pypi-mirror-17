#!/usr/bin/python
# -*- coding: utf-8 -*-
##
## @author Edouard DUPIN
##
## @copyright 2012, Edouard DUPIN, all right reserved
##
## @license APACHE v2.0 (see license file)
##

from lutin import debug
from lutin import system
from lutin import tools
import os

class System(system.System):
	def __init__(self, target):
		system.System.__init__(self)
		# create some HELP:
		self.help = "X11: Basic interface of Linux Graphic interface"
		self.valid = True
		# no check needed ==> just add this:
		self.add_module_depend(['c'])
		
		self.add_header_file([
		    "/usr/include/X11/*"
		    ],
		    destination_path="X11",
		    recursive=True)
		
		self.add_export_flag('link-lib', 'X11')


