# Create a logger object.
# Taken from https://github.com/VT-SailBOT
import logging
import coloredlogs
import os
import curses

# os.environ['COLOREDLOGS_LOG_FORMAT'] ='%(asctime)s.%(msecs)03d %(name)s - %(message)s'
# os.environ['COLOREDLOGS_DATE_FORMAT'] ='%H%M%S'
# os.environ['COLOREDLOGS_LEVEL_STYLES'] ='info=cyan,bold;warning=yellow;error=red;critical=red,bold'
logger = logging.getLogger("SVSystem")


class CursesHandler(logging.Handler):
    def __init__(self, screen):
        logging.Handler.__init__(self)
        self.screen = screen

        curses.start_color()
        curses.use_default_colors()
        for i in range(0, curses.COLORS):
            curses.init_pair(i + 1, i, -1)

    def emit(self, record):
        try:
            msg = self.format(record)
            screen = self.screen
            screen.addstr(u'\n%s' % msg, self.get_color_pair(record.levelname))
            screen.refresh()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

    def get_color_pair(self, level):
        index = str(level)
        color = {
                'DEBUG': 100,
                'INFO': 39,
                'WARNING': 209,
                'ERROR': 161,
                'CRITICAL': 197
            }[index]
        return curses.color_pair(color)


def setup_log(win):
    logging.getLogger().setLevel(logging.DEBUG)
    mh = CursesHandler(win)
    formatterDisplay = logging.Formatter('[%(asctime)s] %(levelname)-0s: %(message)s', '%H:%M:%S')
    mh.setFormatter(formatterDisplay)
    logger.addHandler(mh)

# coloredlogs.install(level='DEBUG')

# class Logger:
#     def __init__(self, module_name, level):
#         os.environ['COLOREDLOGS_LOG_FORMAT'] ='%(asctime)s.%(msecs)03d %(name)s - %(message)s'
#         os.environ['COLOREDLOGS_DATE_FORMAT'] ='%H%M%S'
#         self.logger = logging.getLogger(module_name)
#         coloredlogs.install(level=level)
#
#     def debug(self, msg):
#         self.logger.debug(msg)
#
#     def info(self, msg):
#         self.logger.info(msg)
#
#     def warn(self, msg):
#         self.logger.warn(msg)
#
#     def error(self, msg):
#         self.logger.error(msg)
#
#     def critical(self, msg):
#         self.logger.critical(msg)
