[![Build][build-image]]()
[![Status][status-image]][pypi-project-url]
[![Stable Version][stable-ver-image]][pypi-project-url]
[![Coverage][coverage-image]]()
[![Python][python-ver-image]][pypi-project-url]
[![License][bsd3-image]][bsd3-url]


# thquickjs

## Overview
TangledHub library for creating context for JavaScript and Python code.
QuickJS is a small and embeddable Javascript engine. 
Safely evaluate untrusted Javascript. 
Create and manipulate values inside the QuickJS runtime. 
Expose host functions to the QuickJS runtime.

## Licensing
thquickjs is licensed under the BSD license. Check the [LICENSE](https://opensource.org/licenses/BSD-3-Clause) for details

## Installation
```bash
pip install thquickjs
```

---

## Testing
```bash
docker-compose build thquickjs-test ; docker-compose run --rm thquickjs-test
```

## Building
```bash
docker-compose build thquickjs-build ; docker-compose run --rm thquickjs-build
```

## Publish
```bash
docker-compose build thquickjs-publish ; docker-compose run --rm -e PYPI_USERNAME=__token__ -e PYPI_PASSWORD=__SECRET__ thquickjs-publish
```

---

## Usage

### Evaluate JavaScript code
Create instance of QuickJS. Use that instance to evaluate JavaScript code. 
JavaScript code can be in string or file.
JavaScript code (variables, functions) can be accessed from quickjs context.
```python
'''
    setup and create instance of QuickJS object
    - eval code function evaluate JS code
    - get function obtain a function from quickjs context
    - js function call in python code

    params:
        eval:
            code: string(js code)
        
        get:
            function_name: str

    returns:
        get:
            function: js function
'''
from thquickjs import QuickJS

# create QuckJS object
qjs: QuickJS = QuickJS()

# example js code
code = '''
    f = function(x) {
        return 40 + x;
    }
    
    f1 = function(x, y) {
        return x + y;
    }
'''

# evaluate JS code
qjs.eval(code).unwrap()

# obtain a function from quickjs context
func = qjs.get('f1').unwrap() # js function in python

# invoke function from JS code in Python code
result = func(2, 3) # returns 5
```

JavaScript code can be in separate file. 
Note that file extension doesn't have to be *.js*.

```python
'''
    setup and create instance of QuickJS object
    - eval code function evaluate JS code from file
    - get function obtain a function from quickjs context
    - js function call in python code

    params:
        eval:
            code: string(js code)
        
        get:
            function_name: str

    returns:
        get:
            function: js function
'''
from thquickjs import QuickJS

# create QuckJS object
qjs = QuickJS()

# value of code is content of file 
code = '''
    f = function(x) {
        return 40 + x;
    }
    
    f1 = function(x, y) {
        return x + y;
    }
'''

file_name: str = 'abc.txt'

with open(file_name, 'r') as reader:
    content = reader.read()

# evaluate JS code
qjs.eval(content).unwrap()

# obtain a function from quickjs context
func = qjs.get('f1').unwrap() # js function in python

# invoke function from JS code in Python code
result = func(2, 3) # returns 5
```

Try to get non-existing variable from context will return None.

```python
from thquickjs import QuickJS

# create QuckJS object
qjs = QuickJS()

# example js code
code = '''
    f = function(x) {
        return 40 + x;
    }
    
    f1 = function(x, y) {
        return x + y;
    }
'''

# evaluate JS code
qjs.eval(code).unwrap()

# try to get non-existing variable from context will return None
func = qjs.get('a').unwrap() # None
```
### Parsing js modules
```python
# create QuckJS object
qjs = QuickJS()

# import lodash
path = os.path.join('/deps', 'thquickjs', 'vendor', 'lodash.js')

# import module by specified path
qjs.import_js_module(path).unwrap()

# use lodash
code = '''
    var a = _.range(10);
    a;
'''

# evaluate JS code
res = qjs.eval(code, as_json=True).unwrap()
# [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```

### Add values to thquickjs context
Variables can be added in thquickjs context.
```python
from thquickjs import QuickJS

# create QucikJS object
qjs: QuickJS = QuickJS()

# set variable and value to context
qjs.set('x', 8).unwrap()

# get value by given variable name
v = qjs.get('x').unwrap() # v is 8

# change value of variable x in context
qjs.set('x', 12).unwrap()

# get value by given variable name
v = qjs.get('x').unwrap() # v is 12

```

Add Python callable in thquickjs context
```python
from thquickjs import QuickJS

# create QucikJS object
qjs = QuickJS()

py_name = 'pylam'
py_func = lambda x: x * 10

# adding Python callable in context
qjs.add_callable(py_name, py_func).unwrap()

# get function by given variable name
f = qjs.get(py_name).unwrap() # v is 8

# result
result = f(5) # returns value of 50
```

### Handling errors
In previous examples, using unwrap() will return appropriate value or rise Exception. 
Using *unwrap_or(v: Any)* or *unwrap_value()* will prevent rising exceptions and terminating program.

Handling errors when parsing JavaScript code
```python
from _quickjs import Object, JSException
from thquickjs import QuickJS

# create QuckJS object
qjs = QuickJS()

# example of unparsable js code
code = '''unparsable js code'''

# standard way to handle exception using try and except blocks
try:
    # evaluate unparsable JS code
    qjs_func: Object = qjs.eval(code).unwrap()
except JSException as e:
    pass

# evaluation of js code and unwraps_value - returns exception as string
qjs_func = qjs.eval(code).unwrap_value()

# unwrap_or method sets default value in case of exception
# qjs_func in case of exception will have default value
qjs_func = qjs.eval(code).unwrap_or('default value in case of exception') 
```

Handling errors when adding Python callable
```python
from thquickjs import QuickJS

## handling errors

# create QucikJS object
qjs: QuickJS = QuickJS()

# handling error with try/except
def add_ten(n: int) -> int:
    return n + 10

py_name = 'pylam'

try:
    # add callable to context
    f = qjs.add_callable(py_name, 'unparsable').unwrap()
except TypeError as e:
    f = add_ten

# handling error with unwrap_value
def add_two(n: int) -> int:
    return n + 2

py_name = 'pylam'

# in case of Err, variable f will contain error message
f = qjs.add_callable(py_name, 'unparsable').unwrap_value() 

# in case of Err, add_two function will be assigned to variable f
f = qjs.add_callable(py_name, 'unparsable').unwrap_or(add_two) 
f(3) # result 5
```

Using unwrap_value() and unwrap_or(v: Any) when there is no exceptions, 
will have no effects on return value.
```python
from thquickjs import QuickJS

# create QucikJS object
qjs = QuickJS()

# set variable and value to context
qjs.set('x', 8).unwrap()

# get value by given variable name
v = qjs.get('x').unwrap() # v is 8

# change value of variable x in context
qjs.set('x', 12).unwrap()

# get value by given variable name
v = qjs.get('x').unwrap() # v is 12

# if unwrap doesn't rise Exception, unwrap_value will return expected value
v1 = qjs.get('x').unwrap_value() # v1 is 12

# if unwrap doesn't rise Exception, unwrap_or will have no effects on return value
v2 = qjs.get('x').unwrap_or(11) # v2 is 12

```
### Set memory limit
Use *set_memory_limit* method to set available memory for thquickjs.
To get informations about memory use *memory* method.
```python
qjs: QuickJS = QuickJS()

qjs.set_memory_limit(memory_limit = 1024000)

# get informations about memory - used, available etc.
res: dict = qjs.memory()
```


### Set time limit
To set time limit in context, use *set_time_limit* method.
```python
qjs = QuickJS()

qjs.set_time_limit(time_limit = 600)
```
## Testing
Run in console:
```bash
docker-compose build thquickjs-test ; docker-compose run --rm thquickjs-test
```

<!-- Links -->

<!-- Badges -->
<!-- Badges -->
[bsd3-image]: https://img.shields.io/badge/License-BSD_3--Clause-blue.svg
[bsd3-url]: https://opensource.org/licenses/BSD-3-Clause
[build-image]: https://img.shields.io/badge/build-success-brightgreen
[coverage-image]: https://img.shields.io/badge/Coverage-100%25-green

[pypi-project-url]: https://pypi.org/project/thquickjs/
[stable-ver-image]: https://img.shields.io/pypi/v/thquickjs?label=stable
[python-ver-image]: https://img.shields.io/pypi/pyversions/thquickjs.svg?logo=python&logoColor=FBE072
[status-image]: https://img.shields.io/pypi/status/thquickjs.svg

