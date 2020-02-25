# OpenBrother(WIP)
This project aim to create a dynamic mapping system of a minecraft world using the [OpenComputer](https://github.com/MightyPirates/OpenComputers).


## more prescitions ?
3 parts are to understands :

### the server side
this side have the work to:
- store and update all the data send by the _game side_ using the database [MongoDB](https://www.mongodb.com/fr)
- provide informations to the _front_ and _game side_  with APIs using [Flask](https://github.com/pallets/flask) 
- run a pathfinding algotism ([A*](https://fr.wikipedia.org/wiki/Algorithme_A*)) in the 3D world using the data from the database

##### warning
This side is ment to run on a raspberry pi 3+ using [ubuntu server 64bits](https://ubuntu.com/download/raspberry-pi)
some difficulty to install mongodb on a 32bits system are to be expected as it's no more supported by the devs

### the front side
**TODO**

### the game side
using robots from OpenComputer (that we call _turtle_ because we are used to [ComputerCraft](http://www.computercraft.info/)), we send to the _server side_ every block that we can so the player can program another _turtle_ to (for exemple) mine for him every of a certain block in an area.



# creadits

| Name | Email |
| ------ | ------ |
| Gaspard Bettinger | bettinger.gaspard@gmail.com |
| TODO | TODO |