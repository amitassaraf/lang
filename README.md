Lang - Python Language Constraints
=============================

Lang is a Python module that allows enforcing programming language constraints. Lang was built using a Java like mindset, so many of the constraints that are supported are mirrors of constraints in the Java programming language.

Features:

 - Access Modifiers
	 - Private & Protected modifiers
	 - Protect variables, properties, getters and setters
 - Class decorators, Meta classes, Base classes to enforce constraints
 -  Interface classes (Only signatures & class members)
 - Abstract classes, methods, properties
 - Final classes (& methods WIP)

Examples:
--------------
**Protected/Private members**

*Private variables can only be accessed by the same class while protected variables can also be accessed by subclasses. *

    class Box(object):
	    __metaclass__ = EnforceProtectedMeta
	    
	    def __init__(self):
	        self._cant_touch_this = 7
or
    
    @enforce_protected
    class Box(object):
	    
	    def __init__(self):
	        self._cant_touch_this = 7
or
    
    class Box(EnforceProtected):
	    
	    def __init__(self):
	        self._cant_touch_this = 7
Private is that same as protected but exchange 'protected' with 'private'.  Private variables are variables that begin with an '\_' and end with an '\_',  for example:  \_i_am_private_for_this_class\_

**Protected/Private properties**

    class Box(object):
	    @protected_property
	    def size(self):
		    ...
		
		@size.setter
		def size(self, value):
			...
Protected setter/getter only

    class Box(object):
	    @protected_setter_only
	    def size(self):
		    ...

		@size.setter
		def size(self):
			...
**Interface Classes**

An interface is a class that can only implement function signatures and class members.

    class IBox(Interface):
	    # or __metaclass__ = EnforceInterfaceMeta
	    DEFAULT_HEIGHT = 10
	    
	    def size(self):
		    pass
		    
		def calculate_volume(self):
			pass
			
If a function is implemented that it's source is not only 'pass' then an exception is thrown.

**Abstract Classes**

This exists already in python  (abc module) so I just wrapped it to be in the same package.

    class Box(Abstract): 
	    # or __metaclass__ = EnforceAbstractMeta
	    
	    @abstract_method
	    def i_am_abstract(self):
		    ...
		
		@abstract_property
		def size(self):
			...

**Final Classes**

Final classes are classes that cannot be subclassed

    class TheBestBox(object):
	    __metaclass__ = FinalClassMeta

Installation
----------------

Either install from pip:

    pip install lang

or clone the git repo and run:

    python setup.py install

License
----------
This module is under [Apache 2.0](http://www.apache.org/licenses/LICENSE-2.0) license. 


Contact Me
----------------

If you have any ideas or suggestions or bugs, please do contact me!

LinkedIn: Amit Assaraf

Email: amit@helpi.me
