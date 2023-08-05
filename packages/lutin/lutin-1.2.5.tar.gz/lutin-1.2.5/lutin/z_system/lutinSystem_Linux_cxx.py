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
from lutin import multiprocess
import os

class System(system.System):
	def __init__(self, target):
		system.System.__init__(self)
		# create some HELP:
		self.help = "CXX: Generic C++ library"
		self.valid = True
		# no check needed ==> just add this:
		self.add_module_depend([
		    'c',
		    'm',
		    'pthread'
		    ])
		self.add_export_flag("c++", "-D__STDCPP_GNU__")
		#self.add_export_flag("c++-remove", "-nostdlib")
		#self.add_export_flag("need-libstdc++", True)
		self.add_export_flag("link-lib", "stdc++")
		
		compilator_gcc = "g++"
		if target.config["compilator-version"] != "":
			compilator_gcc = compilator_gcc + "-" + target.config["compilator-version"]
		
		#get g++ compilation version :
		version_cpp = multiprocess.run_command_direct(compilator_gcc + " -dumpversion");
		if version_cpp == False:
			debug.error("Can not get the g++ version ...")
		
		self.add_header_file([
		    "/usr/include/c++/" + version_cpp + "/*"
		    ],
		    recursive=True)


