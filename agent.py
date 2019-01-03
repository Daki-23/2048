import random

class Agent:
    def get_action(self, prev_action):
        action_choices = {"RIGHT", "DOWN"} - prev_action
        if action_choices:
            return random.choice(list(action_choices))
        else:
            return random.choice(list(["UP", "LEFT"]))