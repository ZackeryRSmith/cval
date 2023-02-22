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

class Warning(Error):
    """ Used when cval detects something that could cause unintended results and security issues """
    pass

def cval(
    source              : Union[str, bytes, CodeType]             ,
    globals             : Optional[Dict[str, Any]]       =None     ,
    locals              : Optional[Mapping[str, Any]]    =None     ,
    modules             : Optional[bool]                 =False   ,
    calls               : Optional[bool]                 =False   ,
    allowed_modules     : Optional[list]                 =[]      ,
    allowed_calls       : Optional[list]                 =[]      ,
    allowed_global_vars : Optional[list]                 =[]      ,
    allowed_local_vars  : Optional[list]                 =[]      ,
):
    """
    A safer version of eval
    
    :: NOTE
    : This is merely a defense before a statement is sent to eval. If by some means cval does 
    : not catch anything, that code will end up going through eval. As long as cval is used right,
    : it will be very difficult for someone to do code injection with eval.

    :: BEST PRACTICE
    : It's a better idea to just not use eval in the first place. It may seem like using eval is 
    : the only way to accomplish a certain task, and maybe it is in your case. Though with enough 
    : rethinking, it is 100% possible to remove eval in the first place. Use cval as a last ditch thing!
    
    :param str  source              : code to be evaluated
    :param dict globals             : global variables and symbols for the current program
    :param dict locals              : local variables and symbols for the current program's scope
    :param bool modules             : allow eval to import packages 
    :param bool calls               : allow eval to make function calls
    :param list allowed_modules     : allow some modules to be used by eval
    :param list allowed_calls       : allow some functions to be called
    :param list allowed_global_vars : allow variables from the global scope to be accessed
    :param list allowed_local_vars  : allow variables from the local scope to be accessed
    """
    

    # Check if a global variable is being used
    if globals:
        # if `*` is the first element of this array every global var is allowed
        if allowed_global_vars != [] and allowed_global_vars[0] == "*":
            allowed_global_vars = globals 
            
        # remove allowed global variables
        res = [i for i in list(globals) if i not in allowed_global_vars]
        
        for key in res:
            if key in source:
                raise SuspiciousSource(f'Cval found global variable "{key}" in the source, killing for safety.')
    elif len(allowed_global_vars):
        raise Warning("passed values to allowed_global_vars but globals was never defined! Killing for safety")
    
    # Check if a local variable is being used
    if locals:
        # if `*` is the first element of this array every global var is allowed
        if allowed_local_vars != [] and allowed_local_vars[0] == "*":
            allowed_local_vars = locals
            
        # remove allowed global variables
        res = [i for i in list(locals) if i not in allowed_local_vars]
        
        for key in res:
            if key in source:
                raise SuspiciousSource(f'Cval found local variable "{key}" in the source, killing for safety.')

    elif len(allowed_local_vars):
        raise Warning("passed values to allowed_local_vars but locals was never defined! Killing for safety")

    # Check for a module import
    if modules == False:
        res = search(r"__import__.*\((?P<module>([^\)])*\))", source)
        if res:
            # Check if module was pardoned
            if res.group("module").replace("(", "").replace("'", "").replace('"', "").replace(")", "") in allowed_modules:
                pass
            else:
                # Some extra checks
                #if res.group("module").replace("(", "").replace("'", "").replace('"', "").replace(")", "") == "":
                #    raise IllegalSource("Cval panicked due to an attemped module import in source!")
                raise IllegalSource(f'Cval panicked due to an attempted illegal import of the module {res.group("module")[:-1]}')
    
    # Check for function call
    if calls == False:
        res = search(r"(?P<function>[a-zA-Z][a-zA-Z1-9]+).*(?P<arguments>\([^\)]*\)(\.[^\)]*\))?)", source)
        if res:
            # Check if call was pardoned
            if res.group("function") in allowed_calls: pass
            else: raise IllegalSource(f'Cval panicked due to an illegal function call in source! Attemped call to "{res.group("function")}"')           

    # Pass parsed source to eval
    return eval(source, globals, locals)
