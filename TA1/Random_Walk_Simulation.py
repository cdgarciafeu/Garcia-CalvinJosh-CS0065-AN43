import agentpy as ap
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# -------- Get user input from console --------
num_agents = int(input("Enter number of agents: "))
grid_size = int(input("Enter grid size (e.g., 10 for 10x10): "))
num_steps = int(input("Enter number of steps: "))

# -------- Agent Definition -----------
class RandomWalker(ap.Agent):
    def step(self):
        # Lazy initialization of path history once position is available
        if not hasattr(self, 'path'):
            self.path = [self.position]
            
        direction = random.choice([(1,0), (-1,0), (0,1), (0,-1)])
        x, y = self.position
        
        # Keep agents inside grid boundaries
        x = max(0, min(self.model.p.grid_size[0]-1, x + direction[0]))
        y = max(0, min(self.model.p.grid_size[1]-1, y + direction[1]))
        
        self.position = (x, y)
        self.path.append(self.position)  # Record the new position

# -------- Model Definition -----------
class RandomWalkModel(ap.Model):
    def setup(self):
        # Create agents
        self.agents = ap.AgentList(self, self.p.agents, RandomWalker)
        
        # Initialize random positions and starting paths
        for agent in self.agents:
            agent.position = (random.randint(0, self.p.grid_size[0]-1),
                              random.randint(0, self.p.grid_size[1]-1))
            agent.path = [agent.position]
        
        # Create grid and add agents
        self.grid = ap.Grid(self, self.p.grid_size, torus=False)
        self.grid.add_agents(self.agents)

    def step(self):
        for agent in self.agents:
            agent.step()

# -------- Parameters from user input -----------
parameters = {
    'agents': num_agents,
    'grid_size': (grid_size, grid_size),
    'steps': num_steps
}

# -------- Run Model -----------
model = RandomWalkModel(parameters)
model.setup()

# -------- Interactive Animation & Path Display -----------
fig, ax = plt.subplots()
ax.set_xlim(0, model.p.grid_size[0])
ax.set_ylim(0, model.p.grid_size[1])
ax.set_xticks(range(model.p.grid_size[0]+1))
ax.set_yticks(range(model.p.grid_size[1]+1))
ax.grid(True)

# Create a line plot for each agent's path trail and a scatter plot for current positions
path_lines = [ax.plot([], [], alpha=0.6, linestyle='-', linewidth=1.5)[0] for _ in range(num_agents)]
scat = ax.scatter([], [], s=150, color='red', label='Agents', zorder=3)

def update(frame):
    model.step()
    
    # Update visual path lines and current positions for each agent
    for i, agent in enumerate(model.agents):
        px = [p[0] for p in agent.path]
        py = [p[1] for p in agent.path]
        path_lines[i].set_data(px, py)
        
    x = [agent.position[0] for agent in model.agents]
    y = [agent.position[1] for agent in model.agents]
    scat.set_offsets(list(zip(x, y)))
    
    return path_lines + [scat]

ani = animation.FuncAnimation(fig, update, frames=model.p.steps, interval=300, blit=True, repeat=False)
plt.title("Random Walk Simulation with Path Trails")
plt.show()

# -------- Post-Simulation Analysis: Final Positions -----------
print("\n--- Simulation Complete ---")
print("Final Positions and Recorded Path Statistics of All Agents:")
for i, agent in enumerate(model.agents):
    print(f"Agent {i+1}: Final Position = {agent.position}, Total Path Steps Recorded = {len(agent.path)}")