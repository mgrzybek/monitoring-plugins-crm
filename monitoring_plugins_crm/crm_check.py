#! /usr/bin/env python
# -*- coding: utf-8 -*-

from pynagios import Plugin, make_option, Response, WARNING, CRITICAL, UNKNOWN

import xml.etree.ElementTree
import subprocess
import os

class CrmCheck(Plugin):
	offline_nodes = []
	online_nodes = []
	standby_nodes = []
	maintenance_nodes = []

	failed_resources = []
	running_resources = []

	perfdata = make_option("--perfdata", dest="perfdata", help="Add perfdata to the output message", type="choice", choices=[ "yes", "no"], default="no")
	nodes = make_option("--nodes", dest="nodes", help="Check nodes status", type="choice", choices=[ "yes", "no"], default="yes")
	resources = make_option("--resources", dest="resources", help="Check resources status", type="choice", choices=[ "yes", "no"], default="yes")

	## Performs a check,
	# Uses crmsh classes to get the status
	def doApiGet(self):
		cib_command = [ '/usr/sbin/crm_mon', '--as-xml' ]
		rs = subprocess.check_output(cib_command)
		xml_cib = xml.etree.ElementTree.fromstring(rs)

		if self.options.nodes == 'yes':
			for node in xml_cib.iter('node'):
				if node.get('online') != None:
					if node.get('online') == 'false':
						self.offline_nodes.append(node.get('name'))
					else:
						self.online_nodes.append(node.get('name'))
				if node.get('standby') != None:
					if node.get('standby') == 'true':
						self.standby_nodes.append(node.get('name'))
				if node.get('maintenance') != None:
					if node.get('maintenance') == 'true':
						self.maintenance_nodes.append(node.get('name'))

		if self.options.resources == 'yes':
			for resource in xml_cib.iter('resource'):
				if resource.get('failed') != None:
					if resource.get('failed') == 'true' and resource.get('failure_ignored') == 'false' or resource.get('orphaned') == 'true':
						self.failed_resources.append(resource.get('id'))
					else:
						self.running_resources.append(resource.get('id'))

	## Returns a response and perf data for this check
	# @return a Response object
	def check(self):
		try:
			if os.getuid() != 0:
				return Response(UNKNOWN, "Must be run as root")

			if self.options.nodes == 'no' and self.options.resources == 'no':
				return Response(UNKNOWN, "Nothing to monitor: nodes=no and resources=no")

			self.doApiGet()

			response = self.parseResult(len(self.failed_resources))

			if self.options.perfdata == 'yes':
				self.setPerformanceData(response)

			return response
		except Exception as e:
			return Response(UNKNOWN, "Error occurred: " + str(e))

	## Parses the result of the check
	# @param data unused
	# @return a Response object
	def parseResult(self, data=None):
		result = self.response_for_value(len(self.failed_resources))

		if self.options.nodes == 'yes':
			if len(self.offline_nodes) > 0:
				return Response(CRITICAL, "[ Nodes: %s online, %s offline, %s standby, %s maintenance ]" % ( len(self.online_nodes), len(self.offline_nodes), len(self.standby_nodes), len(self.maintenance_nodes) ) )

			result.message = "[ Nodes: %s online, %s offline, %s standby, %s maintenance ]" % ( len(self.online_nodes), len(self.offline_nodes), len(self.standby_nodes), len(self.maintenance_nodes) )

		if self.options.resources == 'yes':
			if result.message == None:
				result.message = ''

			result.message += "[ Resources: %s running, %s failed ]" % ( len(self.running_resources), len(self.failed_resources) )

		return result

	## Adds performance data to the monitoring result
	# @param result the result object to modify
	# @return the modified result
	def setPerformanceData(self, result):
		result.set_perf_data("offline_nodes", len(self.offline_nodes))
		result.set_perf_data("failed_resources", len(self.failed_resources))
		return result
