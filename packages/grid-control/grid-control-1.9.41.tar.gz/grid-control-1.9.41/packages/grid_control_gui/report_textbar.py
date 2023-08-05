# | Copyright 2014-2016 Karlsruhe Institute of Technology
# |
# | Licensed under the Apache License, Version 2.0 (the "License");
# | you may not use this file except in compliance with the License.
# | You may obtain a copy of the License at
# |
# |     http://www.apache.org/licenses/LICENSE-2.0
# |
# | Unless required by applicable law or agreed to in writing, software
# | distributed under the License is distributed on an "AS IS" BASIS,
# | WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# | See the License for the specific language governing permissions and
# | limitations under the License.

import sys
from grid_control.job_db import JobClass
from grid_control.job_selector import ClassSelector
from grid_control.report import Report

class BasicProgressBar(object):
	def __init__(self, minValue = 0, maxValue = 100, totalWidth = 16):
		(self._min, self._max, self._width) = (minValue, maxValue, totalWidth)
		self.update(0)

	def update(self, newProgress = 0):
		# Compute variables
		complete = self._width - 2
		progress = max(self._min, min(self._max, newProgress))
		done = int(round(((progress - self._min) / max(1.0, float(self._max - self._min))) * 100.0))
		blocks = int(round((done / 100.0) * complete))

		# Build progress bar
		if blocks == 0:
			self._bar = '[>%s]' % (' '*(complete-1))
		elif blocks == complete:
			self._bar = '[%s]' % ('='*complete)
		else:
			self._bar = '[%s>%s]' % ('='*(blocks-1), ' '*(complete-blocks))

		# Print percentage
		text = str(done) + '%'
		textPos = int((self._width - len(text) + 1) / 2)
		self._bar = self._bar[0:textPos] + text + self._bar[textPos+len(text):]

	def __str__(self):
		return str(self._bar)


class BarReport(Report):
	alias = ['bar']

	def __init__(self, jobDB, task, jobs = None, configString = ''):
		Report.__init__(self, jobDB, task, jobs, configString)
		self._bar = BasicProgressBar(0, len(jobDB), 65)

	def getHeight(self):
		return 1

	def display(self):
		self._bar.update(len(self._jobDB.getJobs(ClassSelector(JobClass.SUCCESS))))
		sys.stdout.write(str(self._bar) + '\n')
