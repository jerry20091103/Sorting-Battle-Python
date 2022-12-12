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
        # Because P1 has 50 pressure, the 25 attack power will be used to reduce its own pressure.
        p1.attack(p2, 25)
        assert p1.pressure == 25
        assert p2.pressure == 50
        # Here, after removing the remaining 25 pressure from P1, the remaining 5 attack power will be used on P2.
        p1.attack(p2, 30)
        assert p1.pressure == 0
        assert p2.pressure == 55
        # And finally, this maximizes P2's pressure.
        p1.attack(p2, 70)
        assert p1.pressure == 0
        assert p2.pressure == 100

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
