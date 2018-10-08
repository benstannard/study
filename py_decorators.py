# Check out amazing  article: https://dbader.org/blog/python-decorators


from functools import wraps
# You can use functools.wraps in your own decorators to copy over the lost metadata from the undecorated function to the decorator closure.
# Applying functools.wraps to the wrapper closure returned by the decorator carries over the docstring and other metadata of the input function
# As a best practice I’d recommend that you use functools.wraps in all of the decorators you write yourself.


# What is a decorator?
"""
They "wrap/decorate" another function and let you execute code before after the wraped function runs.
Decorators can be used to inject additional functionality to one or more functions.

Decorators allow you to define reusable building blocks that can change or extend the behavior of other functions.
And they let you do that without permanently modifying the wrapped function itself.
The function’s behavior changes only when it’s decorated.

When you use a decorator, really what you’re doing is replacing one function with another.
One downside of this process is that it “hides” some of the metadata attached to the original (undecorated) function.

For example, the original function name, its docstring, and parameter list are hidden by the wrapper closure.
You can use functools.wraps in your own decorators to copy over the lost metadata from the undecorated function to the decorator closure.

Multiple decorators on a single function are applied bottom to top (decorator stacking). The top decorator decorates the function that results from the decorators below it.
"""



def greet(): return 'Hello!'

# Slightly more complex decorator which converts the result of the decorated function to uppercase letters.

def uppercase(func):
    def wrapper():
        original_result = func()  # Technically, you do not need this step
        modified_result = original.result.upper()
        return modified_result
    return wrapper

"""
Instead of simply returning the input function, this uppercase decorator defines a new function on the fly (a closure) and
uses it to wrap the input function in order to modify its behavior at call time.

The wrapper closure has access to the undecorated input function and it is free to execute additional code before and after calling the input function.
(Technically, it doesn’t even need to call the input function at all.)

@uppercase
def greet():
    return 'Hello!'

>>> greet()
'HELLO!'
"""

# Tack on
"""
uppercase defines and returns another function (the closure) that can then be called at a later time, run the original input function, and modify its result.
Decorators modify the behavior of a callable through a wrapper so you don’t have to permanently modify the original.
The callable isn’t permanently modified—its behavior changes only when decorated.

This let’s you “tack on” reusable building blocks, like logging and other instrumentation, to existing functions and classes. 
It’s what makes decorators such a powerful feature in Python that’s frequently used in the standard library and in third-party packages."""


# Applying Multiple Decorators to a Single Function
def strong(func):
    def wrapper():
        return '<strong>' + func() + '</strong>'
    return wrapper

def emphasis(func):
    def wrapper():
        return '<em>' + func() + '</em>'
    return wrapper

@strong
@emphasis
def greet():
    return 'Hello!'

>>> greet()
'<strong><em>Hello!</em></strong>'

# If you break the above code down...
# decorated_greet = strong(emphasis(greet))





# Decorating Functions That Accept Arguments
"""
All examples so far only decorated a simple nullary greet function that didn’t take any arguments whatsoever. 
So the decorators you saw here up until now didn’t have to deal with forwarding arguments to the input function.
If you try to apply one of these decorators to a function that takes arguments it will not work correctly."""

# How do you decorate a function that takes arbitrary arguments?
"""
*args and **kwargs
feature for dealing with variable numbers of arguments comes in handy.
The following proxy decorator takes advantage of that."""

def proxy(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

# Let's expand
def trace(func):
    def wrapper(*args, **kwargs):
        print(f'TRACE: calling {func.__name__}() '
              f'with {args}, {kwargs}')

        original_result = func(*args, **kwargs)

        print(f'TRACE: {func.__name__}() '
              f'returned {original_result!r}')

        return original_result
    return wrapper


@trace
def say(name, line): return f'{name}: {line}'

>>> say('Jane', 'Hello, World')
'TRACE: calling say() with ("Jane", "Hello, World"), {}'
'TRACE: say() returned "Jane: Hello, World"'
'Jane: Hello, World'


# How to Write “Debuggable” Decorators.
from functools import wraps

def uppercase(func):
    @wraps(func)
    def wrapper():
        return func().upper()
    return wrapper
