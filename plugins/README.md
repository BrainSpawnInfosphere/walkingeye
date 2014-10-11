# Plugins

## Plugins

The plugins for this use a base class `Module` which has a couple of useful methods. An example of a plugin is shown below:

    from Modula import *
    
    class Plugin(Module):
		def __init__(self):
			Module.__init__(self,'intent')
			
		def process(self, entity):
			return 'string'
			
The class is always called `Plugin` and the main method that gets called is `process()`.