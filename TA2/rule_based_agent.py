def initialize_environment():
    """Initializes three rooms (A, B, and C) and allows the user to set their initial states[cite: 1]."""
    environment = {}
    for room in ['A', 'B', 'C']:
        while True:
            # Prompt user to set the initial state of each room as dirty or clean[cite: 1]
            state = input(f"Is Room {room} Dirty or Clean? ").strip().lower()
            if state in ['dirty', 'clean']:
                environment[room] = state
                break
            print("Invalid input. Please enter 'dirty' or 'clean'.")
    return environment

def is_dirty(environment, room):
    """Checks if the specified room is dirty[cite: 1]."""
    return environment.get(room) == 'dirty'

def clean_room(environment, room):
    """Updates the state of the specified room to clean[cite: 1]."""
    environment[room] = 'clean'


class VacuumAgent:
    """Represents a rule-based vacuum cleaner agent that perceives and cleans rooms[cite: 1]."""
    def __init__(self, start_location='A'):
        self.location = start_location  # Agent starts in Room A by default

    def perceive_and_act(self, environment):
        """
        Perceives the current environment state and decides whether 
        to clean the room or move to the next room[cite: 1].
        """
        current_room = self.location
        action = ""

        # Rule 1: If the current room is dirty, clean it[cite: 1]
        if is_dirty(environment, current_room):
            clean_room(environment, current_room)
            action = f"Room {current_room} has been cleaned"
        else:
            # Rule 2: If the current room is clean, move to the next room[cite: 1]
            self.move()
            action = f"Moving to room {self.location}"
            
        return current_room, action

    def move(self):
        """Switches rooms sequentially from A -> B -> C -> A."""
        if self.location == 'A':
            self.location = 'B'
        elif self.location == 'B':
            self.location = 'C'
        else:
            self.location = 'A'


def run_simulation():
    """Sets up the environment, initializes the agent, and runs the simulation loop[cite: 1]."""
    env = initialize_environment()
    
    start_loc = 'A'
        
    agent = VacuumAgent(start_location=start_loc)
    
    # Ask the user how many steps the simulation should run[cite: 1]
    try:
        steps = int(input("How many steps should the agent run? "))
    except ValueError:
        steps = 5
        print("Invalid number of steps entered. Defaulting to 5 steps.")

    # Run the agent in a loop for the specified number of steps[cite: 1]
    for step in range(1, steps + 1):
        loc, action_desc = agent.perceive_and_act(env)
        print(f"Step {step}:")
        print(f"  - Agent is in room {loc}")
        print(f"  - {action_desc}")
        print(f"  - Environment State: {env}")
        print("-" * 40)

if __name__ == "__main__":
    run_simulation()