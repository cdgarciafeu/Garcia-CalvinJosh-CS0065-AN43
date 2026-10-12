def initialize_environment():
    """Initializes three rooms (A, B, and C) and allows the user to set their initial states."""
    environment = {}
    for room in ['A', 'B', 'C']:
        while True:
            state = input(f"Is Room {room} Dirty or Clean? ").strip().lower()
            if state in ['dirty', 'clean']:
                environment[room] = state
                break
            print("Invalid input. Please enter 'dirty' or 'clean'.")
    return environment

def is_dirty(environment, room):
    return environment.get(room) == 'dirty'

def clean_room(environment, room):
    environment[room] = 'clean'


class VacuumAgent:
    def __init__(self, start_location='A'):
        self.location = start_location 

    def perceive_and_act(self, environment):
        current_room = self.location
        action = ""

        if is_dirty(environment, current_room):
            clean_room(environment, current_room)
            action = f"Room {current_room} has been cleaned"
        else:
            self.move()
            action = f"Moving to room {self.location}"
            
        return current_room, action

    def move(self):
        if self.location == 'A':
            self.location = 'B'
        elif self.location == 'B':
            self.location = 'C'
        else:
            self.location = 'A'


def run_simulation():
    env = initialize_environment()
    
    start_loc = 'A'
        
    agent = VacuumAgent(start_location=start_loc)
    
    try:
        steps = int(input("How many steps should the agent run? "))
    except ValueError:
        steps = 5
        print("Invalid number of steps entered. Defaulting to 5 steps.")

    
    for step in range(1, steps + 1):
        loc, action_desc = agent.perceive_and_act(env)
        print(f"Step {step}:")
        print(f"  - Agent is in room {loc}")
        print(f"  - {action_desc}")
        print(f"  - Environment State: {env}")
        print("-" * 40)

if __name__ == "__main__":
    run_simulation()