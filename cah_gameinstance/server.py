import json
import os
import uuid
from datetime import datetime
from json import JSONDecodeError
from random import shuffle

import bottle
from bottle import static_file
from bottle_websocket import GeventWebSocketServer, websocket
from geventwebsocket import WebSocketError
from pip._vendor import requests

from cah.card import Card
from cah.cardtype import CardType
from cah.deck import Deck
from cah_deckapi.server import conform_content
from cah_gameinstance.gamephase import GamePhase
from cah_gameinstance.player import Player

debug = True
game_phase = GamePhase.SETUP
players = []
instance_id = str(uuid.uuid4())
prompt_cards = []
response_cards = []

app = bottle.Bottle()
package_root = os.path.dirname(os.path.realpath(__file__))


@app.route('/')
def index():
    return static_file('index.tpl', root=package_root + '/views/')


def get_player(player_id):
    if len(players) == 0:
        return None

    for player in players:
        if player.uuid == player_id:
            return player
    return None


def username_taken(username):
    for player in players:
        if player.username == username:
            return True
    return False


def generate_state(my_player=None):
    state = {
        "event": "state"
    }
    player_state = {}
    for player in players:
        if player.username:
            player_state[player.username] = {
                "isCzar": player.isCzar,
                "isAdmin": player.isAdmin,
                "points": player.points,
            }
    state['players'] = player_state
    state['game_phase'] = game_phase

    if game_phase is not GamePhase.SETUP:
        state['prompt_card'] = prompt_cards[0].to_json_obj()
        state['my_cards'] = [card.to_json_obj() for card in my_player.cards]

    return json.dumps(state)


def broadcast_message(data):
    for player in players:
        player.websocket.send(data)


def choose_next_czar(players):
    ''' Check who currently is the Czar '''
    current_czar: Player = None
    for player in players:
        if player.isCzar:
            current_czar = player
            break
    if current_czar is None:
        ''' No one is currently the Czar, default to first player '''
        players[0].isCzar = True
        print("Player " + players[0].username + " is the new Czar")
    else:
        ''' Determine position '''
        player_position = players.index(current_czar)
        if player_position == len(players) - 1:
            ''' Last player in the list, start from beginning '''
            current_czar.isCzar = False
            players[0].isCzard = True
            print("Player " + players[0].username + " is the new Czar")
        else:
            ''' Next player is Czar '''
            current_czar.isCzar = False
            players[player_position+1].isCzar = True
            print("Player " + players[player_position+1].username + " is the new Czar")


def rotate_prompt_cards(prompt_cards):
    top_card = prompt_cards.pop(0)
    prompt_cards.append(top_card)


def deal_cards(response_cards):
    for player in players:
        while len(player.cards) < 7:
            player.add_card(response_cards.pop(0))


def broadcast_state():
    for player in players:
        state = generate_state(player)
        player.websocket.send(state)


@app.get('/ws', apply=[websocket])
def websocket_handler(ws):
    global game_phase
    global prompt_cards
    global response_cards
    player = None
    try:
        """ Ask websocket connection to identify itself """
        ws.send('{ "event": "identity_request", "instance_id": "' + instance_id + '" }')

        while True:
            msg = None
            if player is None:
                msg = ws.receive()
            else:
                msg = player.websocket.receive()

            if msg is not None:
                response = None
                try:
                    response = json.loads(msg)
                    print("Client sent us: " + str(response))
                except JSONDecodeError as e:
                    print(player.username + " send us invalid JSON: " + str(e))

                try:
                    if response['event'] == "existing_player":
                        existing_player = get_player(response['player_id'])
                        if existing_player is not None:
                            print("Player " + existing_player.username + " (" + existing_player.uuid + ") rejoined")
                            existing_player.websocket.close()
                            player = existing_player
                            player.websocket = ws

                            ''' Let the player know that he rejoined successfully '''
                            player.websocket.send('{ "event": "rejoin_ack" }')
                            """ Send current game state """
                            broadcast_state()
                        else:
                            ''' We don't recognize this player, so adding him '''
                            player = Player(websocket=ws)
                            player.websocket.send(
                                '{ "event": "player_creation", "instance_id": "' +
                                instance_id + '", "player_id": "' + player.uuid + '" }')
                            players.append(player)
                            """ Send current game state """
                            broadcast_state()
                    elif response['event'] == "set_username":
                        # TODO: sanitize HTML entities
                        """ Check if another player hasn't already this username is use """
                        if not username_taken(response['username']):
                            if not player:
                                ''' Make admin if only player '''
                                is_admin = True if len(players) == 0 else False
                                ''' New player, send instance UUID '''
                                player = Player(websocket=ws, username=response['username'], isAdmin=is_admin)
                                player.websocket.send(
                                    '{ "event": "player_creation", "instance_id": "' +
                                    instance_id + '", "player_id": "' + player.uuid + '" }')
                                players.append(player)
                                """ Send current game state """
                                broadcast_state()
                                broadcast_message(
                                    '{ "event": "player_joined", "username": "' +
                                    player.username + '", "timestamp": "' + str(datetime.now().timestamp()) + '" }')
                            else:
                                player.username = response['username']
                                player.websocket.send(
                                    '{ "event": "username_ok" }')
                                """ Send current game state """
                                broadcast_state()
                        else:
                            player.websocket.send(
                                '{ "event": "username_nok" }')
                    elif response['event'] == 'game_start':
                        if player.isAdmin:
                            if game_phase is GamePhase.SETUP:
                                """ Fetch the decks """
                                for deck_id in response['deck_ids']:
                                    response = requests.get(deckapi_uri + "/decks/" + deck_id)
                                    if response.status_code == 200:
                                        entry = json.loads(response.content.decode('utf-8'))
                                        deck = Deck(
                                            name=entry['name'],
                                            description=entry['description'],
                                            lang=entry['lang'],
                                            cards=[]
                                        )

                                        ''' Attempt to create Card objects '''
                                        if len(entry['cards']) > 0:
                                            for card_entry in entry['cards']:
                                                card = Card(
                                                    type=CardType(card_entry['type']),
                                                    content=conform_content(str(card_entry['content'])),
                                                    pick=int(card_entry['pick']),
                                                    draw=int(card_entry['draw'])
                                                )
                                                deck.cards.append(card)
                                        prompt_cards.extend(deck.prompt_cards)
                                        response_cards.extend(deck.response_cards)
                                    game_phase = GamePhase.CARDS_SELECTION
                                    print('Player ' + player.username + ' started the game.')
                                    ''' Choose the next Czar '''
                                    choose_next_czar(players)
                                    ''' Shuffle the cards '''
                                    shuffle(prompt_cards)
                                    shuffle(response_cards)
                                    rotate_prompt_cards(prompt_cards)
                                    deal_cards(response_cards)
                                    broadcast_state()
                            else:
                                player.websocket.send(
                                    '{ "event": "unauthorized", "message": "You cannot change game settings while game '
                                    'in progress." }')
                        else:
                            player.websocket.send(
                                '{ "event": "unauthorized", "message": "You are unauthorized for this action" }')
                    else:
                        print("I have no idea what to do with that message")
                except TypeError as e:
                    print("We received an invalid request: " + str(e))
    except WebSocketError as e:
        if hasattr(player, 'username'):
            print(player.username + " had a websocket error: " + str(e))
    except AttributeError as e:
        if hasattr(player, 'username'):
            print(player.username + "'s websocket attribute doesn't exist: " + str(e))
    finally:
        if player is not None:
            '''players.remove(player)'''


@app.route('/js/logic.js', method='GET')
def send_logic_js():
    return bottle.template('logic_js', deckapi_uri=deckapi_uri, websocket_uri=websocket_uri)


@app.route('/js/<filename:path>', method='GET')
def send_js(filename):
    return static_file(filename, root=package_root + '/resources/js/')


@app.route('/img/<filename:path>', method='GET')
def send_img(filename):
    return static_file(filename, root=package_root + '/resources/img/')


@app.route('/css/<filename:path>', method='GET')
def send_css(filename):
    return static_file(filename, root=package_root + '/resources/css/')


@app.route('/favicon/<filename:path>', method='GET')
def send_favicon(filename):
    return static_file(filename, root=package_root + '/resources/favicon/')


if __name__ == '__main__':
    """ Default values """
    server_address = "0.0.0.0"
    server_port = 8081
    deckapi_uri = "http://localhost:8080/api/v1"
    websocket_uri = "ws://localhost:8081/ws"
    """ Try reading configuration from the environment """
    if os.environ.get('GAMEINSTANCE_ADDRESS'):
        server_address = os.environ.get('GAMEINSTANCE_ADDRESS')
    if os.environ.get('GAMEINSTANCE_PORT'):
        server_port = int(os.environ.get('GAMEINSTANCE_PORT'))
    if os.environ.get('GAMEINSTANCE_DEBUG'):
        debug = bool(os.environ.get('GAMEINSTANCE_DEBUG'))
    if os.environ.get('GAMEINSTANCE_DECKAPI_URI'):
        deckapi_uri = str(os.environ.get('GAMEINSTANCE_DECKAPI_URI'))
    if os.environ.get('GAMEINSTANCE_WEBSOCKET_URI'):
        websocket_uri = str(os.environ.get('GAMEINSTANCE_WEBSOCKET_URI'))

    bottle.TEMPLATE_PATH.insert(0, package_root + "/views")
    app.run(debug=debug, host=server_address, port=server_port, reloader=True, server=GeventWebSocketServer)
