

def addTrailingSlash(strToAdjust: str) -> str:
    """Adds a trailing slash to the end of the string, if it doesn't contain trailing slash"""
    return strToAdjust if strToAdjust[-1] == '/' else strToAdjust + '/'


class EasyUrl:
    """Simple wrapper for building URLs in Python syntax and treating them as objects and functions
    address : str | EasyUrl
        A string with initial URL, or another EasyUrl instance from which it will copy it's URL
    callHandler : callable | EasyUrl = None
        A function to handle __call__ method or EasyUrl from which the handler is copied
        It's called the following way: callHandler(*((selfAddress,) + args), **kwds)
    """

    def __init__(self, address:any , callHandler:callable=None):
        if isinstance(address, EasyUrl):
            address = object.__getattribute__(address, "address")
        self.address = address
        if isinstance(callHandler, EasyUrl):
            callHandler = object.__getattribute__(callHandler, "callHandler")
        self.callHandler = callHandler

    def __getitem__(self, name):
        callHandler = object.__getattribute__(self, "callHandler")
        selfAddress = object.__getattribute__(self, "address")
        newAddress = addTrailingSlash(selfAddress) + str(name)
        return type(self)(newAddress, callHandler)

    def __getattribute__(self, name):
        return self[name]

    def __add__(self, other):
        callHandler = object.__getattribute__(self, "callHandler")
        selfAddress = object.__getattribute__(self, "address")
        newAddress = selfAddress + str(other)
        return type(self)(newAddress, callHandler)

    def __str__(self) -> str:
        return object.__getattribute__(self, "address")

    def __call__(self, *args: any, **kwds: any) -> any:
        callHandler = object.__getattribute__(self, "callHandler")
        selfAddress = object.__getattribute__(self, "address")
        if callHandler:
            return callHandler(*((selfAddress,) + args), **kwds)
