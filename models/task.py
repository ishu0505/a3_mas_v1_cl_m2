import numpy as np

class Task:
    """A task that requires agents to complete."""
    
    def __init__(self, task_id, pos, radius, required_agents):
        self.task_id = task_id
        self.pos = pos  # (x, y) position
        self.radius = radius  # Tr - task radius
        self.required_agents = required_agents  # Tc - number of agents needed
        self.agents_in_range = []  # Agents currently within radius
        self.completed = False
    
    def is_within_range(self, agent_pos):
        """Check if a position is within task radius."""
        distance = np.sqrt((agent_pos[0] - self.pos[0])**2 + 
                          (agent_pos[1] - self.pos[1])**2)
        return distance <= self.radius
    
    def add_agent(self, agent):
        """Add an agent to the task."""
        if agent not in self.agents_in_range:
            self.agents_in_range.append(agent)
    
    def remove_agent(self, agent):
        """Remove an agent from the task."""
        if agent in self.agents_in_range:
            self.agents_in_range.remove(agent)
    
    def check_completion(self):
        """Check if task has enough agents to complete."""
        # Filter agents that are actually within range
        valid_agents = [agent for agent in self.agents_in_range 
                       if self.is_within_range(agent.pos)]
        
        self.agents_in_range = valid_agents
        
        if len(self.agents_in_range) >= self.required_agents:
            # Select Tc closest agents if more than required
            if len(self.agents_in_range) > self.required_agents:
                # Sort by distance and keep closest Tc agents
                sorted_agents = sorted(
                    self.agents_in_range,
                    key=lambda a: np.sqrt((a.pos[0] - self.pos[0])**2 + 
                                         (a.pos[1] - self.pos[1])**2)
                )
                self.agents_in_range = sorted_agents[:self.required_agents]
            
            self.completed = True
            return True
        return False
    
    def get_distance_to(self, agent):
        """Get distance from agent to task."""
        return np.sqrt((agent.pos[0] - self.pos[0])**2 + 
                      (agent.pos[1] - self.pos[1])**2)