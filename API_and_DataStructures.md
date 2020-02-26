# API and DataStructures
here will be explained how the API works, what it needs to work and what it's give you.

## DataAPI
This API is made with flask and used to comunicate with the Database
### structures
because of library limitations, the api usage is a pain is the __***__.
every request will have to provide (even if it's empty) a string called `data` representing a `stringify`_ed (?)_ json containing all of the arguments the server needs.

__exemple__:
empty data:
```json
https://foo.dev/bar?data="{}"
```
rebuild request:
```json
https://foo.dev/rebuild?data="{\"radius\":3}"
```
sorry about that...

### API
Warning : this is not finished at all
#### /debug/rebuild
will drop the database and rebuild it with random but valid blocks. debug purpose only
```json
data = {
	"radius": 3
}
```
#### /listeTypeBlocks
```json
data = {
	"chunk":[{"x":2, "y":1, "z":2}],
	"filter":{},
	"dim":"overworld"
}
```

#### /identify
```json
data = {
	"name": "air",
	"mod": "minecraft"
}
data = {
	"fullname":"minecraft:air"
}
data = {
	"id": "5e55e995f0ac096ddbae1914"
}
```
#### /getRef
```json
data = {
	"filter":{}
}
```

## TurtleAPI
This _API_ is what will use robots and drones to comunicate with the backend.

First thing to say about it : ___it's not a api lol___
turtles work with sockets ([the low-level ones](https://ocdoc.cil.li/component:internet)) so it's technicly not a API... but who cares ? this module is called TurtleAPI anyway :)
### Protocole
the communication works like that:


```
Once connected, a KeepAlive ping is send every 2 seconds of inactivity.
if it time out, the socket will reset itself

Every pkg is structured in 3 parts :
the first  byte will be the order to execute (see below for more info)
the second byte will be the len of the third part
the third part is what ever the order needs to works.

exemple :
--change your color to blue--
[ 0x04 | 0x03 | 0x00 | 0x00 | 0xFF ]

--change status text--
[ 0x01 | 0x0B | H | e | l | l | o |   | W | o | r | l | d ]

--get position--
[ 0x03 | 0x00 ]

note that this model can't send more than 255 byte of data for the third part. but this should never be needed
```

### orders

```
0x00 close/reset socket
0x01 set status text. will try to read and display the third part
0x02 move to. will try to read 3 ints (x, y, z) on the third part
0x03 get position
0x04 set light color. will try to read 3 ints (r, g, b) on the third part
0x05 scan (WIP). will try to read 3 ints (x, y, z) on the third part

0xFF ping ...... pong ?
```

#### 0x00 close/reset socket
Will just restart the socket. (not the entire computer)
#### 0x01 set status text (drone)
Will try to change the status text.
A string must be provided in the third part.
_note that it will crash if no third part is provided_
#### 0x02 move to (drone)
_still WIP_
Will execute [`drone.move()`](https://ocdoc.cil.li/component:drone).
3 ints (32bits) must be provided in the third part (x, y, z).
_note that it will crash if no third part is provided_
#### 0x02 move to (robot)
_WIP. nothing available for now._
#### 0x03 get position (drone)
With the help of the [debug card](https://ocdoc.cil.li/component:debug) (for now but it might change). The drone Will send back his position via the socket with a string :
```
"2431|78|234"
 "x  |y |z  "
```
#### 0x04 set light color (drone/robot)
Will execute [`(drone or robot).setLightColor()`](https://ocdoc.cil.li/component:drone).
3 bytes must be provided in the third part (r, g, b).
_note that it will crash if no third part is provided_
#### 0x05 scan (drone)
Still in work for a proof of concept.
I dunno if I should make it scan a entier chunk or just a single block.
I dunno if I should give it the nbt or the meta
I dunno how I will structure it... pffffffffffff
_What do I know exactly ?_
anyway ! _WIP. nothing available for now._
#### 0xFF ping (drone/robot)
pong ?
