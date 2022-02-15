<!-- TOP OF README ANCHOR -->
<a name="top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/ZackeryRSmith/cval/">
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

## About
A decently simple script that uses regular expression to add a layer of protection to eval. Why? Well I keep seeing *"eval really is dangerous"* and *"eval is a bad practice"*. All these statements have some validity to them, but there is almost always a better way to do what you want to acomplish. Cval tackles the *"eval really is dangerous"* mindset, if you must use eval for a public project use cval.

## Exploiting
I **encourage** you to break my script, report even the smallest vulnerabilities in the [issues](https://github.com/ZackeryRSmith/cval/issues), thanks!

## Examples
These examples are focused purely on security rather then real world practical examples.

###### Disable module importing
```python
cval(source='__import__("os")', modules=False)
```

###### Allow certain modules
```python
cval(source='__import__("os")', modules=False, allowed_modules=["os"])
```

###### Disable function calls
```python
cval(source=input(), calls=False)
```

###### Allow certain function calls
```python
cval(source='print("Hello, World!")', calls=False, allowed_calls=["print"])
```

###### Block global variables
```python
cval(source=input(), globals=globals(), gscope=False)
```

###### Block local variables
```python
cval(source=input(), locals=locals(), lscope=False)
```
