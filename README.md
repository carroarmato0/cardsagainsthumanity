# Cards Against Humanity

[![Build Status](https://travis-ci.com/carroarmato0/cardsagainsthumanity.svg?branch=main)](https://travis-ci.com/carroarmato0/cardsagainsthumanity)

This is a Python implementation I'm making while learning the language.

This project will have three components:
- DeckAPI
- DeckManager
- Cards Against Humanity game

## DeckAPI
The DeckAPI is a microservice implemented using [Bottle](https://bottlepy.org/), a Python Web Framework, and uses MongoDB as a Document storage backend. This API allows anyone to fetch existing card Decks as JSON objects, as well as upload their own.

## DeckManager
The DeckManager is a Bootstrap 5 web frontend implemented using [Bottle](https://bottlepy.org/), and uses plain Javascript to talk to the DeckAPI.
While not a requirement, it exists to interact with the DeckAPI in a user friendlier way.

## Cards Against Humanity game
This is an implementation of the game. It uses websockets to communicate with a server instance and to synchronise the game state among the players.
Players can choose among a default set of card Decks, and add additional ones by entering the codes of the ones registered with the DeckAPI.

## Roadmap
Since this is a personal project, no time-frame is put in place, however, there are milestones that can be reached.

* ~~Implement a basic library to represent cards and decks~~
* Implement the DeckAPI
  * ~~Getting all Decks~~
  * ~~Getting a specific Deck~~
  * ~~Create a Deck~~
  * ~~Adding cards to a Deck~~
  * ~~Removing cards from a Deck~~
  * ~~Delete a Deck~~
  * Unit Tests for API
* Implement the DeckManager
  * ~~Overview of Decks.~~
  * ~~Show specific Deck~~
  * Delete specific Deck
  * Add cards to Deck
  * Remove cards to Deck
  * Edit Cards
  * Edit Deck
  * Export/Import of Decks
  * Finish design
  * Docker Container
  * Functional tests
* Implement the basic game.
  * Lobby
  * Selection of Decks
  * Filtering of Cards
  * Game Logic
  * Docker Container
  * Functional tests
