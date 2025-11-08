import mesa
import numpy as np
from .agent import STAAgent
from .task import Task

class STAModel(mesa.Model):
    """Search and Task Allocation Model."""
    
    def __init__(self, num_agents, num_tasks, task_radius, 
                 required_agents_per_task, agent_speed, 
                 communication_range=0, seed=None):
        super().__init__()
        
        # Parameters
        self.num_agents = num_agents  # R
        self.num_tasks = num_tasks  # T
        self.task_radius = task_radius  # Tr
        self.required_agents_per_task = required_agents_per_task  # Tc
        self.agent_speed = agent_speed  # Rv
        self.communication_range = communication_range  # Rd
        
        # Statistics
        self.tasks_completed = 0
        self.tasks_completed_per_iteration = []
        
        # Set random seed if provided
        if seed is not None:
            np.random.seed(seed)
            self.random = np.random.RandomState(seed)
        
        # Create agents with random initial positions
        self.agents = []
        for i in range(self.num_agents):
            agent = STAAgent(i, self, self.agent_speed)
            # Random initial position in [0, 1000] x [0, 1000]
            agent.pos = (self.random.uniform(0, 1000), 
                        self.random.uniform(0, 1000))
            self.agents.append(agent)
        
        # Create initial tasks
        self.tasks = []
        for i in range(self.num_tasks):
            self._spawn_task(i)
    
    def _spawn_task(self, task_id):
        """Spawn a new task at a random location."""
        pos = (self.random.uniform(0, 1000), self.random.uniform(0, 1000))
        task = Task(task_id, pos, self.task_radius, 
                   self.required_agents_per_task)
        self.tasks.append(task)
        
        # Check if newly spawned task immediately has enough agents
        self._check_immediate_completion(task)
    
    def _check_immediate_completion(self, task):
        """Check if a newly spawned task can be completed immediately."""
        for agent in self.agents:
            if agent.mode == "searching" and task.is_within_range(agent.pos):
                task.add_agent(agent)
                agent.current_task = task
                agent.mode = "waiting"
    
    def step(self):
        """Execute one step of the model."""
        # Track tasks completed this iteration
        tasks_completed_this_iter = 0
        
        # Move all agents
        for agent in self.agents:
            agent.step()
        
        # Check task completion
        completed_tasks = []
        for task in self.tasks:
            if task.check_completion():
                completed_tasks.append(task)
                tasks_completed_this_iter += 1
                self.tasks_completed += 1
                
                # Release agents working on completed task
                for agent in task.agents_in_range:
                    agent.release()
        
        # Remove completed tasks and spawn new ones
        for task in completed_tasks:
            self.tasks.remove(task)
            self._spawn_task(task.task_id)
        
        # Record statistics
        self.tasks_completed_per_iteration.append(tasks_completed_this_iter)
    
    def run_model(self, num_iterations):
        """Run the model for a specified number of iterations."""
        for _ in range(num_iterations):
            self.step()
    
    def get_average_completion_rate(self):
        """Calculate average tasks completed per iteration."""
        if len(self.tasks_completed_per_iteration) == 0:
            return 0
        return np.mean(self.tasks_completed_per_iteration)
    
    def get_completion_rate_over_time(self):
        """Get the task completion rate over time."""
        return self.tasks_completed_per_iteration