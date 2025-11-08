import mesa
import numpy as np

class STAAgent(mesa.Agent):
    """An agent that searches for and completes tasks."""
    
    def __init__(self, unique_id, model, speed, agent_type="reactive"):
        super().__init__(unique_id, model)
        self.speed = speed  # Rv - movement speed per iteration
        self.pos = None  # Will be set by model
        self.current_task = None  # Task agent is working on
        self.mode = "searching"  # searching, waiting, responding
        self.agent_type = agent_type  # "strategic" or "reactive"
        
        # Communication protocol variables
        self.target_task = None  # Task agent is responding to
        self.response_timer = 0  # Iterations remaining in response mode
        self.discovered_task = False  # Did this agent discover the task via free search?
        
        # Auction variables
        self.current_bid = None  # Current bid in auction
        self.auction_task = None  # Task being auctioned
        
    def step(self):
        """Execute one step of agent behavior."""
        if self.mode == "searching":
            self.random_move()
            self.check_for_tasks()
        elif self.mode == "waiting":
            # Agent is at a task, waiting for it to complete
            pass
        elif self.mode == "responding":
            self.respond_to_signal()
    
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
                # Mark if this agent discovered the task via free search
                self.discovered_task = (self.mode != "responding")
                task.add_agent(self)
                
                # Handle based on protocol
                if self.model.use_auction and self.discovered_task:
                    # Auction protocol: become auctioneer
                    self.conduct_auction(task)
                elif self.model.use_communication and self.discovered_task:
                    # Swarm protocol: emit call-out signal
                    self.emit_callout_signal(task)
                return
    
    def conduct_auction(self, task):
        """Conduct an auction for the discovered task."""
        if self.model.communication_range <= 0:
            return
        
        # This agent is the auctioneer
        bidders = []
        
        # Find agents within communication range who can bid
        for agent in self.model.agents:
            if agent.unique_id == self.unique_id:
                continue
            
            distance = self.distance_to(agent.pos)
            if distance <= self.model.communication_range:
                # Agent can participate if in searching mode
                if agent.mode == "searching":
                    # Agent bids with their distance to the auctioneer
                    bid = {
                        'agent': agent,
                        'distance': distance
                    }
                    bidders.append(bid)
        
        # Sort bidders by distance (lower is better)
        bidders.sort(key=lambda b: b['distance'])
        
        # Recruit the closest (Tc - 1) agents (auctioneer already at task)
        needed = self.model.required_agents_per_task - 1
        winners = bidders[:needed]
        
        # Assign winners to move toward task
        for winner in winners:
            agent = winner['agent']
            agent.mode = "responding"
            agent.target_task = task
            agent.response_timer = self.model.response_duration if hasattr(self.model, 'response_duration') else 60
    
    def emit_callout_signal(self, task):
        """Emit a call-out signal to nearby agents."""
        if self.model.communication_range <= 0:
            return
            
        # Find agents within communication range
        for agent in self.model.agents:
            if agent.unique_id == self.unique_id:
                continue
            
            distance = self.distance_to(agent.pos)
            if distance <= self.model.communication_range:
                # Agent receives signal if in searching mode
                if agent.mode == "searching":
                    agent.receive_callout_signal(task)
    
    def receive_callout_signal(self, task):
        """Receive a call-out signal and start responding."""
        self.mode = "responding"
        self.target_task = task
        self.response_timer = self.model.response_duration
    
    def respond_to_signal(self):
        """Move toward the target task in response to signal."""
        if self.target_task is None or self.target_task not in self.model.tasks:
            # Task no longer exists or invalid
            self.release()
            return
        
        # Decrement response timer
        self.response_timer -= 1
        
        # Check if already at task
        if self.target_task.is_within_range(self.pos):
            self.current_task = self.target_task
            self.mode = "waiting"
            self.discovered_task = False  # Responding agent, not discoverer
            self.target_task.add_agent(self)
            self.target_task = None
            return
        
        # If timer expires, return to searching
        if self.response_timer <= 0:
            self.release()
            return
        
        # Move toward task
        self.move_toward_task(self.target_task)
    
    def move_toward_task(self, task):
        """Move toward a task at maximum speed."""
        # Calculate direction to task
        dx = task.pos[0] - self.pos[0]
        dy = task.pos[1] - self.pos[1]
        distance = np.sqrt(dx**2 + dy**2)
        
        if distance == 0:
            return
        
        # Normalize direction and move at speed
        move_distance = min(self.speed, distance)
        new_x = self.pos[0] + (dx / distance) * move_distance
        new_y = self.pos[1] + (dy / distance) * move_distance
        
        # Ensure within bounds
        new_x = np.clip(new_x, 0, 1000)
        new_y = np.clip(new_y, 0, 1000)
        
        self.pos = (new_x, new_y)
    
    def receive_calloff_signal(self):
        """Receive a call-off signal and return to searching."""
        if self.mode == "responding" and self.target_task is not None:
            # Release from responding mode
            self.release()
    
    def release(self):
        """Release agent back to searching mode."""
        self.mode = "searching"
        self.current_task = None
        self.target_task = None
        self.response_timer = 0
        self.discovered_task = False
    
    def distance_to(self, pos):
        """Calculate Euclidean distance to a position."""
        return np.sqrt((self.pos[0] - pos[0])**2 + (self.pos[1] - pos[1])**2)