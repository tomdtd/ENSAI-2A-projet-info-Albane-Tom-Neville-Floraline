import os
import requests

from typing import List


class PokerClient:
    """Make call to the poker endpoint"""

    def __init__(self) -> None:
        self.__host = os.environ["WEBSERVICE_HOST"]

    
