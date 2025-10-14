import os


class RunSatisfactory:
    def __init__(self, os_type: str):
        self.os: str = os_type

    async def run(self):
        os.cmd("echo kek")  # TODO everything
