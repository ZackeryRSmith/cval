<!-- TOP OF README ANCHOR -->
<a name="top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/ZackeryRSmith/cval/blob/main/cval.png">
    <img src="https://github.com/ZackeryRSmith/cval/blob/main/cval.png" alt="Cval logo" width="155" height="155">
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
I **encourage** you to break my script, report even the smallest vulnerabilities in the [issues](https://github.com/ZackeryRSmith/cval/issues), thanks!

## Examples
These examples are focused purely on security rather then real world practical examples.

##### Disable module importing
```python
cval(source='__import__("os")', calls=False, modules=False)
```

###### Output:
```text
cval.IllegalSource: Cval panicked due to an illegal module import in source!
```

##### Allow certain modules
```python
cval(source='__import__("os")', calls=True, modules=False, allowed_modules=["os"])
```

##### Disable function calls
```python
cval(source='print("Hello, World!")', calls=False)
```

###### Output:
```text
cval.IllegalSource: Cval panicked due to an illegal function call in source!
```

##### Allow certain function calls
```python
cval(source='print("Hello, World!")', calls=False, allowed_calls=["print"])
```

##### Block global variables
```python
foo = "bar"
# You may also add "global foo". Due to the current scope we don't need to though

def foobar():
  cval(source="foo", globals=globals(), gscope=False)  # Will not be able to access "foo"
```

###### Output:
```text
cval.SuspiciousSource: Cval found global variable "foo" in the source, killing for safety!
```

##### Block local variables
```python
def foo():
  bar = "foobar"
  
  cval(source='bar', locals=locals(), lscope=False)  # Will not be able to access "bar"
```

###### Output:
```text
Cval found local variable "bar" in the source, killing for safety!
```
