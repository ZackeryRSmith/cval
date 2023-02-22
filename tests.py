# some tests for cval

from cval import cval, IllegalSource, SuspiciousSource, Warning

# ONLY USED FOR TESTING
import os

# disable module importing 
# :NOTE: modules is False by default, and the reason we allow function calls
#        is to see the error given when trying to import a module.
try: cval('__import__("os")', calls=True, modules=False)
except IllegalSource:
    print("Passed test 1")

# allow certain modules
if cval('__import__("os")', allowed_modules=["os"], allowed_calls=["import"]) == os:
    print("Passed test 2")

# allow certain function calls
cval('print("Passed test 3")', allowed_calls=["print"])

# block access to global variables
foo = "bar"

def foobar():
    try: cval('print(foo)', globals=globals(), allowed_calls=["print"])  # Will not be able to access "foo"
    except SuspiciousSource:
        print("Passed test 4")
foobar()

# allow some access to global variables
foo = "bar"

def foobar():
    cval('print(foo, end=": ")', globals=globals(), allowed_global_vars=["foo"], allowed_calls=["print"])
    print("Passed test 5")
foobar()

# alternativly allow access to all global variables
foo = "bar"
bar = "foo"

def foobar():
    cval('print(bar+foo, end=": ")', globals=globals(), allowed_global_vars=["*"], allowed_calls=["print"])
    print("Passed test 6")
foobar()

# block access to local variables
def fizzbuzz():
    fizz = "buzz"
    try: cval('print(fizz)', locals=locals())  # Will not be able to access "fizz"
    except SuspiciousSource:
        print("Passed test 7")
fizzbuzz()

# allow some access to local variables
def fizzbuzz():
    fizz = "buzz"
    cval('print(fizz, end=": ")', locals=locals(), allowed_local_vars=["fizz"], allowed_calls=["print"])
    print("Passed test 8")
fizzbuzz()

# alternativly allow access to all local variables
def fizzbuzz():
    fizz = "buzz"
    buzz = "fizz"
    cval('print(buzz+fizz, end=": ")', locals=locals(), allowed_local_vars=["*"], allowed_calls=["print"])
    print("Passed test 9")
fizzbuzz()
