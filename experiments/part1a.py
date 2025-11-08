import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from models.sta_model import STAModel

def run_part1a():
    """
    Part 1(a): Single agent, single task scenario
    - T = 1 (one simultaneous task)
    - Tc = 1 (one agent required)
    - Tr = 50 (task radius)
    - R = 1 (one agent)
    - Rv = 25 (agent speed)
    """
    
    print("=" * 60)
    print("Part 1(a): Single Agent, Single Task")
    print("=" * 60)
    
    # Parameters
    num_agents = 1
    num_tasks = 1
    task_radius = 50
    required_agents = 1
    agent_speed = 25
    num_iterations = 1000
    
    print(f"\nParameters:")
    print(f"  Number of agents (R): {num_agents}")
    print(f"  Number of tasks (T): {num_tasks}")
    print(f"  Task radius (Tr): {task_radius}")
    print(f"  Required agents per task (Tc): {required_agents}")
    print(f"  Agent speed (Rv): {agent_speed}")
    print(f"  Iterations: {num_iterations}")
    
    # Run simulation
    print(f"\nRunning simulation...")
    model = STAModel(
        num_agents=num_agents,
        num_tasks=num_tasks,
        task_radius=task_radius,
        required_agents_per_task=required_agents,
        agent_speed=agent_speed,
        seed=42
    )
    
    model.run_model(num_iterations)
    
    # Get results
    completion_rate = model.get_completion_rate_over_time()
    avg_completion_rate = model.get_average_completion_rate()
    total_completed = model.tasks_completed
    
    print(f"\nResults:")
    print(f"  Total tasks completed: {total_completed}")
    print(f"  Average tasks per iteration: {avg_completion_rate:.4f}")
    
    # Plot results
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    # Plot 1: Tasks completed per iteration over time
    ax1.plot(completion_rate, linewidth=0.8, alpha=0.7)
    ax1.set_xlabel('Iteration', fontsize=11)
    ax1.set_ylabel('Tasks Completed', fontsize=11)
    ax1.set_title('Tasks Completed per Iteration (Single Agent)', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.axhline(y=avg_completion_rate, color='r', linestyle='--', 
                label=f'Average: {avg_completion_rate:.4f}', linewidth=2)
    ax1.legend()
    
    # Plot 2: Cumulative tasks completed
    cumulative = np.cumsum(completion_rate)
    ax2.plot(cumulative, linewidth=1.5, color='green')
    ax2.set_xlabel('Iteration', fontsize=11)
    ax2.set_ylabel('Cumulative Tasks Completed', fontsize=11)
    ax2.set_title('Cumulative Task Completion', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Save plot
    os.makedirs('results', exist_ok=True)
    plt.savefig('results/part1a_results.png', dpi=300, bbox_inches='tight')
    print(f"\nPlot saved to: results/part1a_results.png")
    plt.show()
    
    # Analysis and discussion
    print("\n" + "=" * 60)
    print("ANALYSIS:")
    print("=" * 60)
    print("""
Movement Model:
- Used uniform random walk: random angle [0, 2π] and random distance [0, Rv]
- This ensures agent explores the space uniformly over time
- Boundary reflections keep agent within [0, 1000] × [0, 1000]

Performance Metric Analysis:
- Tasks completed per iteration is binary (0 or 1) for single agent
- This creates a noisy, discrete signal
- Average completion rate gives better steady-state performance measure
- Cumulative completion shows overall system efficiency

Is this a good measure?
- For single agent: YES for average rate, but per-iteration is too noisy
- Better metrics could include:
  * Average time between task completions
  * Spatial coverage efficiency
  * Expected task completion time from spawn
    """)

if __name__ == "__main__":
    run_part1a()