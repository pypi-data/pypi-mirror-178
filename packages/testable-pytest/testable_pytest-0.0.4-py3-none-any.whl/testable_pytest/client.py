from requests import Session
from settings import Settings


class TestableClient(Session):
    """
    API Client that can interact with Testable
    """
    def __init__(self, settings: Settings):
        super().__init__()
        self.settings = settings

    def create_or_update_case(self):
        pass
