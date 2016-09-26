## COMMANDS
* abuse 150
* whoall
* list down nodes

## INFRASTRUCTURE
Ideally, LCMbot should have to do as little as possible to deliver its services.
LCMbot should only serve as an easy point of access to information.
LCM should provide this information to LCMbot in a machine-friendly format,
possibly through an API only reachable from within LCM network.

For example, this is my idea of how this would go down for `whoall`:
LCMbot is running on a VM, inside LCM network. It communicates with telegram 
bot API via http, and http is its only link to the outside world. When LCMbot
receives the `/whoall` command, it interrogates a running service inside LCM
network and retrieves machine readable information on who is connected where.
LCMbot's only concern is reshaping the data in a human readable form and send
it as a telegram message.
