==============
Axessy
==============

Axessy is a simple package to read and parse messages from AXESS TMC X3 devices.

ChangeLog
-------------

    * 0.3: Fixed message() method
    * 0.1: First release

Installation
-------------

There are two ways to install the package:

1. Using pip with the following command:
    
    pip install axessy

2. Start setup.py file from this repository:
    
    python setup.py install
    
Usage
-------------
You can import the module in the following way:

    import axessy.axessy
    
In this package there is the "AxessPackage" class defined with the following methods:

    * parsePacket(params): "params" includes the GET parameters sent via an "/online" or "/batch" command from the device, and stores the data inside the class variables;
    
    * message(msg, beep=100, show=2): builds a string that you can put inside an HttpResponse to send back to the device;
    
    * sendKeepAlive(url, username, password): asks the device to send a keepalive message.
    
Also the "AxessPackage().ack" and "AxessPackage().keepalive" variables are defined for string responses to "/batch" and "/keepalive" commands.

A dictionary with all possible errors saved into a transaction, "AxessPackage().error_dict", is defined and automatically used by "parsePacket" method.

Finally there are two new Error classes used by the "checkPacket()" method (this method is used by "parsePacket" automatically):

    * MacAddressError
    
    * CardError