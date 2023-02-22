<!-- TOP OF README ANCHOR -->
<a name="top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/ZackeryRSmith/cval">
    <img src="https://raw.githubusercontent.com/ZackeryRSmith/cval/main/cval.png" alt="Cval logo" width="155" height="155">
  </a>

<h3 align="center">Cval</h3>

  <p align="center">
    A layer of protection for eval
    <br />
    <b>
      <a href="https://github.com/ZackeryRSmith/cval/#examples">View Examples</a>
      ·
      <a href="https://github.com/ZackeryRSmith/cval/issues">Report Bug</a>
    </b>
  </p>
</div>

# Installation
I know many people don't care about the motives behind a program, so I have put the installation at the top.

#### Unix and Mac
```shell
python3 -m pip install cval
```

#### Windows
```powershell
py -m pip install cval
```

## About
A decently simple script that uses regular expression to add a layer of protection to eval. Why? Well I keep seeing *"eval really is dangerous"* and *"eval is a bad practice"*. All these statements have some validity to them, and there is almost always a better way to do what you want to acomplish. Cval tackles the *"eval really is dangerous"* mindset, if you must use eval for a public project use cval.

## Exploiting
I **encourage** you to break my script, report any bugs or vulnerabilities [here](https://github.com/ZackeryRSmith/cval/issues), thanks!

## Examples
These examples are focused purely on security rather then real world practical examples.

##### Disable module importing
```python
# :NOTE: modules is False by default, and the reason we allow function calls
#        is to see the error given when trying to import a module.
cval('__import__("os")', calls=True, modules=False)
```

###### Output:
```text
cval.IllegalSource: Cval panicked due to an attempted illegal import of the module "os"
```

##### Allow certain modules
```python
cval('__import__("os")', allowed_modules=["os"], allowed_calls=["import"])
```

##### Disable function calls
```python
cval('print("Hello, World!")', calls=False)
```

###### Output:
```text
cval.IllegalSource: Cval panicked due to an illegal function call in source! Attemped call to "print"
```

##### Allow certain function calls
```python
cval('print("Hello, World!")', allowed_calls=["print"])
```

##### Block access to global variables
```python
foo = "bar"

def foobar():
    # :NOTE: `globals` doesn't need to be passed in this case
    #        this is only done here for clarity 
    cval('print(foo)', globals=globals(), allowed_calls=["print"])  # Will not be able to access "foo"
foobar()
```

###### Output:
```text
cval.SuspiciousSource: Cval found global variable "foo" in the source, killing for safety.
```

##### Allow some access to global variables
```python
foo = "bar"

def foobar():
    cval('print(foo)', globals=globals(), allowed_global_vars=["foo"], allowed_calls=["print"])
foobar()
```

###### Output:
```text
bar
```

##### Allow access to all global variables
```python
foo = "bar"
bar = "foo"

def foobar():
    cval('print(bar+foo")', globals=globals(), allowed_global_vars=["*"], allowed_calls=["print"])
foobar()
```

###### Output:
```text
foobar
```

##### Block access local variables
```python
def fizzbuzz():
    fizz = "buzz"
    cval('print(fizz)', locals=locals())  # Will not be able to access "fizz"
fizzbuzz()
```

###### Output:
```text
cval.SuspiciousSource: Cval found local variable "fizz" in the source, killing for safety.
```

##### Allow some access to local variables
```python
def fizzbuzz():
    fizz = "buzz"
    cval('print(fizz)', locals=locals(), allowed_local_vars=["fizz"], allowed_calls=["print"])
fizzbuzz()
```

###### Output:
```text
buzz
```

##### Allow access to all local variables
```python
def fizzbuzz():
    fizz = "buzz"
    buzz = "fizz"
    cval('print(buzz+fizz)', locals=locals(), allowed_local_vars=["*"], allowed_calls=["print"])
fizzbuzz()
```

###### Output:
```text
fizzbuzz
```
