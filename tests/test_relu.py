from sorting_battle_gym.relu import relu
class TestGitHubActions:

    def test_relu(self):
        assert relu(1) == 1
        assert relu(-1) == 0