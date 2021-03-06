# A safer version of Python's eval function
# Written by ZackeryRSmith, protected by the GNU GPL3.0

from typing import (
    Any      ,
    Dict     ,
    Mapping  ,
    Optional ,
    Union
)
from types import CodeType
from re    import search


class Error(Exception):
    """ Base error class """
    def __init__(self, message):
        super().__init__(message)
        

class IllegalSource(Error):
    """ Used when the source passed goes against the set rules """
    pass


class SuspiciousSource(Error):
    """ Used whenever it's not 100% certain the source is illegal """
    pass


def cval(
    source           : Union[str, bytes, CodeType]             ,
    globals          : Optional[Dict[str, Any]]       =...     ,
    locals           : Optional[Mapping[str, Any]]    =...     ,
    gscope           : Optional[bool]                 =False   ,
    lscope           : Optional[bool]                 =False   ,
    allowed_modules  : Optional[list]                 =[]      ,
    modules          : Optional[bool]                 =False   ,
    allowed_calls    : Optional[list]                 =[]      ,
    calls            : Optional[bool]                 =False   ,
):
    """
    A safer version of eval
    
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
    :param bool calls: Allow eval to make function calls
    :param list allowed_modules: Allow some modules to be used by eval
    :param list allowed_calls: Allow some functions to be called
    """
    # Check if a global variable is being used
    if gscope == False and globals != ...:
        for key in list(globals):
            if key in source:
                raise SuspiciousSource(f'Cval found global variable "{key}" in the source, killing for safety.')
    elif gscope == True and globals == ...:
        raise ValueError("gscope activated but globals was never defined!")
    
    # Check if a local variable is being used
    if lscope == False and globals != ...:
        for key in list(locals):
            if key in source:
                raise SuspiciousSource(f'Cval found local variable "{key}" in the source, killing for safety.')
    elif lscope == True and locals == ...:
        raise ValueError("lscope activated but locals was never defined!")

    # Check for a module import
    if modules == False:
        res = search(r"__import__.*\((?P<module>([^\)])*\))t", source)
        if res:
            # Check if module was pardoned
            if res.group("module").replace("(", "").replace("'", "").replace('"', "").replace(")", "") in allowed_modules:
                pass
            else:
                # Some extra checks
                if res.group("module").replace("(", "").replace("'", "").replace('"', "").replace(")", "") == "":
                    raise IllegalSource("Cval panicked due to an attemped module import in source!")
                raise IllegalSource("Cval panicked due to an illegal module import in source!")
    
    # Check for function call
    if calls == False:
        res = search(r"(?P<function>[a-zA-Z][a-zA-Z1-9]+).*(?P<arguments>\([^\)]*\)(\.[^\)]*\))?)", source)
        if res:
            # Check if call was pardoned
            if res.group("function") in allowed_calls: pass
            else: raise IllegalSource("Cval panicked due to an illegal function call in source!")           

    # Pass parsed source to eval
    if   globals != ... and locals != ... : return eval(source, globals, locals)
    elif globals != ...                   : return eval(source, globals)
    elif locals  != ...                   : return eval(source, locals)
    else                                  : return eval(source)
