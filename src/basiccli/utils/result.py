from dataclasses import dataclass


@dataclass
class Result:
    success: bool
    message: str

    def is_success(self) -> bool:
        return self.success
