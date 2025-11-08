import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from models.sta_model import STAModel

def run_part1b():
    """
    Part 1(b): Multiple agents, single task scenario
    - Vary R = 3, 5, 10, 20, 30
    - T = 1, Tc = 1, Tr = 50, Rv = 25
    """
    
    print("=" * 60)
    print("Part 1(b): Performance as Function of Agent Number")
    print("=" * 60)
    
    # Parameters
    agent_counts = [3, 5, 10, 20, 30]
    num_tasks = 1
    task_radius = 50
    required_agents = 1
    agent_speed = 25
    num_iterations = 1000
    num_runs = 10  # Multiple runs for statistical reliability
    
    print(f"\nParameters:")
    print(f"  Agent counts (R): {agent_counts}")
    print(f"  Number of tasks (T): {num_tasks}")
    print(f"  Task radius (Tr): {task_radius}")
    print(f"  Required agents per task (Tc): {required_agents}")
    print(f"  Agent speed (Rv): {agent_speed}")
    print(f"  Iterations per run: {num_iterations}")
    print(f"  Number of runs: {num_runs}")
    
    # Store results
    results = {
        'agent_counts': agent_counts,
        'mean_rates': [],
        'std_rates': [],
        'all_rates': []
    }
    
    # Run simulations for each agent count
    for num_agents in agent_counts:
        print(f"\n{'='*40}")
        print(f"Running simulations for R = {num_agents} agents")
        print(f"{'='*40}")
        
        run_rates = []
        
        for run in range(num_runs):
            model = STAModel(
                num_agents=num_agents,
                num_tasks=num_tasks,
                task_radius=task_radius,
                required_agents_per_task=required_agents,
                agent_speed=agent_speed,
                seed=42 + run  # Different seed for each run
            )
            
            model.run_model(num_iterations)
            avg_rate = model.get_average_completion_rate()
            run_rates.append(avg_rate)
            
            print(f"  Run {run+1}/{num_runs}: {avg_rate:.4f} tasks/iteration")
        
        mean_rate = np.mean(run_rates)
        std_rate = np.std(run_rates)
        
        results['mean_rates'].append(mean_rate)
        results['std_rates'].append(std_rate)
        results['all_rates'].append(run_rates)
        
        print(f"  Mean: {mean_rate:.4f} ± {std_rate:.4f}")
    
    # Convert to numpy arrays for plotting
    results['mean_rates'] = np.array(results['mean_rates'])
    results['std_rates'] = np.array(results['std_rates'])
    
    # Create plots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
    
    # Plot 1: Mean performance with error bars
    ax1.errorbar(agent_counts, results['mean_rates'], 
                 yerr=results['std_rates'], 
                 marker='o', linewidth=2, markersize=8, capsize=5)
    ax1.set_xlabel('Number of Agents (R)', fontsize=11)
    ax1.set_ylabel('Average Tasks per Iteration', fontsize=11)
    ax1.set_title('Performance vs Number of Agents (with std dev)', 
                  fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.set_xticks(agent_counts)
    
    # Plot 2: Box plot showing distribution
    box_data = [results['all_rates'][i] for i in range(len(agent_counts))]
    ax2.boxplot(box_data, labels=agent_counts)
    ax2.set_xlabel('Number of Agents (R)', fontsize=11)
    ax2.set_ylabel('Average Tasks per Iteration', fontsize=11)
    ax2.set_title('Distribution of Performance', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Plot 3: Performance improvement ratio (normalized to R=3)
    baseline = results['mean_rates'][0]
    normalized = results['mean_rates'] / baseline
    ax3.plot(agent_counts, normalized, marker='s', linewidth=2, 
             markersize=8, color='green')
    ax3.set_xlabel('Number of Agents (R)', fontsize=11)
    ax3.set_ylabel('Performance Ratio (relative to R=3)', fontsize=11)
    ax3.set_title('Normalized Performance Improvement', 
                  fontsize=12, fontweight='bold')
    ax3.grid(True, alpha=0.3)
    ax3.set_xticks(agent_counts)
    ax3.axhline(y=1, color='r', linestyle='--', alpha=0.5)
    
    # Plot 4: Efficiency (tasks per agent)
    efficiency = results['mean_rates'] / np.array(agent_counts)
    ax4.plot(agent_counts, efficiency, marker='^', linewidth=2, 
             markersize=8, color='red')
    ax4.set_xlabel('Number of Agents (R)', fontsize=11)
    ax4.set_ylabel('Tasks per Iteration per Agent', fontsize=11)
    ax4.set_title('Agent Efficiency', fontsize=12, fontweight='bold')
    ax4.grid(True, alpha=0.3)
    ax4.set_xticks(agent_counts)
    
    plt.tight_layout()
    
    # Save plot
    os.makedirs('results', exist_ok=True)
    plt.savefig('results/part1b_results.png', dpi=300, bbox_inches='tight')
    print(f"\n{'='*60}")
    print(f"Plot saved to: results/part1b_results.png")
    plt.show()
    
    # Print summary table
    print("\n" + "="*60)
    print("SUMMARY TABLE:")
    print("="*60)
    print(f"{'Agents (R)':<12} {'Mean Rate':<15} {'Std Dev':<15} {'Efficiency':<15}")
    print("-" * 60)
    for i, R in enumerate(agent_counts):
        eff = results['mean_rates'][i] / R
        print(f"{R:<12} {results['mean_rates'][i]:<15.4f} "
              f"{results['std_rates'][i]:<15.4f} {eff:<15.4f}")
    
    # Analysis
    print("\n" + "="*60)
    print("ANALYSIS:")
    print("="*60)
    print(f"""
Key Observations:
1. Performance increases with more agents (more coverage)
2. With T=1 and Tc=1, only 1 agent works at a time
3. Additional agents increase probability of finding task
4. Efficiency (per-agent) decreases with more agents (diminishing returns)

Expected Behavior:
- Linear improvement initially (more agents = more coverage)
- Diminishing returns as search area saturates
- Theoretical maximum: ~{1000*1000/(np.pi*50**2):.2f} tasks (area coverage)

Scalability:
- Going from 3 to 30 agents: {results['mean_rates'][-1]/results['mean_rates'][0]:.2f}x improvement
- But efficiency drops from {efficiency[0]:.4f} to {efficiency[-1]:.4f} per agent
    """)

if __name__ == "__main__":
    run_part1b()