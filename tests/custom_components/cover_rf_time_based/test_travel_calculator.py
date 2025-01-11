import unittest

from custom_components.cover_rf_time_based.travelcalculator import TravelCalculator, PositionType, TravelStatus

TRAVEL_TIME_DOWN = 19.5
TRAVEL_TIME_UP = 21
START_TIME = 1000

class TestTravelCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = TravelCalculator(travel_time_down=TRAVEL_TIME_DOWN, travel_time_up=TRAVEL_TIME_UP)
        self._reset_time()

    def test_initial_position(self):
        self.assertEqual(self.calculator.current_position(), 0)
        self.assertEqual(self.calculator.position_type, PositionType.UNKNOWN)

    def test_set_position(self):
        self.calculator.set_position(50)
        self.assertEqual(self.calculator.current_position(), 50)
        self.assertEqual(self.calculator.position_type, PositionType.CONFIRMED)

    def test_start_travel_up(self):
        self.calculator.start_travel_up()
        self.assertEqual(self.calculator.travel_to_position, 100)
        self.assertEqual(self.calculator.travel_direction, TravelStatus.DIRECTION_UP)

    def test_start_travel_down(self):
        self.calculator.set_position(100)
        self.calculator.start_travel_down()
        self.assertEqual(self.calculator.travel_to_position, 0)
        self.assertEqual(self.calculator.travel_direction, TravelStatus.DIRECTION_DOWN)

    def test_stop(self):
        self.calculator.start_travel_up()
        self._tick(TRAVEL_TIME_UP / 2)
        self.calculator.stop()
        self.assertEqual(self.calculator.travel_direction, TravelStatus.STOPPED)
        self.assertEqual(self.calculator.current_position(), 50)

    def test_is_traveling(self):
        self.calculator.start_travel_up()
        self._tick(0.01)
        self.assertTrue(self.calculator.is_traveling())
        self._tick(0.01)
        self.calculator.stop()
        self.assertFalse(self.calculator.is_traveling())

    def test_position_reached(self):
        self.calculator.start_travel_up()
        self._tick(TRAVEL_TIME_UP)
        self.assertTrue(self.calculator.position_reached())

    def test_position_not_reached(self):
        less_than_travel_time_up = TRAVEL_TIME_UP - 0.01

        self.calculator.start_travel_up()
        self._tick(less_than_travel_time_up)
        self.assertFalse(self.calculator.position_reached())

    def test_is_open(self):
        self.calculator.set_position(100)
        self.assertTrue(self.calculator.is_open())

    def test_is_closed(self):
        self.calculator.set_position(0)
        self.assertTrue(self.calculator.is_closed())

    def test_opening_than_closing(self):
        self.calculator.start_travel_up()
        self._tick(TRAVEL_TIME_UP / 2)
        self.calculator.start_travel_down()
        self._tick(TRAVEL_TIME_DOWN / 4)
        self.assertEqual(self.calculator.current_position(), 25)

    def _set_time(self, time):
        self.calculator.time_set_from_outside = time

    def _reset_time(self):
        self.calculator.time_set_from_outside = START_TIME

    def _tick(self, seconds):
        self.calculator.time_set_from_outside += seconds


if __name__ == '__main__':
    unittest.main()
