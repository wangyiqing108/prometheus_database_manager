import os
import sys

HOME = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(HOME, "conf"))
sys.path.append(os.path.join(HOME, "bin"))

from utils import create_logger
from config import config

from server import app

create_logger()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config.PORT, debug=config.DEBUG)
