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


## Examples
Some examples focused purely on security rather then real world practical examples.

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
