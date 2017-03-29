# -*-coding:Utf-8 -*

"""Ce fichier contient la classe ReadFromPipe.

"""
import random
import sys
from threading import Thread
import time

class ReadFromPipe(Thread):
    """Thread chargé de lire le pipe."""

    def __init__(self, pipe):
        Thread.__init__(self)
        self.pipe = pipe

    def run(self):
        """Lecture du pipe."""

        while True:
            s = self.pipe.readline()
            sys.stdout.write(s)
            sys.stdout.flush()
