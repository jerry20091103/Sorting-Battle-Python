from sorting_battle_gym.game_pressure_state import GamePressureState

class TestgGamePressureState:
    def test_initial_state(self):
        '''
        Test the initial values of GamePressureState.
        '''
        pressure_state = GamePressureState(100)
        assert pressure_state.pressure == 0
        assert pressure_state.max_pressure == 100

        pressure_state = GamePressureState(40)
        assert pressure_state.pressure == 0
        assert pressure_state.max_pressure == 40

    def test_add_pressure(self):
        '''
        Test the add_pressure function of GamePressureState.
        '''
        pressure_state = GamePressureState(100)
        assert pressure_state.pressure == 0
        pressure_state.add_pressure(10)
        assert pressure_state.pressure == 10
        pressure_state.add_pressure(20)
        assert pressure_state.pressure == 30
        pressure_state.add_pressure(100)
        assert pressure_state.pressure == 100

    def test_consume_pressure(self):
        '''
        Test the consume_pressure function of GamePressureState.
        '''
        pressure_state = GamePressureState(100)
        assert pressure_state.consume_pressure(10) == 0
        pressure_state.add_pressure(100)
        assert pressure_state.consume_pressure(10) == 10
        assert pressure_state.pressure == 90
        assert pressure_state.consume_pressure(20) == 20
        assert pressure_state.pressure == 70
        assert pressure_state.consume_pressure(100) == 70
        assert pressure_state.pressure == 0

    def test_attack(self):
        '''
        Test the attack function of GamePressureState.
        '''
        p1 = GamePressureState(100)
        p2 = GamePressureState(100)
        p1.add_pressure(50)
        p2.add_pressure(50)
        # After reduced 25 pressure from P1, the attack power on P2 will be 25(original power) + 25(consumed pressure) = 50.
        # P1's pressure will be 25, P2's pressure will be 100.
        p1.attack(p2, 25)
        assert p1.pressure == 25
        assert p2.pressure == 100
        # Here, after removing the remaining 25 pressure from P1, the attack power will be 30(original power) + 25(consumed pressure) = 55.
        # P1's pressure will be 0, P2's pressure will be 100(max).
        p1.attack(p2, 30)
        assert p1.pressure == 0
        assert p2.pressure == 100
        # Then P2 attack back
        # P1's pressure will be 100, P2's pressure will be 30.
        p2.attack(p1, 70)
        assert p1.pressure == 100
        assert p2.pressure == 30

    def test_get_pressure_rate(self):
        '''
        Test the get_pressure_rate function of GamePressureState.
        '''
        pressure_state = GamePressureState(100)
        assert pressure_state.get_pressure_rate() == 0
        pressure_state.add_pressure(15)
        assert pressure_state.get_pressure_rate() == 0.15
        pressure_state.add_pressure(25)
        assert pressure_state.get_pressure_rate() == 0.4
        pressure_state.add_pressure(100)
        assert pressure_state.get_pressure_rate() == 1
