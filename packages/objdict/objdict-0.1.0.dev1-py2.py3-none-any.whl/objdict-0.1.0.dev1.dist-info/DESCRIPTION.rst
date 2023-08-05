=========
 ObjDict
=========

Uses_.
------
Why an 'ObjDict'?  The reasons include:
    - the 'swiss army knife' class
    - support for json message encoding and decoding
    - ObjDict in place of dictionaries as a convenient ad-hoc data structures
    - mutable equivalent to nametuple (or namedlist)
    - adding json serialization to classes

Background_.
------------
    - Mulitple Uses of Dictionaries
    - history of the ObjDict

Instructions_.
--------------
    - General Notes and Restrictions
    - Instancing and json load
    - str representation and json dumps
    -

Uses
-----
The swiss army knife class.
+++++++++++++++++++++++++++

As described in this 'uses' sections, the ObjDict class has many uses, and can
be used in place of namedtupples, namedlists, OrderedDict objects as well as
for processing Json data.  One sinlge import gives all this flexibility.

The one trade-off for this flexibiliy compared to using the individual specialised
classes is performance. If you have performance critical code that is used in
massively iterative code then, for example, namedtuples are far better if they
provide all the functionality you require.

Support for json message encoding and decoding
++++++++++++++++++++++++++++++++++++++++++++++

Where an application has the need to build json data to save or transmit, or
to decode and process json data loaded or recieved, the ObjDict structure provides all
the tools to achive this with clear Object oriented code.  This usage has different
requirements than json serialisation (as disccussed below), as it is necessary
to be able to produce not just a json representation of an object,  but create
objects that can desribe any possible
arbitary json data. For example, the order of fields may be signifcant in a
json message, although field order may not be significant for serialisation. The ObjDict class has
the tools to produce exactly the json data required by any application, and to decode
any possible incomming json messages for processing.  It was for this usage that
ObjDict was intially developed.

ObjDict in place of Dictionaries for Ad-hoc data structures.
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
See the text below on 'mulitple uses of dictionaries' for background.
There is a significant amount of code where dictionaries have been used for
ad-hoc structures. The use case often arises where it can become useful if
these data structure can have elements accessed in the simpler are many

Mutable Equivalent To NamedTuple
++++++++++++++++++++++++++++++++
There are occasions where a 'namedtuple' cannot be used due to the need for
mutable objects.  The ObjDict also fulfills this need and can be intialised
from list data.  There are many other classes that also fill this need, but
the ObjDict combines this functionality with json processing, with dictionary
access to data and other functions.

Json Serialisable Objects.
++++++++++++++++++++++++++
Applications that have a need to serialise objects in order to restore those
objects either within the same application, or in an application connected
through a datalink, may desire json as the format for object storage or object
message format.  The ObjDict class and module provides the tools for this,
serialising the state of an object in order for that state to be later
loaded, either by an identical class, or a different class which has use
for some or all of the same 'object state' information.

OrderedDict alternative.
++++++++++++++++++++++++
OrderedDicts do everything dictionaries can, and in some applications it can
be useful to simply move to OrderedDict classes for all dictionaries.  'ObjDict'
is another alternative, with a shorter name, even more flexibiliy and power,
and a much more readable 'str' representation that can also be used for clearer
initialisation. See instructions for details on 'str' and initialisation
flexibility.

Background
----------
History and acknowledgement.
++++++++++++++++++++++++++++
The project was emerged from a need for code to generate and decode json
messages. Originally the package `jsonweb <http://www.jsonweb.net/>`_.  was
selected for the task, but it became clear the use case differed. 'jsonweb' is
ideal for representing classes as json, and reloading classes from that json
and provides validation and tests and schema that are not reproduced in ObjDict.
However ObjDict provides specifically for classes created to generate or process
json as data, as
opposed to json as a representation of the class, and now the ObjDict
class with a wider range of uses. The whole issue of json data which ambiguously
may correspond to either a dictionary collection, or an object, arises from
general processing of json data and gives rise to the ObjDict. The ObjDict
project started out to add more control
over json as a fork of jsonweb, but evolved over time to the different use cases.

ObjDict vs jsonweb
++++++++++++++++++


Multiple Uses of Dictionaries.
++++++++++++++++++++++++++++++
In python, dictionaries are designed as 'collections' but are often used as
ad-hoc structures or objects.  In a true collection, the key for an entry does
not indicate properties
of the value associated with the key. For example, a collection of people,
keyed by names,
would not normally infer the significance or type of data for each entry
(or in this case person) by the key.  The data has the same implications regardless
of whether the key is 'bob' or 'jane'. The data associate with 'bob' or 'jane'
is of the same type and is interpreted the same way.
For an 'ad-hoc' structure the keys **do** signal both the nature of the data and
even the type of data.
Consider for each entry for a person we have a full name,  and age.
A dictionary could be used to hold this information, but this time it is an
ad-hoc structure.  As a dictionary we always expect the same two keys, and each
is specific to the information and different keys even have different types of data.
This is not a dictionary as a collection, but as an ad-hoc structure. These are two
very different uses of a dictionary, the collection the dictionary was designed for,
and the ad-hoc structure or ad-hoc object as a second use.

Introducing the ObjDict.
++++++++++++++++++++++++
An ObjDict is a subclass of dictionary designed to support this second
'ad-hoc object' mode of use. An ObjDict supports all normal dict operations, but
add support for accessing and setting entries as attributes.
So::

    bob['full_name']= 'Robert Roberts'
        is equivalent to
    bob.full_name = 'Robert Roberts'

Either form can be used. ObjDicts also have further uses.

Multiple modes of Dictionary Use and JSON
++++++++++++++++++++++++++++++++++++++++++
The standard json dump and load map json 'objects' to python dictionaries.
JSON objects even look like python dictionaries (using {}
braces and a ':'). In javascript, objects can also
be treated as similar to dictionaries in python.  The reality is some json
objects are best represented in python as objects,  yet others are best
represented as dictionaries.

Consider::

    { "name": {"first":"fred", "last":"blogs"}
     "colour_codes":{"red":100,"green":010, "yellow":110, "white":111 }
    }

In this data, the 'name' is really an object but the 'color_codes' is a
true dictionary. Name is not a true dictionary because it is not a collection
of similar objects, but rather something with two specific properties.
Iterating through name does not really make sense, however iterating through
our colours does make sense. Adding to the collection of colours and their
being a variable number of colours in the collection is all consistent.
Treating 'name' is not ideal as the 'keys' rather than being entries in a collections
each have specific meaning.  Keys should not really have meaning, and these keys
are really 'attributes' of name, and name better represented as an object.

So two types of information are represented in the same way in json.

Another limitation of working with python dictionaries and JSON is that in messages
order can be significant and but dictionaries are not ordered.

The solution provided here is to map JSON 'objects' to a new python ObjDict
(Object Dictionaries).  These act like OrderedDictionaries, but can also be treated
as python objects.

So 'dump' or '__json__()' or 'str() / __str__()' of the 'names' and
'colour_codes' example above produces an
outer ObjDict containing two inner 'ObjDict's,  'name' and 'colour_codes'.
Assume the outer ObjDict is assigned to a variable 'data'
Each obj dict can be treated as either an object or a dictionay, so all the code
below is valid::

    data= ObjDict(string_from_above)
    name = data['name'] #works, but as 'data' is not a real 'dict' not ideal
    name = data.name  #better
    first_name = data.name.first
    first_name = data["name"]["first"]  #works but again not ideal

    red_code = data.colour_codes["red"]
    #as colour codes is a true collection it will be unlikely to set
    #members to individual variables, but the code is valid

ObjDict items also 'str' or 'dump' back to the original JSON as above.
However if the original string was changed to::

    { "name": {"first":"fred", "last":"blogs", "__type__": "Name"}
     "colour_codes":{"red":100,"green":010, "yellow":110, "white":111 }
    }

The json 'load' used to load or intitalise ObjDict uses an object_pairs_hook
that checks a table of registered class names and corresponding classes.

If there is an entry in the table, then that class will be used for embeded objects.
Entries with no __type__ result in ObjDict objects, and if the 'DefaultType' is
set then a class derived from the default type, with the name from the value
of '__type__' will be returned.  If 'DefaultType' is None, then an exception will
be generated.
See the instructions section for further information.


.. _Instructions:

Instructions.
-------------
 - `General Notes and Restrictions`_.
 - `Initialisation and json load`_.
 - str and json dumps
 - custom classes and json


General Notes and Restrictions
+++++++++++++++++++++++++++++++
Since ObjDict keys do not have to be valid attribute names (for example an
integer can be a dictionary key but not an attribute name, and dictionary keys
can contain spaces), so not all
key entries can be accessed as attributes. Similarly, there are attributes
which are not considered to be key data, and these attributes have an underscore
preceding the name.  Some attributes are part of the scaffolding of the ObjDict
class and these all have a leading underscore, as well as a trailing underscore.
It is recommened to use a leading undercore for all class 'scaffolding' added as
extentions to the ObjDict class or to derived classes, where this scaffolding
is not to be included as also dictionary data.


Initialisation and json load
+++++++++++++++++++++++++++++
ObjDict can be intialised from lists, from json strings, from dictionaries,
from parameter lists or from keyword parameter lists.

Initialisation From Lists or Parameter Lists.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Intitialisation from a list of key value pairs, as with OrderedDict class is
supported.  Beyond key value pairs, there is also support for direct initialisation
from lists. The _keys parameter must be included for initialisation from lists.
Also, Classes
derived from ObjDict can have _keys as a class attribute, providing an similar
use pattern to the 'namedtuple'.  '_keys' can be either
a list of strings, or a string with space or comma separated values. When
initialising from a list or parameter list, the list size must match the number
of keys created through '_keys',  however other items can be added after
initialisation.

So this code produces True::

    class XY(ObjDict):
        _keys='x y'

    sample = XY(1,3)
    sample.x,sample.y == 1,3

Alternatively form to produce a similar result but with the SubClass would be::

    sample= ObjDict(1,3,_keys='x y')
    sample= ObjDict([1,3],_keys='x y')

Initialisation from Json Strings.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
For more complex intitialisation, json strings can provide an ideal solution.
This allows for complex structures with nested embeded 'ObjDict' or other objects

The background section ``

Initialisation from dict, OrderedDict, or key word arguments.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

str and json dumps.
+++++++++++++++++++
A limitation with OrderDict objects is that 'str' represenation can be clumsy
when the structure is nested.

Both the 'str' and 'json' methods of the ObjDict class produce json output which
remains clear regardless of nested structures.

Custom classes
++++++++++++++
Custom classes allow for json data to result in instantiating objects other
than ObjDict from json data.  These custom classes can be subclassed from ObjDict
or built from first principles.


eading data directly into a class with appropriate
methods to manipulate data, and can also customise how data is written back as JSON.

Such classes can be subclassed from ObjDict but do not need to be.

For a 'dummy' class which is just a dict use::

    @decode.from_object()
    class Sample(ObjDict):
      pass

A simple introduction/migration is to leave 'combiParse' still treating
objects as dictionaries by using the  no__type__=True parameter.
This allows an app to use its own code to convert dictionaries into object,
but still benefit from unParse being able to generate JSON directly from objects.

E.g. if you have::

    { "name":{
            "first": "joe",
            "last": "foo"
        }
    }
    #now code
    @objdict.from_json()
    class Name:
        def __init__(self,first=None,last=None,**kwargs):
            self.first=first
            self.last=last


Read with::

    combiParse(string)

then convert the name
dictionary into an object and put that object back in the original tree::

    tree=combiParse(string)
    tree['name'] = Name(**tree['name'])  # kwargs!!! i.e. "**" required :-)

The result would be 'unParsed' ::

    { "name":{
            __type__: "Name"
            "first": "joe",
            "last": "foo"
        }
    }


Decoding automatically to objects can then be added at a later time.

Note: using '@decode.from_object()' instead of '@decode.from_object()'
results in all of the json being passed as a single dict paramter,
not just parameters listed in the 'init',
being in the call to instance the object.
This means the 'JSONSimpleHandler' needs a \*args in the signature.  We also
need the same solution when decoding manually as in the migration example.

Maintaining Order With Custom Classes and Defaults.
+++++++++++++++++++++++++++++++++++++++++++++++++++
ObjDict classes and automatically created classes currently maintain key order,
but of course cannot provide for default values for attributes.

Custom classes can specify default values for attributes, but currently custom
classes do not automatically maintain order, even if based on ObjDict classes.

Maintaining order and supporting default values are available with an __init__
method.  Note, the order attributes are set will be their order in a message.
Classes subclasses from ObjDict will have '__type__' at the end of json output.

If a custom class is decorated with @decode.from_object(JSONSimpleHandler),
then all fields in the raw JSON will be sent in a single dict. Of course, as
a dict order is lost and also there are no default values.
The recommended code for the init is something like this::

     @objdict.from_json()
     class Custom(ObjDict):
        def __init__(self,*args,**kwargs):
            super(Custom,self).__init__()
            if args:
                arg0=args[0]
                assert len(args)==0, "unexpected argument"
                self.arg1=arg0.pop('arg1',default)
                self.arg2=arg0.pop('arg2',default)
                ........
                self.update(arg0)
            self.update(**kwargs)

Life is much simpler with @decode.from_object(), but at the expense of ignoring
any unexpected arguments.  Currently \*\*kwargs will always be empty in this case
but a future update will likely address this.  Example::

    @decode.from_object()
    class Custom(ObjDict):
       def __init__(self,arg1=None,arg2=None ....,**kwargs):
           super(Custom,self).__init__()
           self.arg1=arg1
           self.arg2=arg1
           ........
           self.update(**kwargs) #currently kwargs will be empty


All that is needed as imports is above.

This system supports both 'ObjDict's and custom classes.  In JSON representation
a __type__ field is used to indicate actual type.  For your own classes use::

    @encode.to_object()
    @decode.from_object()
    class Sample:
        def __init(self,p1,p2,...):
            self.p1=p1
            self.p2=p2
            ....

to map between::

    { "p1": 1, "p2":2, "__type__": "Sample"}
        and
    Sample(1,2)

However simple examples such as this could also use the default 'ObjDict' objects.


