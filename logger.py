"""
:author: Shau
"""

import logging
import colorlog

def load_logger():
    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler(filename='bot.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        colorlog.ColoredFormatter('%(log_color)s%(asctime)s%(reset)s:%(levelname)s:%(name)s: %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S', reset=True, log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white'
            }))

    if logger.hasHandlers():
        logger.handlers.clear()

    remove_discord_loggers()

    logger.addHandler(handler)
    logger.addHandler(console_handler)

def remove_discord_loggers():
    discord_loggers = ["discord.gateway", "discord.client"]
    for logger_name in discord_loggers:
        logging.getLogger(logger_name).setLevel(logging.CRITICAL)

def get_logger():
    return logging.getLogger('discord')

