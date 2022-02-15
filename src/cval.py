# Safe(er) eval

from typing import *
from types import (
    CodeType
)
from re import *

class Error(Exception):
    """ Base error class """
    pass

class IllegalSource(Error):
    """ Used when the source passed goes against the set rules """
    pass

class SuspiciousSource(Error):
    """ Used whenever it's not 100% certain the source is illegal """
    pass


def cval(
    source: Union[str, bytes, CodeType]             ,
    globals: Optional[Dict[str, Any]]      =...     ,
    locals: Optional[Mapping[str, Any]]    =...     ,
    smart: Optional[bool]                  =True    ,
    gscope: Optional[bool]                 =False   ,
    lscope: Optional[bool]                 =False   ,
    allowed_modules: Optional[list]        =[]      ,
    modules: Optional[bool]         =False   ,
    allowed_calls: Optional[list]          =[]      ,
    calls: Optional[bool]                  =False   ,
):
    """
    A safer version of eval, depending on the use case + proper usage 
    this should patch eval vulnerabilities in your code.
    
    :: NOTE
    : This is mearly a defence before a statement is sent to eval. If by some means 
    : cval does not catch anything, that code will end up going through eval. Aslong as 
    : cval is used right it will be very difficult for someone to do code injection with eval.

    :: BEST PRACTICE
    : It's a better idea to just not use eval in the first place. It may seems like using
    : eval is the only way to accomplish a certain task, and maybe it is in your case.
    : With enough rethinking it is 100% possible to remove eval in the first place.
    : Use cval as a last ditch thing!
        
    :param bool gscope: Allow eval to refrence anything from the global scope. !! REQUIRES `globals` TO BE PASSED !!
    :param bool lscope: Allow eval to refrence anything from the local scope. !! REQUIRES `locals` TO BE PASSED !!
    :param bool modules: Allow eval to import packages 
    :param list allowed_modules: Allow some modules to be used by eval
    :param bool calls: Allow eval to make function calls
    :param list allowed_calls: Allow some functions to be called
    """
    # Check if a global variable is being used
    if gscope != True and globals != ...:
        for key in list(globals):
            if key in source:
                raise SuspiciousSource(f'Cval found global variable "{key}" in the source, killing for safety')
    elif gscope == True and globals == ...:
        raise ValueError("gscope activated but globals was never defined!")
    
    # Check if a local variable is being used
    if lscope != True:
        pass

    # Check for a module import
    if modules != True:
        res = search(r"__import__\((?P<module>([^\)])*\))", source)
        if res:
            # Check if module was pardoned
            if res.group("module").replace("(", "").replace("'", "").replace('"', "").replace(")", "") in allowed_modules:
                pass
            else:
                # Some extra checks
                if res.group("module").replace("(", "").replace("'", "").replace('"', "").replace(")", "") == "":
                    raise IllegalSource("Cval panicked due to an attemped module import in source")
                raise IllegalSource("Cval panicked due to an illegal module import in source")
    
    # Check for function call
    if calls != True:  # Meaning function calls are not allowed
        res = search(r"(?P<function>[a-zA-Z]+)(?P<arguments>\([^\)]*\)(\.[^\)]*\))?)", source)
        if res:
            # Check if call was pardoned
            if res.group("function") in allowed_calls:
                pass
            else:
                raise IllegalSource("Cval panicked due to an illegal function call in source!")           

    # Pass parsed source to eval
    if globals != ... and locals != ...: return eval(source, globals, locals)
    elif globals != ...: return eval(source, globals)
    elif locals != ...: return eval(source, locals)
    else: return eval(source)
