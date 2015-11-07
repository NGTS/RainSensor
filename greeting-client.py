# saved as greeting-client.py
import Pyro4

getRain = Pyro4.Proxy("PYRONAME:example.sensor")    # use name server object lookup uri shortcut
print(getRain.get_rain('test'))