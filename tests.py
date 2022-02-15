# A bunch of unit tests for seval

from cval import cval, IllegalSource, SuspiciousSource

# Variables for testing
username = "abc"
password = "1234"


# Accessing global variables
try:
    cval("password", globals=globals(), gscope=False)
except SuspiciousSource:
    print("Passed `fetch global variable 1`")
except:
    print("Failed to pass `fetch global variable 1`")


# Importing a module
try:
    cval("__import__('os')", import_modules=False)
except IllegalSource:
    print("Passed `module importing 1`")
except:
    print("Failed to pass `module importing 1`")


# Calling a function
try:
    cval("foo('bar')", calls=False)
except IllegalSource:
    print("Passed `calling function 1`")
except:
    print("Failed to pass `calling function 1`")
