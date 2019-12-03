import math
from game.serializable import Serializable
import os

# Helper class for utility functions
class Utility:
    @staticmethod
    def debug(src, msg):
        print("[%s] %s" % (src, msg))

    @staticmethod
    def round(num):
        sign = -1 if num < 0 else 1
        num = abs(num)
        if num % 1 >= 0.5:
            return sign*math.ceil(num)
        else:
            return sign*math.floor(num)

    @staticmethod
    def save(world):
        name = world.name
        if not os.path.exists("saves"):
            os.makedirs("saves")

        file = open(f"saves/{name}.world", "w")
        file.write(Serializable.serialize(world))
        file.close()