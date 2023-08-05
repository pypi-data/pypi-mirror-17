# | Copyright 2012-2016 Karlsruhe Institute of Technology
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

import shlex
from grid_control import utils
from grid_control.config import ConfigError, noDefault
from grid_control.utils.parsing import parseDict, split_advanced, split_brackets
from python_compat import imap, irange, lmap, lzip

def parseTuple(t, delimeter):
	t = t.strip()
	if t.startswith('('):
		return tuple(imap(str.strip, split_advanced(t[1:-1], lambda tok: tok == delimeter, lambda tok: False)))
	return (t,)


def frange(start, end = None, num = None, steps = None, format = '%g'):
	if (end is None) and (num is None):
		raise ConfigError('frange: No exit condition!')
	if (end is not None) and (num is not None) and (steps is not None):
		raise ConfigError('frange: Overdetermined parameters!')
	if (end is not None) and (num is not None) and (steps is None):
		steps = float(end - start) / (num - 1)
	if (end is not None) and (num is None):
		steps = steps or 1
		num = int(1 + (end - start) / steps)
	return lmap(lambda x: format % x, imap(lambda i: start + (steps or 1) * i, irange(num)))


def parseParameterOption(option):
	# first token is variable / tuple - rest is option specifier: "a option" or "(a,b) option"
	tokens = list(split_brackets(option.lower()))
	if len(tokens) and '(' in tokens[0]:
		# parse tuple in as general way as possible
		def validChar(c):
			return c.isalnum() or (c in ['_'])
		result = [tuple(utils.accumulate(tokens[0], '', lambda i, b: not validChar(i), lambda i, b: validChar(i)))]
		if tokens[1:]:
			result.append(str.join('', tokens[1:]).strip())
	else:
		result = str.join('', tokens).strip().split(' ', 1)
	if len(result) == 1:
		result.append(None)
	return tuple(result)


def parseParameterOptions(options):
	(varDict, optDict) = ({}, {})
	for rawOpt in options:
		var, opt = parseParameterOption(rawOpt)
		optDict[(var, opt)] = rawOpt
		if opt is None:
			if isinstance(var, tuple):
				for sk in var:
					varDict[sk] = var
			else:
				varDict[var] = var
	return (varDict, optDict)


class ParameterConfig:
	def __init__(self, config):
		(self._config, self._changes) = (config, [])
		(self._varDict, self._optDict) = parseParameterOptions(config.getOptions())


	def _parseParameter(self, varName, value, ptype):
		if ptype == 'verbatim':
			return [value]
		elif ptype == 'split':
			delimeter = self.get(self._getParameterOption(varName), 'delimeter', ',')
			return lmap(str.strip, value.split(delimeter))
		elif ptype == 'lines':
			return value.splitlines()
		elif ptype in ('expr', 'eval'):
			result = eval(value) # pylint:disable=eval-used
			if isinstance(result, (list, type(range(1)))):
				return list(result)
			return [result]
		elif ptype == 'default':
			return shlex.split(value)
		elif ptype == 'format':
			fsource = self.get(self._getParameterOption(varName), 'source')
			fdefault = self.get(self._getParameterOption(varName), 'default', '')
			return (ptype, varName, value, fsource, fdefault)
		raise ConfigError('[Variable: %s] Invalid parameter type: %s' % (varName, ptype))


	def _parseParameterTuple(self, varName, tupleValue, tupleType, varType, varIndex):
		if tupleType == 'tuple':
			tupleDelimeter = self.get(self._getParameterOption(varName), 'delimeter', ',')
			tupleStrings = lmap(str.strip, split_advanced(tupleValue, lambda tok: tok in ' \n', lambda tok: False))
			tupleList = lmap(lambda t: parseTuple(t, tupleDelimeter), tupleStrings)
		elif tupleType == 'binning':
			tupleList = lzip(tupleValue.split(), tupleValue.split()[1:])

		result = []
		for tupleEntry in tupleList:
			try:
				tmp = self._parseParameter(varName, tupleEntry[varIndex], varType)
			except Exception:
				raise ConfigError('Unable to parse %r' % repr((tupleEntry, tupleStrings)))
			if isinstance(tmp, list):
				if len(tmp) != 1:
					raise ConfigError('[Variable: %s] Tuple entry (%s) expands to multiple variable entries (%s)!' % (varName, tupleEntry[varIndex], tmp))
				result.append(tmp[0])
			else:
				result.append(tmp)
		return result


	def _onChange(self, config, old_obj, cur_obj, cur_entry, obj2str):
		self._changes.append((old_obj, cur_obj, cur_entry, obj2str))
		return cur_obj


	def _getOpt(self, var, opt = None):
		return self._optDict.get((var, opt), ('%s %s' % (var, opt or '')).replace('\'', ''))


	def _getParameterOption(self, varName):
		try:
			return self._varDict[varName.lower()]
		except Exception:
			raise ConfigError('Variable %s is undefined' % varName)


	def _parseDict(self, varName, value, valueParser):
		keyTupleDelimeter = self.get(self._getParameterOption(varName), 'key delimeter', ',')
		return parseDict(value, valueParser, lambda k: parseTuple(k, keyTupleDelimeter))


	def _processParameterList(self, varName, values):
		if isinstance(values, tuple):
			return values
		result = list(values)
		for idx, value in enumerate(values):
			valueRepeat = int(self.get(varName, 'repeat idx %d' % idx, '1'))
			assert(valueRepeat >= 0)
			if valueRepeat > 1:
				result.extend((valueRepeat - 1) * [value])
		paramRepeat = int(self.get(varName, 'repeat', '1'))
		return paramRepeat * result


	def showChanges(self):
		pass


	def getConfig(self, *args, **kwargs):
		return self._config.changeView(*args, **kwargs)


	def get(self, var, opt = None, default = noDefault):
		return self._config.get(self._getOpt(var, opt), default, onChange = self._onChange)


	def getBool(self, var, opt = None, default = noDefault):
		return self._config.getBool(self._getOpt(var, opt), default, onChange = self._onChange)


	def getParameter(self, varName):
		optKey = self._getParameterOption(varName)

		if isinstance(optKey, tuple):
			varIndex = list(optKey).index(varName.lower())
			tupleValue = self.get(optKey, None, '')
			tupleType = self.get(optKey, 'type', 'tuple')
			varType = self.get(varName, 'type', 'verbatim')

			if '=>' in tupleValue:
				if self.getBool(optKey, 'parse dict', True):
					return self._parseDict(varName, tupleValue,
						lambda v: self._processParameterList(varName, self._parseParameterTuple(varName, v, tupleType, varType, varIndex)))
			return self._processParameterList(varName, self._parseParameterTuple(varName, tupleValue, tupleType, varType, varIndex))

		else:
			varValue = self.get(optKey, None, '')
			varType = self.get(varName, 'type', 'default')

			if '=>' in varValue:
				if self.getBool(optKey, 'parse dict', True):
					return self._parseDict(varName, varValue,
						lambda v: self._processParameterList(varName, self._parseParameter(varName, v, varType)))
			return self._processParameterList(varName, self._parseParameter(varName, varValue, varType))
