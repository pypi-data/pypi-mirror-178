#!./runmodule.sh

'''
This module defines the ConfigFile class
which can be used to load and save config files.
'''

import os
import shlex
import enum
import typing
from collections.abc import Iterable, Iterator, Sequence, Callable

import appdirs

from .config import Config, DictConfig, MultiConfig, ConfigId


def readable_quote(value: str) -> str:
	'''
	This function has the same goal like :func:`shlex.quote` but tries to generate better readable output.

	:param value: A value which is intended to be used as a command line argument
	:return: A POSIX compliant quoted version of :obj:`value`
	'''
	out = shlex.quote(value)
	if out == value:
		return out

	if '"\'"' in out and '"' not in value:
		return '"' + value + '"'

	return out


@enum.unique
class NotificationLevel(enum.Enum):
	INFO = 'info'
	ERROR = 'error'

UiCallback: 'typing.TypeAlias' = 'Callable[[NotificationLevel, str|BaseException], None]'

class UiNotifier:

	def __init__(self, show: UiCallback) -> None:
		self.show = show

	def show_info(self, msg: str) -> None:
		self.show(NotificationLevel.INFO, msg)

	def show_error(self, msg: 'str|BaseException') -> None:
		self.show(NotificationLevel.ERROR, msg)


class ParseException(Exception):

	'''
	This is raised and caught inside of :class:`ConfigFile` to communicate errors while parsing a config file.
	If you don't intend to subclass :class:`ConfigFile` you do not need to worry about this class.
	'''

class MultipleParseExceptions(Exception):

	'''
	This is raised and caught inside of :class:`ConfigFile` to communicate errors while parsing a config file where multiple settings are set in the same line.
	If you don't intend to subclass :class:`ConfigFile` you do not need to worry about this class.
	'''

	def __init__(self, exceptions: 'Sequence[ParseException]') -> None:
		super().__init__()
		self.exceptions = exceptions

	def __iter__(self) -> 'Iterator[ParseException]':
		return iter(self.exceptions)

class ConfigFile:

	'''
	Read or write a config file.
	'''

	FILENAME = 'config'

	COMMENT = '#'
	COMMENT_PREFIXES = ('"', '#')
	ENTER_GROUP_PREFIX = '['
	ENTER_GROUP_SUFFIX = ']'
	KEY_VAL_SEP = '='

	SET = ('set',)
	INCLUDE = ('include',)

	primitive_types = {str, int, bool, float}


	def __init__(self, ui_callback: UiCallback, *,
		appname: str,
		authorname: 'str|None' = None,
		config_instances: 'dict[str, Config[typing.Any]]' = Config.instances,
	) -> None:
		'''
		:param ui_callback: A function to display messages to the user
		:param appname: The name of the application, required for generating the path of the config file if you use :meth:`load` or :meth:`save`
		:param authorname: The name of the developer of the application, on MS Windows useful for generating the path of the config file if you use :meth:`load` or :meth:`save`
		:param config_instances: The Config instances to load or save
		'''
		self.appname = appname
		self.authorname = authorname
		self.ui_notifier = UiNotifier(ui_callback)
		self.config_instances = config_instances

	def get_app_dirs(self) -> 'appdirs.AppDirs':
		'''
		Create or get a cached `AppDirs <https://github.com/ActiveState/appdirs/blob/master/README.rst#appdirs-for-convenience>`_ instance with multipath support enabled.

		When creating a new instance, `platformdirs <https://pypi.org/project/platformdirs/>`_, `xdgappdirs <https://pypi.org/project/xdgappdirs/>`_ and `appdirs <https://pypi.org/project/appdirs/>`_ are tried, in that order.
		The first one installed is used.
		appdirs, the original of the two forks and the only one of the three with type stubs, is specified in pyproject.toml as a hard dependency so that at least one of the three should always be available.
		I am not very familiar with the differences but if a user finds that appdirs does not work for them they can choose to use an alternative with ``pipx inject appname xdgappdirs|platformdirs``.
		'''
		if not hasattr(self, '_appdirs'):
			try:
				import platformdirs  # type: ignore [import]  # this library is not typed and not necessarily installed, I am relying on it's compatibility with appdirs
				AppDirs = typing.cast('type[appdirs.AppDirs]', platformdirs.PlatformDirs)
			except ImportError:
				try:
					import xdgappdirs  # type: ignore [import]  # this library is not typed and not necessarily installed, I am relying on it's compatibility with appdirs
					AppDirs = typing.cast('type[appdirs.AppDirs]', xdgappdirs.AppDirs)
				except ImportError:
					AppDirs = appdirs.AppDirs

			self._appdirs = AppDirs(self.appname, self.authorname, multipath=True)

		return self._appdirs

	# ------- load -------

	def iter_user_site_config_paths(self) -> 'Iterator[str]':
		'''
		Iterate over all directories which are searched for config files.
		'''
		appdirs = self.get_app_dirs()
		yield from appdirs.user_config_dir.split(os.path.pathsep)
		yield from appdirs.site_config_dir.split(os.path.pathsep)

	def iter_config_paths(self) -> 'Iterator[str]':
		'''
		Iterate over all paths which are checked for config files, user specific first.

		Use this method if you want to tell the user where the application is looking for it's config file.
		The first existing file yielded by this method is used by :meth:`load`.
		The paths are based on :meth:`get_app_dirs`.
		'''
		for path in self.iter_user_site_config_paths():
			yield os.path.join(path, self.FILENAME)

	def load(self) -> None:
		'''
		Load the first existing config file returned by :meth:`iter_config_paths`.

		If there are several config files a user specific config file is preferred.
		If a user wants a system wide config file to be loaded, too, they can explicitly include it in their config file.
		'''
		for fn in self.iter_config_paths():
			if os.path.isfile(fn):
				self.load_file(fn)
				return

	def load_file(self, fn: str) -> None:
		'''
		Load a config file and change the :class:`Config` objects accordingly.
		Errors are communicated via :attr:`ui_notifier`.

		:param fn: The file name of the config file (absolute or relative path)
		'''
		self.config_id: 'ConfigId|None' = None
		self.load_without_resetting_config_id(fn)

	def load_without_resetting_config_id(self, fn: str) -> None:
		with open(fn, 'rt') as f:
			for lnno, ln in enumerate(f, 1):
				self.parse_line(ln, lnno, f.name)

	def parse_line(self, ln: str, lnno: 'int|None' = None, fn: 'str|None' = None) -> None:
		'''
		:param ln: The line to be parsed
		:param lnno: The number of the line, used in error messages
		:param fn: The name of the file from which ln was read (absolute or relative path), used in error messages and for relative imports

		`lnno` and `fn` are allowed to be None in case `ln` is not read from a config file but from a command line.

		:meth:`parse_error` is called if something goes wrong, e.g. invalid key or invalid value.
		'''
		ln = ln.strip()
		if not ln:
			return
		if self.is_comment(ln):
			return
		if self.enter_group(ln):
			return

		ln_splitted = shlex.split(ln, comments=True)
		self.parse_splitted_line(ln_splitted, ln, lnno, fn)

	def enter_group(self, ln: str) -> bool:
		'''
		Check if `ln` starts a new group and set :attr:`config_id` if it does.

		:param ln: The current line
		:return: `True` if `ln` starts a new group
		'''
		if ln.startswith(self.ENTER_GROUP_PREFIX) and ln.endswith(self.ENTER_GROUP_SUFFIX):
			self.config_id = typing.cast(ConfigId, ln[len(self.ENTER_GROUP_PREFIX):-len(self.ENTER_GROUP_SUFFIX)])
			return True
		return False

	def parse_splitted_line(self, ln_splitted: 'Sequence[str]', ln: str, lnno: 'int|None' = None, fn: 'str|None' = None) -> None:
		cmd = ln_splitted[0]

		try:
			if cmd in self.SET:
				self.set(ln_splitted)
			elif cmd in self.INCLUDE:
				self.include(fn, ln_splitted)
			else:
				self.unknown_command(ln_splitted, ln, lnno, fn)
		except ParseException as e:
			self.parse_error(str(e), ln, lnno)
		except MultipleParseExceptions as exceptions:
			for exc in exceptions:
				self.parse_error(str(exc), ln, lnno)

	def is_comment(self, ln: str) -> bool:
		'''
		Check if `ln` is a comment.

		:param ln: The current line
		:return: `True` if `ln` is a comment
		'''
		for c in self.COMMENT_PREFIXES:
			if ln.startswith(c):
				return True
		return False


	def set(self, cmd: 'Sequence[str]') -> None:
		if len(cmd) < 2:
			raise ParseException('no settings given')

		if self.KEY_VAL_SEP in cmd[1]:  # cmd[0] is the name of the command, cmd[1] is the first argument
			self.set_multiple(cmd)
		else:
			self.set_with_spaces(cmd)

	def set_with_spaces(self, cmd: 'Sequence[str]') -> None:
		n = len(cmd)
		if n == 3:
			cmdname, key, value = cmd
			self.parse_key_and_set_value(key, value)
		elif n == 4:
			cmdname, key, sep, value = cmd
			if sep != self.KEY_VAL_SEP:
				raise ParseException(f'seperator between key and value should be {self.KEY_VAL_SEP}, not {sep!r}')
			self.parse_key_and_set_value(key, value)
		elif n == 2:
			raise ParseException(f'missing value or missing {self.KEY_VAL_SEP}')
		else:
			assert n >= 5
			raise ParseException(f'too many arguments given or missing {self.KEY_VAL_SEP} in first argument')

	def set_multiple(self, cmd: 'Sequence[str]') -> None:
		exceptions = []
		for arg in cmd[1:]:
			if not self.KEY_VAL_SEP in arg:
				raise ParseException(f'missing {self.KEY_VAL_SEP} in {arg!r}')
			key, value = arg.split(self.KEY_VAL_SEP, 1)
			try:
				self.parse_key_and_set_value(key, value)
			except ParseException as e:
				exceptions.append(e)
		if exceptions:
			raise MultipleParseExceptions(exceptions)

	def parse_key_and_set_value(self, key: str, value: str) -> None:
		if key not in self.config_instances:
			raise ParseException(f'invalid key {key!r}')

		instance = self.config_instances[key]
		try:
			self.parse_and_set_value(instance, value)
		except ValueError as e:
			raise ParseException(str(e))

	def parse_and_set_value(self, instance: Config[typing.Any], value: str) -> None:
		instance.parse_and_set_value(self.config_id, value)


	def include(self, fn: 'str|None', cmd: 'Sequence[str]') -> None:
		if len(cmd) != 2:
			raise ParseException('invalid number of arguments, expected exactly one: the file to include')

		fn_imp = cmd[1]
		fn_imp = os.path.expanduser(fn_imp)
		if fn and not os.path.isabs(fn_imp):
			fn_imp = os.path.join(os.path.split(os.path.abspath(fn))[0], fn_imp)

		if os.path.isfile(fn_imp):
			self.load_without_resetting_config_id(fn_imp)
		else:
			raise ParseException(f'no such file {fn_imp!r}')


	def unknown_command(self, ln_splitted: 'Sequence[str]', ln: str, lnno: 'int|None', fn: 'str|None') -> 'typing.NoReturn|None':

		raise ParseException('unkown command %r' % ln_splitted[0])


	# ------- save -------

	def save(self,
		config_instances: 'Iterable[Config[typing.Any] | DictConfig[typing.Any, typing.Any]] | None' = None, *,
		ignore: 'Iterable[Config[typing.Any] | DictConfig[typing.Any, typing.Any]] | None' = None,
		no_multi: bool = False,
		comments: bool = True,
	) -> str:
		'''
		Save the current values of all settings to the first existing and writable file returned by :meth:`iter_config_paths` or to the first path if none of the files are existing and writable.

		:param config_instances: Do not save all settings but only those given. If this is a :class:`list` they are written in the given order. If this is a :class:`set` they are sorted by their keys.
		:param ignore: Do not write these settings to the file.
		:param no_multi: Do not write several sections. For :class:`MultiConfig` instances write the default values only.
		:param comments: Write comments with allowed values and help.
		:return: The path to the file which has been written
		'''
		paths = tuple(self.iter_config_paths())
		for fn in paths:
			if os.path.isfile(fn) and os.access(fn, os.W_OK):
				break
		else:
			fn = paths[0]
		self.save_file(fn, config_instances=config_instances, ignore=ignore, no_multi=no_multi, comments=comments)
		return fn

	def save_file(self,
		fn: str,
		config_instances: 'Iterable[Config[typing.Any] | DictConfig[typing.Any, typing.Any]] | None' = None, *,
		ignore: 'Iterable[Config[typing.Any] | DictConfig[typing.Any, typing.Any]] | None' = None,
		no_multi: bool = False,
		comments: bool = True,
	) -> None:
		'''
		Save the current values of all settings to a specific file.

		:param fn: The name of the file to write to (absolute or relative path)

		For an explanation of the other parameters see :meth:`save`.
		'''
		with open(fn, 'wt') as f:
			self.save_to_open_file(f, config_instances, ignore=ignore, no_multi=no_multi, comments=comments)


	def save_to_open_file(self,
		f: typing.TextIO,
		config_instances: 'Iterable[Config[typing.Any] | DictConfig[typing.Any, typing.Any]] | None' = None, *,
		ignore: 'Iterable[Config[typing.Any] | DictConfig[typing.Any, typing.Any]] | None' = None,
		no_multi: bool = False,
		comments: bool = True,
	) -> None:
		'''
		Save the current values of all settings to file-like object.

		:param f: The file to write to

		For an explanation of the other parameters see :meth:`save`.
		'''
		self.last_name: 'str|None' = None
		config_keys: 'Iterable[str]'
		if config_instances is None:
			config_keys = self.config_instances.keys()
			config_keys = sorted(config_keys)
		else:
			config_keys = []
			for c in config_instances:
				if isinstance(c, DictConfig):
					config_keys.extend(sorted(c.iter_keys()))
				else:
					config_keys.append(c.key)
			if not isinstance(config_instances, (list, tuple)):
				config_keys = sorted(config_keys)

		if ignore is not None:
			tmp = set()
			for c in tuple(ignore):
				if isinstance(c, DictConfig):
					tmp |= set(c._values.values())
				else:
					tmp.add(c)
			ignore = tmp

		if comments:
			self.write_data_types(f, config_keys, ignore)

		multi_config_keys = []
		for key in config_keys:
			instance = self.config_instances[key]
			if not instance.wants_to_be_exported():
				continue

			if ignore is not None and instance in ignore:
				continue

			if not no_multi and isinstance(instance, MultiConfig):
				multi_config_keys.append(key)
				continue

			if comments:
				self.write_help(f, instance)
			value = self.format_value(instance, None)
			value = readable_quote(value)
			ln = f'{self.SET[0]} {key} = {value}\n'
			f.write(ln)

		if multi_config_keys:
			for config_id in MultiConfig.config_ids:
				f.write('\n')
				f.write(self.ENTER_GROUP_PREFIX + config_id + self.ENTER_GROUP_SUFFIX + '\n')
				for key in multi_config_keys:
					instance = self.config_instances[key]
					value = self.format_value(instance, config_id)
					value = shlex.quote(value)
					if comments:
						self.write_help(f, instance)
					ln = f'{self.SET[0]} {key} = {value}\n'
					f.write(ln)

	def format_value(self, instance: Config[typing.Any], config_id: 'ConfigId|None') -> str:
		return instance.format_value(config_id)

	def write_data_types(self, f: typing.TextIO, config_keys: 'Iterable[str]', ignore: 'Iterable[Config[typing.Any]]|None') -> None:
		data_types_to_be_explained = set()
		for key in config_keys:
			instance = self.config_instances[key]
			if not instance.wants_to_be_exported():
				continue

			if ignore is not None and instance in ignore:
				continue

			t = instance.type if instance.type != list else instance.item_type

			if t in self.primitive_types:
				continue

			if issubclass(t, enum.Enum):
				continue

			if not hasattr(t, 'help'):
				continue

			data_types_to_be_explained.add(t)

		prefix = self.COMMENT + ' '
		n = '\n'

		if not data_types_to_be_explained:
			return

		name = 'Data types'
		f.write(prefix + name + n)
		f.write(prefix + '-'*len(name) + n)

		for name, t in sorted(((getattr(t, 'type_name', t.__name__), t) for t in data_types_to_be_explained), key=lambda name_type: name_type[0]):
			ln = '- %s' % name
			f.write(prefix + ln + n)
			for ln in self.strip_indentation(t.help.rstrip().lstrip('\n').splitlines()):
				ln = '  ' + ln
				f.write(prefix + ln + n)

	@staticmethod
	def strip_indentation(lines: 'Iterable[str]') -> 'Iterator[str]':
		lines = iter(lines)
		ln = next(lines)
		stripped_ln = ln.lstrip()
		yield stripped_ln

		i = len(ln) - len(stripped_ln)
		for ln in lines:
			assert i == 0 or ln[:i].isspace()
			yield ln[i:]

	def write_help(self, f: typing.TextIO, instance: Config[typing.Any]) -> None:
		if instance.parent is not None:
			name = instance.parent.key_prefix
		else:
			name = instance.key
		if name == self.last_name:
			return

		prefix = self.COMMENT + ' '
		n = '\n'

		f.write(n)
		f.write(prefix + name + n)
		f.write(prefix + '-'*len(name) + n)
		f.write(prefix + instance.format_allowed_values_or_type() + n)
		#if instance.unit:
		#	f.write(prefix + 'unit: %s' % instance.unit + n)
		if isinstance(instance.help, dict):
			for key, val in instance.help.items():
				key_name = instance.format_any_value(key)
				val_name = instance.format_any_value(val)
				f.write(prefix + key_name + ': ' + val_name + n)
		elif isinstance(instance.help, str):
			f.write(prefix + instance.help + n)

		self.last_name = name


	# ------- error handling -------

	def parse_error(self, msg: str, ln: str, lnno: 'int|None') -> None:
		'''
		Is called if something went wrong while trying to load a config file.
		This method compiles the given information into an error message and calls :meth:`UiNotifier.show_error`.

		:param msg: The error message
		:param ln: The line where the error occured
		:param lnno: The number of the line
		'''
		if lnno is not None:
			lnref = 'line %s' % lnno
		else:
			lnref = 'line'
		msg +=  f' while trying to parse {lnref} {ln!r}'
		self.ui_notifier.show_error(msg)
