# A bunch of unit tests for seval

from seval import seval


# Importing a module method 1
try:
    seval("__import__('os')", import_modules=False)
except:
    print("Passed `module importing 1`")

# Calling a function
try:
    seval("foo('bar')", calls=False)
except:
    print("Passed `calling function 1`")
