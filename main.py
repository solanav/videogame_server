import socket
from hashlib import md5

SERVER_PORT = 4343
MAX_PACKET = 1024

class Player():
    ''' Player object '''
    def __init__(self, addr):
        self.addr = addr
        self.pos = None
        self.id = md5(str(addr).encode()).hexdigest()

    def update_pos(self, posx, posy):
        pos = (posx, posy)
        if self.pos != pos:
            print('{} {} > {}'.format(self.id, self.addr, pos))
            self.pos = pos

    def send_update(self, id, posx, posy):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto("{},{},{}".format(id, posx, posy).encode(), self.addr)

def main():
    ''' Main loop '''
    player_list = []

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('localhost', SERVER_PORT))

    print('Starting the server...')

    while True:
        data, addr = sock.recvfrom(MAX_PACKET)

        # Deserialize coordinates
        pos = data.decode('ascii').replace('(', '').replace(')', '')
        posx, posy = pos.split(', ')
        posx = float(posx)
        posy = float(posy)
        id = md5(str(addr).encode()).hexdigest()

        # Looking through player list to update pos
        found = False
        for player in player_list:
            if player.addr == addr:
                # Update player
                player.update_pos(posx, posy)
                found = True
            else:
                # Send update to other players
                if player.pos != (posx, posy):
                    player.send_update(id, posx, posy)

        # New player connected
        if not found:
            print('New player connected on {}'.format(addr))
            p = Player(addr)
            p.update_pos(posx, posy)
            player_list.append(p)

if __name__ == '__main__':
    main()
