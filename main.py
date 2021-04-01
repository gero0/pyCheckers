from pycheckers.game_logic import Game
from pycheckers.constants import *
from pycheckers.player_color import PlayerColor
import pygame
import socket
import sys

opponent_connection = None
opponent_address = None
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

PORT = 65432


def wait_for_connections():
    global opponent_connection
    global opponent_address
    global tcp_socket

    font = pygame.font.Font('ArialCE.ttf', 24)
    conn_img = font.render(
        "Waiting for opponent to connect...", False, (255, 255, 255))
    WINDOW.blit(conn_img, (300, 400))
    pygame.display.update()

    tcp_socket.bind(("0.0.0.0", PORT))
    tcp_socket.listen()

    conn, addr = tcp_socket.accept()
    opponent_address = addr
    opponent_connection = conn
    conn.sendall(b"OK")

    tcp_socket.close()

    print(conn, addr)


def connect_to_server(host):
    global opponent_connection
    global opponent_address
    global tcp_socket

    tcp_socket.connect((host, PORT))
    data = tcp_socket.recv(1024)

    opponent_connection = tcp_socket
    opponent_address = host

    if data == b"OK":
        return True
    else:
        return False


def get_coords_from_mouse(position):
    (x, y) = position

    if x > BOARD_WIDTH:
        return None

    return (x // SQUARE_SIZE, y // SQUARE_SIZE)


def main():
    opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
    args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

    if "-c" in opts:
        role = "Client"
        if len(args) < 1:
            print("You must specify server's IP address")
            quit()
        host = args[0]
    else:
        role = "Server"

    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("pyCheckers")

    color = None

    if role == "Server":
        wait_for_connections()
        color = PlayerColor.WHITE
    else:
        result = connect_to_server(host)
        color = PlayerColor.BLACK
        if result == False:
            quit()

    run = True
    clock = pygame.time.Clock()
    game = Game(color, opponent_connection)

    while run:
        clock.tick(FPS)

        game.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                coords = get_coords_from_mouse(event.pos)
                game.select_square(coords)


if __name__ == "__main__":
    main()
