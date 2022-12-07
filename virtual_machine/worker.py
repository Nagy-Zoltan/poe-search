import clipboard
import Pyro4

from ip import IP


Receiver = Pyro4.Proxy(f"PYRONAME:Receiver@{IP}")


clipboard_content = None


while True:
	clip = clipboard.paste()
	if clip != clipboard_content:
		Receiver.catch_event()
		clipboard_content = clip
