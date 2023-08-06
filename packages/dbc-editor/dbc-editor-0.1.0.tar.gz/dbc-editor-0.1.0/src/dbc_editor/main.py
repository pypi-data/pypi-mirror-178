#!/usr/bin/env python3

'''
An editor for CAN bus database files like dbc or sym, based on cantools and urwid
'''

__version__ = '0.1.0'


import os
import sys
import argparse

import urwid
import cantools

from .config import Config
from . import urwid_edit_with_history


ATTR_TITLE = 'title'
ATTR_HELP_LINE = 'help-line'
ATTR_ERROR = 'error'

CANCEL = 'cancel'


# ------- base classes -------

class MyWindow(urwid.Frame):

	def __init__(self, body=None, **kw):
		self.prev_window = kw.pop('prev_window', None)
		super().__init__(body, **kw)

	def set_body(self, body):
		self.body = body

	def set_title(self, title):
		self.header = urwid.Text((ATTR_TITLE, title))

	def set_help_line(self, shortcuts):
		'''shortcuts: iterable of (key, command) tuples'''
		ln = ", ".join(f"{key}: {cmd}" for key, cmd in shortcuts)
		self.footer = urwid.Text((ATTR_HELP_LINE, ln))

	def cmd_back(self):
		return self.prev_window

	def cmd_search(self):
		search_edit = SearchEdit(self)
		search_edit.set_direction(reverse=False)
		self.footer = search_edit
		self.focus_position = "footer"

	def cmd_search_reverse(self):
		search_edit = SearchEdit(self)
		search_edit.set_direction(reverse=True)
		self.footer = search_edit
		self.focus_position = "footer"

	def search_do(self, text, **flags):
		self.body.search_do(text, **flags)

	def search_cancel(self):
		self.footer = None
		self.focus_position = "body"

	def show_error(self, msg: str) -> None:
		self.footer = urwid.Text((ATTR_ERROR, msg))


class MyListBox(urwid.ListBox):

	def search_do(self, text, **flags):
		#TODO
		pass

class LineWidget(urwid.Text):

	def keypress(self, size, key):
		return key

	def selectable(self):
		return True


# ------- input widgets -------

class EditBaseClass(urwid.Edit):

	def register_on_change_listener(self, callback: 'Callable[[Self, T], None]') -> None:
		urwid.connect_signal(self, 'postchange', callback)


class TextEdit(EditBaseClass):

	def check(self) -> bool:
		return bool(self.value())

	def value(self) -> str:
		return self.get_edit_text()

	def set_value(self, value: str) -> None:
		self.set_edit_text(value)
		self.set_edit_pos(len(self.get_edit_text()))

class OptionalTextEdit(EditBaseClass):

	def check(self) -> bool:
		return True

	def value(self) -> 'str|None':
		out = self.get_edit_text()
		if out:
			return out
		return None

	def set_value(self, value: 'str|None') -> None:
		if value is None:
			self.set_edit_text('')
		else:
			self.set_edit_text(value)
			self.set_edit_pos(len(self.get_edit_text()))

class HexEdit(EditBaseClass):

	fmt = '03X'

	# override method of super class
	def valid_char(ch: str) -> bool:
		return ch.lower() in '0123456789abcdef'

	def check(self) -> bool:
		return bool(self.get_edit_text())

	def value(self) -> int:
		return int(self.get_edit_text(), base=16)

	def set_value(self, value: int) -> None:
		self.set_edit_text(format(value, self.fmt))
		self.set_edit_pos(len(self.get_edit_text()))

class UintEdit(EditBaseClass):

	fmt = ''

	# override method of super class
	def valid_char(self, ch: str) -> bool:
		return ch.lower() in '0123456789'

	def check(self) -> bool:
		return bool(self.get_edit_text())

	def value(self) -> int:
		return int(self.get_edit_text())

	def set_value(self, value: int) -> None:
		self.set_edit_text(format(value, self.fmt))
		self.set_edit_pos(len(self.get_edit_text()))

class FloatEdit(EditBaseClass):

	def __init__(self, caption: str, *, default_value: 'float|None' = None, fmt: str = '') -> None:
		super().__init__(caption=caption)
		self.default_value = default_value
		self.fmt = fmt

	# override method of super class
	def valid_char(self, ch: str) -> bool:
		return ch.lower() in '0123456789.'

	def check(self) -> bool:
		val = self.get_edit_text()
		if not val:
			return self.default_value is not None
		try:
			float(val)
			return True
		except ValueError:
			return False

	def value(self) -> float:
		val = self.get_edit_text()
		if not val:
			return self.default_value
		out = float(val)
		if out.is_integer():
			return int(out)
		return out

	def set_value(self, value: float) -> None:
		self.set_edit_text(format(value, self.fmt))
		self.set_edit_pos(len(self.get_edit_text()))


class PackableRadioButton(urwid.RadioButton):

	def pack(self, size=None, focus=False):
		text = ' '*self.reserve_columns + self.get_label()
		return urwid.Text(text).pack(size=size, focus=focus)

class ChoiceEdit(urwid.Columns):

	def __init__(self, caption: str, *, choices: 'list[str], dict[str, T]') -> None:
		self.caption = caption
		self.choices: 'dict[str, T]' = choices if isinstance(choices, dict) else {v:v for v in choices}
		buttons_group = []
		self.caption = urwid.Text(caption)
		self.radio_buttons = {key: PackableRadioButton(buttons_group, key) for key in list(choices)}
		widgets = [self.caption] + list(self.radio_buttons.values())
		widget_list = [('pack', w) for w in widgets]
		super().__init__(widget_list, dividechars=1)

	def check(self) -> bool:
		return any(btn.state for btn in self.radio_buttons.values())

	def value(self) -> 'T':
		for key, rb in self.radio_buttons.items():
			if rb.state:
				return self.choices[key]

		return None

	def set_value(self, value: 'T') -> None:
		for key, val in self.choices.items():
			if val == value:
				self.radio_buttons[key].set_state(True)
				return

		raise ValueError('Invalid value %r. Should be one of %s' % (value, ', '.join(repr(v) for v in self.choices.values())))

	def register_on_change_listener(self, callback: 'Callable[[Self, T], None]') -> None:
		emit = [False]
		def wrapper(rbtn: urwid.RadioButton, old_state: bool):
			# This is triggered by every radio button which changes,
			# i.e. twice, once for the button which changes from True to False
			# and once for the button which changes from False to True.
			# Checking rbtn.state would ensure that callback is called only once
			# but depending on whether the selection is moved from left to right
			# or right to left it would be called before or after the update
			# so self.value() would be sometimes correct and sometimes not.
			# Instead I am using emit to ensure that callback is called every
			# second time wrapper is called.
			if emit[0]:
				callback(rbtn, self.value())
			emit[0] = not emit[0]

		for rbtn in self.radio_buttons.values():
			urwid.connect_signal(rbtn, 'postchange', wrapper)


# ------- search widget -------

class SearchEdit(urwid_edit_with_history.EditWithHistory):

	PROMPT = "/"
	PROMPT_REVERSE = "?"

	FLAG_SEP = "/"

	flags = {
		'c' : ('case_sensitive', True),
		'i' : ('case_sensitive', False),
		'e' : ('is_regex', True),
		'f' : ('is_regex', False),
	}

	def __init__(self, app):
		super().__init__(multiline=False)
		self.app = app
	
	def clear(self):
		self.edit_text = ""
	
	def set_direction(self, reverse):
		if reverse:
			caption = self.PROMPT_REVERSE
		else:
			caption = self.PROMPT

		self.set_caption(caption)

	def keypress(self, size, key):
		if not super().keypress(size, key):
			return

		cmd = self._command_map[key]
		if cmd == urwid.ACTIVATE:
			try:
				text, flags = self.parse_input()
			except ParseException as err:
				self.app.show_error(err.msg)
				return
			self.app.search_do(text, **flags)
		elif cmd == CANCEL:
			self.app.search_cancel()
	
	def parse_input(self):
		text = self.edit_text

		if self.FLAG_SEP in text:
			text, flags = text.rsplit(self.FLAG_SEP, 1)
			flags = self.parse_flags(flags)
		else:
			flags = {}

		return text, flags

	def parse_flags(self, text):
		flags = {}

		for c in text:
			if c in self.flags:
				key, val = self.flags[c]
				flags[key] = val
			else:
				supported_flags = _(",").join(self.flags.keys())
				self.error(_("invalid flag {flag}; should be one of {supported_flags}").format(flag=c, supported_flags=supported_flags))

		return flags

	def error(self, msg):
		raise ParseException(msg)

class ParseException(ValueError):

	def __init__(self, msg):
		super().__init__(msg)
		self.msg = msg


# ------- main window classes -------

class MyAttrMap(urwid.AttrMap):

	def __init__(self, widget):
		super().__init__(widget, None, CanDatabaseEditor.focus_map)


class ChoiceBox(urwid.Overlay):

	MIN_WIDTH = 30

	def __init__(self, bg, title, choices, cancel=None, **kw):
		self.choices = choices

		title = urwid.Text(title)
		buttons = urwid.Columns(urwid.Button(label, on_press=self.wrap_callback(callback)) for label, callback in choices.items())
		fg = urwid.Pile([title, buttons])
		fg = urwid.LineBox(fg)

		kw.setdefault('align', urwid.CENTER)
		kw.setdefault('valign', urwid.MIDDLE)
		kw.setdefault('width', self.get_width())
		kw.setdefault('height', None)
		super().__init__(fg, bg, **kw)

		if cancel:
			self.cmd_cancel = cancel
		else:
			self.cmd_cancel = lambda: bg

	def wrap_callback(self, callback) -> None:
		def wrapper(btn: urwid.Button) -> None:
			new_window = callback()
			if new_window:
				self.app.open_window(new_window)

		return wrapper

	def get_width(self):
		out = sum(len(c)+4 for c in self.choices)
		if out < self.MIN_WIDTH:
			out = self.MIN_WIDTH
		out += 2
		return out


class MessageList(MyWindow):

	def __init__(self, db):
		self.db = db
		title = 'messages'
		shortcuts = [
			('up/down', 'select message'),
			('+', 'new message'),
			('-', 'delete message'),
			('enter', 'show signales'),
			#TODO: edit message
			('q', 'quit')
		]

		super().__init__()
		self.set_title(title)
		self.set_help_line(shortcuts)
		self.update()

	def update(self):
		content = [MyAttrMap(MessageLineWidget(msg)) for msg in self.db.messages]
		content = MyListBox(content)
		self.set_body(content)

	def get_selected_message(self):
		return self.body.focus.base_widget.msg

	def cmd_open(self):
		return SignalList(self.get_selected_message(), prev_window=self)

	def cmd_edit(self):
		return MessageEdit(self.db, self.get_selected_message(), prev_window=self)

	def cmd_new(self):
		return MessageEdit(self.db, prev_window=self)

	def cmd_remove(self):
		self.db.messages.remove(self.get_selected_message())
		self.update()
		self.app.notify_has_changed()

class MessageLineWidget(LineWidget):

	fmt_line = Config('message-list.fmt', '{msg.frame_id:>6x} {msg.name}  (DLC: {msg.length}, bytes used: {bytes_used})')

	def __init__(self, msg):
		bytes_used = sum(sig.length for sig in msg.signals) / 8.0
		if bytes_used.is_integer():
			bytes_used = int(bytes_used)
		super().__init__(self.fmt_line.format(msg=msg, bytes_used=bytes_used))
		self.msg = msg


class MessageEdit(MyWindow):

	#TODO: check user input like in SignalEdit

	title_edit = 'edit message {msg.frame_id:03x} {msg.name}'
	title_new = 'create new message'

	fmt_frame_id = Config('message-edit.fmt.frame_id', '{:03x}')
	fmt_is_extended_frame = Config('message-edit.fmt.is_extended_frame', '{}')
	fmt_length = Config('message-edit.fmt.length', '{}')
	fmt_name = Config('message-edit.fmt.name', '{}')
	fmt_comment = Config('message-edit.fmt.comment', '{}')

	def __init__(self, db, msg=None, **kw):
		self.db = db
		self.msg = msg
		self.edit_frame_id = urwid.Edit("Frame ID: ")
		self.edit_is_extended_frame = urwid.Edit("Is extended: ")
		self.edit_name = urwid.Edit("Message Name: ")
		self.edit_comment = urwid.Edit("Comment: ")
		self.edit_length = urwid.Edit("Data length (in bytes): ")

		if msg:
			title = self.title_edit.format(msg=msg)
			for key in ('frame_id', 'is_extended_frame', 'name', 'comment', 'length'):
				val = getattr(msg, key)
				if val is None:
					val = ''
				val = getattr(self, 'fmt_%s' % key).format(val)
				widget = getattr(self, 'edit_%s' % key)
				widget.set_edit_text(val)
		else:
			title = self.title_new

		pile = urwid.Pile([
			self.edit_frame_id,
			self.edit_is_extended_frame,
			self.edit_name,
			self.edit_comment,
			self.edit_length,
		])
		filler = urwid.Filler(pile)

		super().__init__(filler, **kw)
		self.set_title(title)

	def get_input_data(self):
		out = {}
		out['frame_id'] = int(self.edit_frame_id.get_edit_text(), base=16)
		out['is_extended_frame'] = self.edit_is_extended_frame.get_edit_text().strip().lower() != 'false'
		out['name'] = self.edit_name.get_edit_text()
		out['comment'] = self.edit_comment.get_edit_text()
		out['length'] = 0 if not self.edit_length.get_edit_text() else int(self.edit_length.get_edit_text())
		return out

	def has_changed(self):
		if not self.msg:
			return True

		data = self.get_input_data()
		for key in data:
			new_val = data[key]
			old_val = getattr(self.msg, key)
			if (new_val or old_val) and new_val != old_val:
				return True

		return False

	#TODO: this name is somewhat misleading for save but that is what activate is currently mapped to
	def cmd_open(self):
		return self.reply_save()

	def cmd_cancel(self):
		return super().cmd_back()

	def cmd_back(self):
		if self.has_changed():
			return ChoiceBox(bg=self, title='Save changes?', choices={'Yes':self.reply_save, 'No':self.reply_dont_save}, cancel=self.reply_cancel)

		return super().cmd_back()

	def reply_save(self):
		if self.msg:
			for attr, value in self.get_input_data().items():
				setattr(self.msg, attr, value)
			out = self.prev_window
		else:
			newmsg = cantools.database.Message(signals=[], **self.get_input_data())
			self.db.messages.append(newmsg)
			out = SignalList(newmsg, prev_window=self.prev_window)

		self.prev_window.update()
		self.app.notify_has_changed()
		return out

	def reply_dont_save(self):
		return self.cmd_cancel()

	def reply_cancel(self):
		return self


class SignalList(MyWindow):

	title = 'signals of message {msg.frame_id:03x} {msg.name}'

	def __init__(self, msg, **kw):
		self.msg = msg

		title = self.title.format(msg=msg)
		shortcuts = [
			('up/down', 'select signal'),
			('+', 'new signal'),
			('-', 'delete signal'),
			#TODO: edit signal
			('q', 'quit')
		]
		body = [MyAttrMap(SignalLineWidget(sig)) for sig in sorted(self.msg.signals, key=lambda sig: sig.start)]
		body = MyListBox(body)

		super().__init__(body, **kw)
		self.set_title(title)
		self.set_help_line(shortcuts)

	def update(self):
		body = [MyAttrMap(SignalLineWidget(sig)) for sig in sorted(self.msg.signals, key=lambda sig: sig.start)]
		body = MyListBox(body)
		self.set_body(body)

	def get_selected_signal(self):
		return self.body.focus.base_widget.signal

	def cmd_open(self):
		return SignalEdit(self.msg, self.get_selected_signal(), prev_window=self)

	def cmd_edit(self):
		return SignalEdit(self.msg, self.get_selected_signal(), prev_window=self)

	def cmd_new(self):
		return SignalEdit(self.msg, prev_window=self)

	def cmd_remove(self):
		self.msg.signals.remove(self.get_selected_signal())
		self.update()
		self.app.notify_has_changed()

class SignalLineWidget(LineWidget):

	def __init__(self, signal):
		self.signal = signal
		super().__init__(f'{signal.name}  {signal.start},{signal.length}  x{signal.scale}->{signal.unit}')


class SignalEdit(MyWindow):

	title_edit = 'edit signal {sig.name} of message {msg.frame_id:03x} {msg.name}'
	title_new = 'create new signal for message {msg.frame_id:03x} {msg.name}'

	TYPE_UNSIGNED_INT = 'uint'
	TYPE_SIGNED_INT = 'int'
	TYPE_FLOAT = 'float'
	TYPE_CHOICES = 'choices'
	TYPES = (TYPE_UNSIGNED_INT, TYPE_SIGNED_INT, TYPE_FLOAT, TYPE_CHOICES)

	BYTE_ORDER = {
		'Little Endian / Intel' : 'little_endian',
		'Big Endian / Motorola' : 'big_endian',
	}

	default_byte_order = Config('signal-edit.default-byte-order', 'little_endian', allowed_values=BYTE_ORDER.values())

	def __init__(self, msg, sig=None, **kw):
		self.msg = msg
		self.sig = sig
		self.edit_name = TextEdit("Signal Name: ")
		self.edit_start = UintEdit("Start Bit: ")
		self.edit_length = UintEdit("Length (number of bits): ")
		self.edit_byte_order = ChoiceEdit("Byte Order: ", choices=self.BYTE_ORDER)
		self.edit_type = ChoiceEdit("Type: ", choices=self.TYPES)
		# Factor by which the raw value transmitted via the CAN bus must be multiplied in order to get the specified unit
		self.edit_scale = FloatEdit("Scale: ", default_value=1)
		self.edit_unit = OptionalTextEdit("Unit: ")
		self.edit_comment = OptionalTextEdit("Comment: ")
		self.text_value_range = urwid.Text("")

		self.choices_group: 'list[ChoiceLineEdit]' = []
		ChoiceLineEdit(self.choices_group, self.update_pile_choices)
		self.pile_choices = urwid.Pile(self.choices_group)
		self.pile_number = urwid.Pile([
			self.edit_scale,
			self.edit_unit,
		])
		self.placeholder = urwid.WidgetWrap(self.pile_number)
		self.edit_type.register_on_change_listener(self.on_type_change)

		if sig:
			title = self.title_edit.format(sig=sig, msg=msg)
			for key in ('name', 'start', 'length', 'byte_order', 'scale', 'unit', 'comment'):
				val = getattr(sig, key)
				widget = getattr(self, 'edit_%s' % key)
				widget.set_value(val)
			if sig.choices:
				for val, name in sig.choices.items():
					self.choices_group[-1].set_value(val, str(name))
					# new ChoiceLineEdit are created automatically by ChoiceLineEdit.add_after_if_last
				self.edit_type.set_value(self.TYPE_CHOICES)
			elif sig.is_float:
				self.edit_type.set_value(self.TYPE_FLOAT)
			elif sig.is_signed:
				self.edit_type.set_value(self.TYPE_SIGNED_INT)
			else:
				self.edit_type.set_value(self.TYPE_UNSIGNED_INT)
		else:
			self.edit_byte_order.set_value(self.default_byte_order)
			#TODO: does this work for big endian, too?
			if self.msg.signals:
				last_signal = self.msg.signals[-1]
				self.edit_start.set_value(last_signal.start + last_signal.length)
			else:
				self.edit_start.set_value(0)
			title = self.title_new.format(msg=msg)

		pile = urwid.Pile([
			self.edit_start,
			self.edit_name,
			self.edit_length,
			self.edit_type,
			self.placeholder,
			self.edit_comment,
			self.edit_byte_order,
			self.text_value_range,
		])
		filler = urwid.Filler(pile)

		super().__init__(filler, **kw)
		self.set_title(title)
		self.init_value_range()
		pile.set_focus(1)

	def init_value_range(self) -> None:
		dependencies = (
			self.edit_length,
			self.edit_type,
			self.edit_scale,
			self.edit_unit,
		)
		def get_value_range() -> str:
			if not all(w.check() for w in dependencies):
				return ''

			length = self.edit_length.value()
			dtype = self.edit_type.value()
			scale = self.edit_scale.value()
			unit = self.edit_unit.value()

			if dtype == self.TYPE_UNSIGNED_INT:
				min_val = 0
				max_val = 2**length - 1
			elif dtype == self.TYPE_SIGNED_INT:
				p = 2 ** (length-1)
				min_val = -p
				max_val = p - 1
			else:
				return ''

			min_val *= scale
			max_val *= scale

			if unit is None:
				unit = ''

			return '(value range: {min_val}{unit}..{max_val}{unit})'.format(min_val=min_val, max_val=max_val, unit=unit)
		def update() -> None:
			self.text_value_range.set_text(get_value_range())
		for w in dependencies:
			w.register_on_change_listener(lambda widget, value: update())

		update()

	def on_type_change(self, widget, value) -> None:
		if value == self.TYPE_CHOICES:
			self.placeholder._w = self.pile_choices
		else:
			self.placeholder._w = self.pile_number

	def update_pile_choices(self) -> None:
		self.pile_choices = urwid.Pile(self.choices_group, focus_item=self.pile_choices.get_focus())
		self.placeholder._w = self.pile_choices


	def get_input_data(self):
		dtype = self.edit_type.value()
		if dtype and dtype not in self.TYPES:
			raise ValueError('invalid type %r, should be one of %s' % (dtype, self.TYPES))

		out = {}
		out['name'] = self.edit_name.value()
		out['start'] = self.edit_start.value()
		out['length'] = self.edit_length.value()
		out['is_signed'] = dtype in {self.TYPE_SIGNED_INT, self.TYPE_FLOAT}
		out['is_float'] = dtype == self.TYPE_FLOAT
		out['byte_order'] = self.edit_byte_order.value()
		out['scale'] = self.edit_scale.value()
		out['unit'] = self.edit_unit.value()
		out['comment'] = self.edit_comment.value()
		out['choices'] = {c.edit_value.value() : c.edit_name.value() for c in self.choices_group if c.edit_name.check()} if dtype == self.TYPE_CHOICES else None
		return out

	def check(self, *, silent: bool = False) -> bool:
		if self.edit_type.value() == self.TYPE_CHOICES:
			placeholder_edits = tuple(c.edit_value for c in self.choices_group if c.edit_name.check())
		else:
			placeholder_edits = tuple(widget for widget, options in self.pile_number.contents)
		for w in (
			self.edit_name,
			self.edit_start,
			self.edit_length,
			self.edit_type,
			self.edit_byte_order,
			self.edit_comment,
		) + placeholder_edits:
			if not w.check():
				if not silent:
					self.show_error('Invalid input for %s' % w.caption.rstrip().rstrip(':'))
				return False

		return True

	def has_changed(self):
		if not self.sig:
			return True

		if not self.check(silent=True):
			return True

		data = self.get_input_data()
		for key in data:
			new_val = data[key]
			old_val = getattr(self.sig, key)
			if (new_val or old_val) and new_val != old_val:
				return True

		return False

	#TODO: this name is somewhat misleading for save but that is what activate is currently mapped to
	def cmd_open(self):
		return self.reply_save()

	def cmd_cancel(self):
		return super().cmd_back()

	def cmd_back(self):
		if self.has_changed():
			return ChoiceBox(bg=self, title='Save changes?', choices={'Yes':self.reply_save, 'No':self.reply_dont_save}, cancel=self.reply_cancel)

		return super().cmd_back()

	def reply_save(self):
		if not self.check():
			return

		if self.sig:
			for attr, value in self.get_input_data().items():
				setattr(self.sig, attr, value)
		else:
			newsig = cantools.database.Signal(**self.get_input_data())
			self.msg.signals.append(newsig)

		self.prev_window.update()
		self.app.notify_has_changed()
		return self.cmd_cancel()

	def reply_dont_save(self):
		return self.cmd_cancel()

	def reply_cancel(self):
		return self



class ChoiceLineEdit(urwid.Columns):

	value_width = 3

	# ------- init -------

	def __init__(self, group: 'list[ChoiceLineEdit]', update_pile: 'Callable[[], None]', *, before: 'ChoiceLineEdit|None' = None) -> None:
		self.group = group
		self.update_pile = update_pile
		self.edit_value = UintEdit('')
		self.edit_name = TextEdit('')

		if before is None:
			group.append(self)
		else:
			group.insert(group.index(before), self)
		self.init_value()
		super().__init__([
			(self.value_width, self.edit_value),
			self.edit_name,
		], dividechars=1)
		self.edit_name.register_on_change_listener(lambda w, v: self.add_after_if_last())

	def init_value(self) -> None:
		prev = self.get_prev_value()
		self.edit_value.set_value(0 if prev is None else prev+1)

	def get_prev_value(self) -> 'int|None':
		i = self.group.index(self) - 1
		while i >= 0:
			prev_widget = self.group[i]
			if prev_widget.edit_value.check():
				return prev_widget.edit_value.value()
			i -= 1
		return None

	def set_value(self, value: int, name: str) -> None:
		self.edit_value.set_value(value)
		self.edit_name.set_value(name)

	# ------- events -------

	def add_after_if_last(self) -> None:
		i = self.group.index(self)
		if i < len(self.group) - 1:
			return

		ChoiceLineEdit(self.group, self.update_pile)
		self.update_pile()

	#TODO: this is not called. Does the UintEdit gobble the event?
	def cmd_new(self) -> None:
		self.add_before()

	#TODO: this is not called. Does the UintEdit gobble the event?
	def cmd_remove(self) -> None:
		self.group.remove(self)
		#TODO: decrement numbers of following
		self.update_pile()

	def add_before(self) -> None:
		ChoiceLineEdit(self.group, self.update_pile, before=self)
		#TODO: change duplicate numbers
		self.update_pile()


# ------- main classes -------

class CanDatabaseEditor:

	palette = [
		(ATTR_TITLE, 'brown', 'default'),
		(ATTR_HELP_LINE, 'dark gray', 'default'),
		(ATTR_ERROR, 'dark red', 'default'),
	]

	focus_map = {}

	command_map = urwid.command_map
	command_map['w'] = 'write'
	command_map['q'] = 'quit'
	command_map['e'] = 'edit'
	command_map['esc'] = 'cancel'
	command_map['+'] = 'new'
	command_map['-'] = 'remove'
	command_map['/'] = 'search'
	command_map['?'] = 'search_reverse'

	fallback_commands = {
		'activate' : 'open',
		'cursor right' : 'open',
		'cursor left' : 'back',
	}

	def __init__(self, fn=None):
		self.init_focus_map()
		self.filename = fn
		self.has_changed = False
		if fn and os.path.isfile(fn):
			self.db = cantools.database.load_file(fn, prune_choices=False, sort_signals=None)
		else:
			self.db = cantools.database.Database()

		MessageList.app = self
		MessageEdit.app = self
		SignalList.app = self
		SignalEdit.app = self
		ChoiceBox.app = self

	def init_focus_map(self):
		for name, fg, bg in tuple(self.palette):
			name_focused = name + '_focused'
			self.palette.append((name_focused, fg+',standout', bg))
			self.focus_map[name] = name_focused

		self.focus_map[None] = 'default_focused'
		self.palette.append(('default_focused', 'default,standout', 'default'))

	def run(self):
		widget = MessageList(self.db)
		self.loop = urwid.MainLoop(widget, self.palette, handle_mouse=False, unhandled_input=self.unhandled_input)
		self.loop.run()

	def get_current_window(self):
		return self.loop.widget

	def open_window(self, window):
		self.loop.widget = window

	def unhandled_input(self, key):
		cmd = self.command_map[key]
		cmd = self.fallback_commands.get(cmd, cmd)
		if cmd == 'quit':
			self.quit()
			return
		elif cmd == 'write':
			self.write()
			return

		window = self.get_current_window()
		func = getattr(window, 'cmd_%s' % cmd, None)
		if func:
			new_window = func()
			if new_window:
				self.open_window(new_window)


	def show_error(self, msg: str) -> None:
		self.loop.widget.show_error(msg)


	# ------- write and quit -------

	def notify_has_changed(self):
		self.has_changed = True

	def quit(self):
		if self.has_changed:
			self.open_window(ChoiceBox(bg=self.get_current_window(), title='Save changes?', choices={'Yes':self.write_and_quit, 'No':self.quit_without_write}))
			return

		self.quit_without_write()

	def write_and_quit(self):
		self.write()
		self.quit_without_write()

	def write(self):
		#TODO: check that db is valid by writing it to a tmp file and loading it
		cantools.database.dump_file(self.db, self.filename)
		self.has_changed = False

	def quit_without_write(self):
		raise urwid.ExitMainLoop()



class PrintVersion(argparse.Action):

	def __init__(self, option_strings, dest, **kwargs):
		kwargs.setdefault('nargs', 0)
		argparse.Action.__init__(self, option_strings, dest, **kwargs)

	def __call__(self, parser, namespace, values, option_string=None):
		print(__version__)
		sys.exit(0)


def main(arglist: 'list[str]|None' = None) -> None:
	p = argparse.ArgumentParser(description=__doc__)
	p.add_argument("-v", "--version", action=PrintVersion, help="show the version number of this program and exit")
	p.add_argument('file', help='CAN bus database file, e.g. dbc or sym file')

	args = p.parse_args(arglist)
	dbeditor = CanDatabaseEditor(args.file)
	dbeditor.run()


if __name__ == '__main__':
	main()
