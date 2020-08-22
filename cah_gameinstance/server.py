import json
import os
import uuid
from datetime import datetime

import bottle
from bottle import static_file
from bottle_websocket import GeventWebSocketServer, websocket
from geventwebsocket import WebSocketError

from cah_gameinstance.gamephase import GamePhase
from cah_gameinstance.player import Player

debug = True
game_phase = GamePhase.SETUP
players = set()
instance_id = str(uuid.uuid4())

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


def generate_state():
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

    return json.dumps(state)


def broadcast_message(data):
    for player in players:
        player.websocket.send(data)


@app.get('/ws', apply=[websocket])
def websocket_handler(ws):
    player = None
    try:
        if len(players) == 0:
            ''' This is the first player, send instance UUID '''
            player = Player(websocket=ws, isAdmin=True)
            player.websocket.send(
                '{ "event": "player_creation", "instance_id": "' +
                instance_id + '", "player_id": "' + player.uuid + '" }')
            players.add(player)
        else:
            ''' There are existing users, ask if new connection, or reconnecting user '''
            ws.send('{ "event": "identity_request", "instance_id": "' + instance_id + '" }')
        while True:
            msg = None
            if player is None:
                msg = ws.receive()
            else:
                msg = player.websocket.receive()

            if msg is not None:
                response = json.loads(msg)
                print("Client sent us: " + str(response))

                if response['event'] == "existing_player":
                    existing_player = get_player(response['player_id'])
                    if existing_player is not None:
                        print("Player " + existing_player.username + " (" + existing_player.uuid + ") rejoined")
                        existing_player.websocket.close()
                        player = existing_player
                        player.websocket = ws

                        ''' Check if game is already in progress '''
                        if game_phase != GamePhase.SETUP:
                            """ Send current game state """
                            broadcast_message(generate_state())
                        else:
                            ''' Let the player know that he rejoined successfully '''
                            player.websocket.send('{ "event": "rejoin_ack" }')
                            """ Send current game state """
                            broadcast_message(generate_state())
                    else:
                        ''' We don't recognize this player, so adding him '''
                        player = Player(websocket=ws)
                        player.websocket.send(
                            '{ "event": "player_creation", "instance_id": "' +
                            instance_id + '", "player_id": "' + player.uuid + '" }')
                        players.add(player)
                        """ Send current game state """
                        broadcast_message(generate_state())
                elif response['event'] == "set_username":
                    # TODO: sanitize HTML entities
                    """ Check if another player hasn't already this username is use """
                    if not username_taken(response['username']):
                        if not player:
                            ''' New player, send instance UUID '''
                            player = Player(websocket=ws, username=response['username'])
                            player.websocket.send(
                                '{ "event": "player_creation", "instance_id": "' +
                                instance_id + '", "player_id": "' + player.uuid + '" }')
                            players.add(player)
                            """ Send current game state """
                            broadcast_message(generate_state())
                            broadcast_message(
                                '{ "event": "player_joined", "username": "' +
                                player.username + '", "timestamp": "' + str(datetime.now().timestamp()) + '" }')
                        else:
                            player.username = response['username']
                            player.websocket.send(
                                '{ "event": "username_ok" }')
                            """ Send current game state """
                            broadcast_message(generate_state())
                    else:
                        player.websocket.send(
                            '{ "event": "username_nok" }')

            else:
                break
    except WebSocketError as e:
        print(player.username + " had a websocket error: " + str(e))
    except AttributeError as e:
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
def send_js(filename):
    return static_file(filename, root=package_root + '/resources/img/')


@app.route('/favicon/<filename:path>', method='GET')
def send_favicon(filename):
    return static_file(filename, root=package_root + '/resources/favicon/')


if __name__ == '__main__':
    """ Default values """
    server_address = "0.0.0.0"
    server_port = 8081
    deckapi_uri = "'http://' + window.location.hostname + ':8080/api/v1'"
    websocket_uri = "'ws://' + window.location.host + '/ws'"
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
