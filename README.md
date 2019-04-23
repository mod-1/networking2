# Networking2
Goal: Create an reliable messaging client over a UDP.

Limitations: 

1. Delivers only 1 packet at a time. Could increase efficiency by introducing a pipeline.

2. The server(Bob.py) has not been programmed to handle concurrent connections. Also it needs to be manually closed using 'Ctrl ^ C'.

3. Since the application could be tested easily, file redirection has bee used, hence if the user wants to test it on the terminal itself, the input for Alice.py must end with the EOF char i.e. after typing in the message, go to a newline and press 'Ctrl ^ D'.

How to test: 

1. Run Bob.py first as it is the server.

    Command: `python3 Bob.py <rcvPort no.\> > output.txt`

2. Then run the UnreliNET, this simulates the unreliable channel as all packets that are transmitted between Alice and Bob go through UnreliNET which introduces bit errors and drops packets at random.

    Command: `java UnreliNET <pr1\> <pr2\> <pr3\> <pr4\> <UnreliNET port\> <rcvPort no.\>`
    
    pr1: Probability of packet corruption from Alice to Bob [Permissible values: 0.0 - 0.3]
    
    pr2: Probability of dropping packet from Alice to Bob [Permissible values: 0.0 - 0.3]
    
    pr3: Probability of packet corruption from Bob to Alice [Permissible values: 0.0 - 0.3]
    
    pr4: Probability of dropping packet from Bob to Alice [Permissible values: 0.0 - 0.3]

3. Finally run the Alice.py as it is the client

    Command: `python3 Alice.py <UnreliNET port \> < input.txt`
    
4. After the execution is completed run: `cmp input.txt output.txt`