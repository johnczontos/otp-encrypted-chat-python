# Chatroom Client code
# @author: John C. Zontos
# email: zontosj@oregonstate.edu

import argparse
import socket
import otp
import ttt

STOPSIGNAL = "/q"
MAXSIZE = 2048


def get_args():
    parser = argparse.ArgumentParser(description='Chatserver++')
    parser.add_argument("port", type=int, help="Port number to listen on")
    parser.add_argument("-i", "--ipaddr", type=str,
                        help="ip address of the host (defaults to localhost)")
    parser.add_argument("-k", "--key", type=argparse.FileType("r"),
                        help="path to the encryption key file")
    parser.add_argument("-t", "--ttt", action="store_true", default=False,
                        help="enable Tic-Tac-Toe mode")

    return parser.parse_args()


def send_txt(s, key):
    # handle empty input
    while True:
        msg = input("> ")
        if msg:
            break
    # if in encryoted mode
    if key:
        msg = otp.encrypt(msg, key)
    print('sending: "{}"'.format(msg))
    s.sendall(msg.encode())


def recv_txt(s, key):
    print("Waiting for message...")
    msg = s.recv(MAXSIZE).decode()
    # if in encryoted mode
    if key:
        msg = otp.decrypt(msg, key)
    # handle stopsignal or disconnection from server
    if not msg or STOPSIGNAL in msg:
        print("chat ended.")
        exit()
    print('recieved message: "{}"'.format(msg))


def send_move(s, board):
    move = board.make_move()
    print('sending: "{}"'.format(move))
    s.sendall(move.encode())


def recv_move(s, board):
    print("Waiting for opponent...")
    move = s.recv(MAXSIZE).decode()
    board.recv_move(move)


def main():

    # parse args
    args = get_args()
    key = args.key.read() if args.key else None
    port = args.port
    addr = args.ipaddr or socket.gethostbyname(socket.gethostname())

    print("Client connecting...\
    \nAddress :", addr, "\
    \nPort :", port)

    if (args.sttt):
        print("tik-tak-toe mode")
        board = ttt.Board()

    # use with to ensure socket is "cleaned up"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # make socket reusable
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.connect((addr, port))
        print("connected to", addr)
        while True:
            while True:
                if(args.sttt):
                    send_move(s, board)
                    recv_move(s, board)
                else:
                    send_txt(s, key)
                    recv_txt(s, key)


if __name__ == "__main__":
    main()
