from dataclasses import dataclass
from datetime import datetime

from ..utils.result import Result


@dataclass
class HelloCommand:
    name: str
    uppercase: bool = False
    repeat: int = 1

    def execute(self) -> Result:
        try:
            greeting = self._build_greeting()

            for _ in range(self.repeat):
                if self.uppercase:
                    print(greeting.upper())
                else:
                    print(greeting)

            return Result(success=True, message=greeting)
        except Exception as e:
            return Result(success=False, message=str(e))

    def _build_greeting(self) -> str:
        time_of_day_greeting = self._time_of_day()
        return f"{time_of_day_greeting}, {self.name}! Welcome to BasicCli"

    def _time_of_day(self) -> str:
        hour = datetime.now().hour
        if 0 <= hour <= 11:
            return "Good morning"
        elif 12 <= hour <= 17:
            return "Good afternoon"
        else:
            return "Good evening"
