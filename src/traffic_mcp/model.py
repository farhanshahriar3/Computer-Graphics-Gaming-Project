"""Headless traffic simulation state shared by MCP tools and clients."""

from __future__ import annotations

from dataclasses import dataclass, field
import random


LANES = (-180, -60, 60, 180)
SPEED_ZONES = ((-1200, -400, 3.0), (-400, 200, 1.2), (200, 1200, 2.5))
GRID_LENGTH = 1200


@dataclass
class Car:
    lane: int
    z: float
    speed: float
    color: tuple[float, float, float]
    original_lane: int
    last_speed: float = 0.0


@dataclass
class TrafficModel:
    """A deterministic, GUI-independent model of the traffic scene."""

    seed: int | None = None
    signal_green: bool = True
    auto_signal: bool = False
    paused: bool = False
    speed_boost: bool = False
    signal_timer: int = 0
    ambulance_index: int = 0
    cars: list[Car] = field(default_factory=list)
    _random: random.Random = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self._random = random.Random(self.seed)
        self.reset()

    def reset(self) -> None:
        self.cars.clear()
        colors = ((1.0, 1.0, 1.0), (0.2, 0.2, 0.2), (1.0, 0.0, 0.0),
                  (0.0, 0.0, 1.0), (0.6, 0.6, 0.6), (0.5, 0.8, 1.0))
        for lane in LANES:
            for _ in range(5):
                self.cars.append(Car(
                    lane=lane, original_lane=lane,
                    z=self._random.randint(-GRID_LENGTH, GRID_LENGTH),
                    speed=self._random.uniform(1.5, 3.0),
                    color=self._random.choice(colors),
                ))
        self.ambulance_index = self._random.randrange(len(self.cars))
        self.signal_timer = 0

    def _front_distance(self, index: int) -> float:
        car = self.cars[index]
        distances = [other.z - car.z for position, other in enumerate(self.cars)
                     if position != index and other.lane == car.lane and other.z > car.z]
        return min(distances, default=500.0)

    def _zone_speed(self, z: float) -> float:
        for lower, upper, speed in SPEED_ZONES:
            if lower <= z <= upper:
                return speed
        return 2.0

    def tick(self, steps: int = 1) -> None:
        """Advance the model by a bounded number of frames."""
        for _ in range(max(0, min(steps, 1000))):
            if self.paused:
                continue
            if self.auto_signal:
                self.signal_timer += 1
                if self.signal_timer >= 300:
                    self.signal_green = not self.signal_green
                    self.signal_timer = 0
            for index, car in enumerate(self.cars):
                car.last_speed = car.speed
                if index != self.ambulance_index and not self.signal_green and car.z < 0:
                    car.speed = 0.0 if self._front_distance(index) >= 80 else -0.5
                else:
                    target = self._zone_speed(car.z) * (2.0 if self.speed_boost else 1.0)
                    front_distance = self._front_distance(index)
                    if front_distance < 100:
                        target *= 0.4
                    elif front_distance < 150:
                        target *= 0.7
                    car.speed += (target - car.speed) * 0.01
                car.z += car.speed
                if car.z > GRID_LENGTH:
                    car.z = -GRID_LENGTH
                elif car.z < -GRID_LENGTH:
                    car.z = GRID_LENGTH

    def status(self) -> dict[str, object]:
        return {
            "signal": "green" if self.signal_green else "red",
            "auto_signal": self.auto_signal, "paused": self.paused,
            "speed_boost": self.speed_boost, "ambulance_index": self.ambulance_index,
            "car_count": len(self.cars),
            "cars": [{"index": index, "lane": car.lane, "z": round(car.z, 2),
                      "speed": round(car.speed, 2),
                      "is_ambulance": index == self.ambulance_index}
                     for index, car in enumerate(self.cars)],
        }

    def inspect(self, index: int) -> dict[str, object]:
        if not 0 <= index < len(self.cars):
            raise IndexError(f"car index must be between 0 and {len(self.cars) - 1}")
        car = self.cars[index]
        return {"index": index, "lane": car.lane, "z": round(car.z, 2),
                "speed": round(car.speed, 2),
                "is_ambulance": index == self.ambulance_index,
                "front_distance": round(self._front_distance(index), 2)}