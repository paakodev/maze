from dataclasses import dataclass

# 0,0 is top-left of screen
@dataclass(frozen=True)
class Point:
    x: int
    y: int