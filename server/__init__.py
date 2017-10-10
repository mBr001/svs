from widgets import LogBox, HeaderBox, Screen, ServerBox
from network import Network
from log import logger
import os
import keyboard
from time import sleep
from socketserver import SocketServer


class UI():
    def __init__(self):
        self.screen = Screen()
        self.socket_server = SocketServer("", 50000)
        self.socket_server.events.on_change += self.update_server_status

        self.maxx = self.screen.maxx
        self.maxy = self.screen.maxy

        # UI elements
        self.headerbox = HeaderBox(1, self.maxx, 0, 0)
        self.serverbox = ServerBox(10, 25, 2, 2)
        self.logbox = LogBox(14, self.maxx - 4, self.maxy - 14, 2)

        self.start_ui()

    def start_ui(self):
        # self.init_screen(stdscr)


        self.socket_server.start()
        # sleep(5)
        # logger.debug("%s", len(self.socket_server.threads))
        # client.on("new_data", self.show_data)

        # keyboard.wait('q')  # if key 'q' is pressed
        # self.logbox.box.getch()
        # self.socket_server.stop()
        # self.screen.stop()

        # key = ""
        # while key != ord('q'):  # press <Q> to exit the program
        self.logbox.box.getch()  # get the key

        self.serverbox.close()
        self.socket_server.stop()
        self.screen.stop()

    def show_data(self, data):
        logger.debug("%s", data)

    def update_server_status(self, status):
        self.serverbox.update_status(status)

