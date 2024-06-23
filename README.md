# fix-protocol-support
Create code for ongoing implementation support for FIX protocol.

**Disclaimer**: This was the initial prototype. The beta-friendly version is a private WIP as a possible library to extend existing support. Options 1 and 2 are two separate brainstorms. I have been exploring common protocols used for trading. My eyes are currently set on the FIX protocol. I have been dabbling with possible extensions as a result of some complaints/vents from random forums. I am beginning to form options but this should be an interesting rabbit hole. I realize I should have probably made this into a blog entry but oh well. Signing off! 🫡

# Option 1

This code establishes a FIX connection to a server, sends a logon message, and then enters a loop where it sends a heartbeat message every 30 seconds. You can add additional methods to send and receive different types of FIX messages.

Please note that this is a simplified example and you may need to add additional error handling and features depending on your specific use case.

Also, this code uses the FIX 4.2 protocol, if you need to use a different version, you'll need to adjust the code accordingly. I should maybe make this easier to configure at some point but that could be another rabbit hole. 

You can also use libraries like fix-protocol which is a Python implementation of the FIX protocol, it provides a more comprehensive and robust implementation of the protocol.

```python
pip install fix-protocol
```

You can use it as follows:

```python
import fix

conn = fix.Connection("example.com", 1234, "SENDER", "TARGET")
conn.logon()

while True:
    # Send and receive messages here
    conn.heartbeat()
    time.sleep(30)

conn.logout()
conn.close()
```
This library provides a more complete implementation of the FIX protocol, including support for multiple versions of the protocol, and many other features. This is very clear, so that might be my ongoing preference. 

# Option 2

This code establishes a FIX session with a server, logs on, and then enters a loop where it receives and processes incoming messages. The FIXApplication class provides callback methods for different message types, which can be overridden to implement custom behavior.

Note that this is just a basic example, and a real-world implementation would need to handle many additional details, such as error handling, message validation, and support for multiple message types.

I should check how great the need might be to extend FIX and other trade-related protocols. I might consider making a user-friendly guide or short book with illustrations for these concepts as I start to master them. 

