class SortingBattleAction:
    '''
    The is a class to represent sorting-battle action.
    '''
    def __init__(self, action_id=-1):
        '''
        Constructor of the sorting-battle action.
        '''
        self.action_id = action_id
        self.action_info = self.find_action_info()

    def find_action_info(self):
        '''
        Find start, end, and type from action_id.
        :return: action info, dict. containing start, end, and type
        '''
        # TODO
        start = (0, 0)
        end = (0, 0)
        action_type = 'TODO'  # action_type: idle, swap, select, add
        return {'start':start, 'end':end, 'type':action_type}

    def action_to_string(self):
        '''
        Readable action.
        '''
        return f'action_id: {self.action_id}\n' + f'type[{self.action_type}], start[{self.start}], end[{self.end}]'

    def get_action_info(self):
        '''
        Get action info.
        :return: action info, dict. containing start, end, and type
        '''
        return self.action_info

    def get_action_id(self):
        '''
        Get action id.
        :return: action id, int. from 0~xxx
        '''
        return self.action_id
