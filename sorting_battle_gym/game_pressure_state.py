class GamePressureState:
    '''
    GamePressureState handles a player's pressure state in a game.
    All the related function are implemented here.
    '''
    def __init__(self, max_pressure=40):
        '''
        Construct with max_pressure.
        :param max_pressure: the maximum value of pressure.
        '''
        self.pressure = 0
        self.max_pressure = max_pressure

    def consume_pressure(self, amount):
        '''
        Try to consume a player's pressure by amount.
        :param amount: the amount of pressure to try consuming.
        :return: the actual amount of pressure consumed.
        '''
        before = self.pressure
        self.pressure = max(0, self.pressure - amount)
        return before - self.pressure

    def add_pressure(self, amount):
        '''
        Add pressure to a player.
        :param amount: the amount of pressure to add.
        '''
        self.pressure = min(self.max_pressure, self.pressure + amount)

    def attack(self, other, attack_power):
        '''
        Attack another player by attack_power.
        The rule is adjusted to attack the opponent with "attack_power + consumed_pressure".
        :param other: the GamePressureState object of the other player.
        :param attack_power: the attack power.
        '''
        consumed_pressure = self.consume_pressure(attack_power)
        other.add_pressure(attack_power + consumed_pressure)

    def get_pressure_rate(self):
        '''
        Get the pressure rate.
        :return: the pressure rate.
        '''
        return self.pressure / self.max_pressure
