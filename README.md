# 2 Player Asteroids

This game allows 2 players to play against each other on the classic arcade game: asteroids.

This works on a shared local network but can easily be configured to be hosted. It uses thge following techniques:
* sockets (second player addition)
* threads (second player addition)
* Queue (Artificial Network Delay) on server
* pygame frame rate (Bucket Synchronization) on client
* Dead Reckoning - If a player goes offline and then re connects, then their original id is assigned back to them

This project uses the code from the following github repository as a base:

https://github.com/aminb/asteroids

The following files have been copied from the above repository:

* images/*
* game.py

The following files I have added:
* network.py
* server.py
* run_client.py
* run_server.py
* README.py

I have also added the following functions to the original game.py:
* send_data (second player addition)
* parse_data (second player addition)
* update_object_positions (second player addition)

To run the game, the server first needs to be started:
```
python server.py
```
Then for Player 1 to join the game:
```
python run_client.py
```
Player 2 can run the same command to join the same game as player 1.
