import mesa
import numpy as np

class STAAgent(mesa.Agent):
    """An agent that searches for and completes tasks."""
    
    def __init__(self, unique_id, model, speed):
        super().__init__(unique_id, model)
        self.speed = speed  # Rv - movement speed per iteration
        self.pos = None  # Will be set by model
        self.current_task = None  # Task agent is working on
        self.mode = "searching"  # searching, waiting, responding
        
    def step(self):
        """Execute one step of agent behavior."""
        if self.mode == "searching":
            self.random_move()
            self.check_for_tasks()
        elif self.mode == "waiting":
            # Agent is at a task, waiting for it to complete
            pass
    
    def random_move(self):
        """Move randomly within speed limit using uniform random walk."""
        # Generate random angle
        angle = self.random.uniform(0, 2 * np.pi)
        
        # Generate random distance (uniform within circle)
        distance = self.random.uniform(0, self.speed)
        
        # Calculate new position
        new_x = self.pos[0] + distance * np.cos(angle)
        new_y = self.pos[1] + distance * np.sin(angle)
        
        # Ensure agent stays within bounds [0, 1000]
        new_x = np.clip(new_x, 0, 1000)
        new_y = np.clip(new_y, 0, 1000)
        
        self.pos = (new_x, new_y)
    
    def check_for_tasks(self):
        """Check if agent is within range of any tasks."""
        for task in self.model.tasks:
            if task.is_within_range(self.pos):
                self.current_task = task
                self.mode = "waiting"
                task.add_agent(self)
                return
    
    def release(self):
        """Release agent back to searching mode."""
        self.mode = "searching"
        self.current_task = None
    
    def distance_to(self, pos):
        """Calculate Euclidean distance to a position."""
        return np.sqrt((self.pos[0] - pos[0])**2 + (self.pos[1] - pos[1])**2)