######
hueber
######

************
description.
************

Hueber is a fully type-checked Python API for the Philips Hue lighting system. Tooling is also included which enables you to declare update statements (also type-checked) and which can then be safely and efficiently pushed to a Philips Hue Bridge. You are free to use either parts of ``hueber`` together or seperately that is up to you (e.g. use the state builder tools with another API).

please note!
============

That as of now this does not cover the full Philips Hue API and only covers ``/lights``, ``/groups`` and ``/config``. It would not take much work to add them but its just not a prioritiy for me now.

**************
prerequisites.
**************

* Python 3.6 (re: static typing annotation)
* Philips Hue bridge ver2 (I have not tested this with the first generation) connected to your local network

****************
getting started.
****************


Open a REPL and start with instantiating a ``Bridge()`` by passing it the local IP address::

    >>> hue = Bridge("192.168.0.5", "r3aLLy-L0nG-Us3RName-H3r3")
    >>> print(Bridge)
    Bridge(192.168.0.5, xxxxx...-H3r3)

note:
=====

Philip's providse documenation on how to find your bridge on your network. Please consult `their documentation <https://developers.meethue.com/documentation/getting-started>`_.

From here all your lights and groups are accessible via the Bridge type (I have only shown an abridged version of the output below)::

    >>> print(hue.lights)
    {1: Light(1, Bedroom Dresser, ... ), 5: Light(5, Kitchen Cabinets, ... ) ... }
    >>> print(hue.groups)
    {1: Group(1, Kid's Bedroom, ...), 3: Group(3, Kitchen, ...) ... }

As you can see above the ``Bridge.lights`` and ``Bridge.groups`` attributes are a collection. An individual ``light`` or ``group`` can be accesed via its index which is the ID given to it by the Philips Hue Bridge::

    >>> hue.lights[1]  # select light with id 1
    Light(1, Coffee Station, Dimmable light)
    >>> hue.lights[1].data  # return a dict of all its attributes
    {'state': {'on': False, 'bri': 77, 'alert': 'select', 'reachable': True},
    'type': 'Dimmable light', 'name': 'Coffee Station', 'modelid': 'LWB014',...
    }

This is all well and good but what if you want to change the state or your light or group? Use the Light-/GroupBuilders to easily construct update strings::

    >>> from hueber.lib import LightBuilder
    >>> new_update = LightBuilder()
    >>> new_update["on"] = True
    >>> new_update["bri"] = 254
    >>> hue.lights[1].push(new_update.update_str())
    [{'success': {'/lights/1/state/on': True}}, {'success': {'/lights/1/state/bri': 254}}]

All ``*Builder`` types are just a ``dict`` underneath so all of the methods and idioms you use for a ``dict`` should be available to a ``Builder``.

**************
going further.
**************

This code is particularly well documented (I think) so please dig into the source if you have any more questions or, if you think something really does need further explanation open an issue and I will do my best to updated the README.

*************
contributing.
*************

I am happy to accept a pull request, look into the TODO.rst file for gaps or features I am looking to implement down the road. Please make sure any PRs are off of the ``dev`` branch otherwise it will just not be accepted and be sure to include your name/handle in the contributors file. Additionally, make sure you run ``mypy`` over the project directory.

