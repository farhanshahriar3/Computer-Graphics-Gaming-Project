import unittest

from traffic_mcp.model import TrafficModel


class TrafficModelTests(unittest.TestCase):
    def test_reset_creates_four_lanes_of_traffic(self) -> None:
        model = TrafficModel(seed=27)
        self.assertEqual(len(model.cars), 20)
        self.assertIn(model.ambulance_index, range(20))

    def test_pause_keeps_positions_stable(self) -> None:
        model = TrafficModel(seed=27)
        before = [car.z for car in model.cars]
        model.paused = True
        model.tick(10)
        self.assertEqual(before, [car.z for car in model.cars])

    def test_auto_signal_changes_after_300_frames(self) -> None:
        model = TrafficModel(seed=27, auto_signal=True)
        initial = model.signal_green
        model.tick(300)
        self.assertNotEqual(initial, model.signal_green)


if __name__ == "__main__":
    unittest.main()