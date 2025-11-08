import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from models.sta_model import STAModel

def calculate_cost_adjusted_performance(model_results, Tc):
    """
    Calculate cost-adjusted performance.
    
    In auction: Discoverers are strategic (cost=2), helpers are reactive (cost=1)
    In swarm: All agents are reactive (cost=1)
    
    Cost per task = (1 strategic × 2) + ((Tc-1) reactive × 1) = 2 + (Tc-1) = Tc + 1
    For Tc=3: Auction cost = 4 per task, Swarm cost = 3 per task
    
    Cost-adjusted performance = (tasks/iteration) / (cost per task)
    """
    # For auction: 1 strategic (cost 2) + (Tc-1) reactive (cost 1) = cost of Tc+1
    auction_cost_per_task = Tc + 1
    
    # For swarm: All Tc agents are reactive (cost 1 each) = cost of Tc
    swarm_cost_per_task = Tc
    
    return auction_cost_per_task, swarm_cost_per_task

def run_part2c():
    """
    Part 2(c): Cost-Benefit Analysis
    - Strategic agents (auctioneers) cost 2× reactive agents
    - Analyze cost-adjusted performance
    - Determine if auction's complexity is justified
    """
    
    print("=" * 80)
    print("Part 2(c): Cost-Benefit Analysis")
    print("=" * 80)
    
    # Parameters
    communication_ranges = [0, 100, 200, 300, 400, 600, 1000, 1400]
    num_agents = 30
    num_tasks = 2
    task_radius = 50
    required_agents = 3  # Tc
    agent_speed = 25
    num_iterations = 2000
    warmup_iterations = 1000
    num_runs = 20
    
    print(f"\nCost Model:")
    print(f"  Strategic Agent (Auctioneer): Cost = 2 units")
    print(f"  Reactive Agent (Helper/Swarm): Cost = 1 unit")
    print(f"\nPer-Task Costs:")
    print(f"  Auction: 1 strategic + {required_agents-1} reactive = 2 + {required_agents-1} = {required_agents+1} units")
    print(f"  Swarm:   {required_agents} reactive = {required_agents} units")
    print(f"\nCost ratio: Auction/Swarm = {(required_agents+1)/required_agents:.3f}x")
    
    auction_cost, swarm_cost = calculate_cost_adjusted_performance(None, required_agents)
    
    # Run all protocols
    print(f"\n{'='*80}")
    print("Running simulations for all protocols...")
    print(f"{'='*80}")
    
    results = {
        'callout': {'mean_rates': [], 'std_rates': []},
        'calloff': {'mean_rates': [], 'std_rates': []},
        'auction': {'mean_rates': [], 'std_rates': []}
    }
    
    for Rd in communication_ranges:
        print(f"\nTesting Rd = {Rd}...")
        
        # Call-Out
        callout_rates = []
        for run in range(num_runs):
            model = STAModel(
                num_agents=num_agents, num_tasks=num_tasks,
                task_radius=task_radius, required_agents_per_task=required_agents,
                agent_speed=agent_speed, communication_range=Rd,
                use_communication=True, use_calloff=False, use_auction=False,
                seed=600 + run
            )
            model.run_model(num_iterations)
            steady_data = model.get_completion_rate_over_time()[warmup_iterations:]
            callout_rates.append(np.mean(steady_data))
        
        results['callout']['mean_rates'].append(np.mean(callout_rates))
        results['callout']['std_rates'].append(np.std(callout_rates))
        
        # Call-Off
        calloff_rates = []
        for run in range(num_runs):
            model = STAModel(
                num_agents=num_agents, num_tasks=num_tasks,
                task_radius=task_radius, required_agents_per_task=required_agents,
                agent_speed=agent_speed, communication_range=Rd,
                use_communication=True, use_calloff=True, use_auction=False,
                seed=600 + run
            )
            model.run_model(num_iterations)
            steady_data = model.get_completion_rate_over_time()[warmup_iterations:]
            calloff_rates.append(np.mean(steady_data))
        
        results['calloff']['mean_rates'].append(np.mean(calloff_rates))
        results['calloff']['std_rates'].append(np.std(calloff_rates))
        
        # Auction
        auction_rates = []
        for run in range(num_runs):
            model = STAModel(
                num_agents=num_agents, num_tasks=num_tasks,
                task_radius=task_radius, required_agents_per_task=required_agents,
                agent_speed=agent_speed, communication_range=Rd,
                use_communication=False, use_calloff=False, use_auction=True,
                seed=600 + run
            )
            model.run_model(num_iterations)
            steady_data = model.get_completion_rate_over_time()[warmup_iterations:]
            auction_rates.append(np.mean(steady_data))
        
        results['auction']['mean_rates'].append(np.mean(auction_rates))
        results['auction']['std_rates'].append(np.std(auction_rates))
        
        print(f"  Call-Out: {results['callout']['mean_rates'][-1]:.4f}")
        print(f"  Call-Off: {results['calloff']['mean_rates'][-1]:.4f}")
        print(f"  Auction:  {results['auction']['mean_rates'][-1]:.4f}")
    
    # Convert to numpy arrays
    for protocol in results.values():
        protocol['mean_rates'] = np.array(protocol['mean_rates'])
        protocol['std_rates'] = np.array(protocol['std_rates'])
    
    # Calculate cost-adjusted performance
    results_cost_adjusted = {
        'callout': results['callout']['mean_rates'] / swarm_cost,
        'calloff': results['calloff']['mean_rates'] / swarm_cost,
        'auction': results['auction']['mean_rates'] / auction_cost
    }
    
    # Create comprehensive cost analysis plots
    fig = plt.figure(figsize=(18, 12))
    gs = fig.add_gridspec(4, 3, hspace=0.4, wspace=0.3)
    
    colors = {'callout': 'blue', 'calloff': 'green', 'auction': 'purple'}
    labels = {'callout': 'Call-Out', 'calloff': 'Call-Off', 'auction': 'Auction'}
    
    # Plot 1: Raw Performance
    ax1 = fig.add_subplot(gs[0, :])
    for protocol in ['callout', 'calloff', 'auction']:
        ax1.errorbar(communication_ranges, results[protocol]['mean_rates'],
                     yerr=results[protocol]['std_rates'],
                     marker='o', linewidth=2, markersize=7, capsize=4,
                     label=f"{labels[protocol]} (raw)", color=colors[protocol], alpha=0.7)
    
    ax1.set_xlabel('Communication Range (Rd)', fontsize=12)
    ax1.set_ylabel('Tasks per Iteration', fontsize=12)
    ax1.set_title('Raw Performance (Without Cost Adjustment)',
                  fontsize=13, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=10)
    
    # Plot 2: Cost-Adjusted Performance
    ax2 = fig.add_subplot(gs[1, :])
    for protocol in ['callout', 'calloff', 'auction']:
        ax2.plot(communication_ranges, results_cost_adjusted[protocol],
                marker='s', linewidth=2, markersize=7,
                label=f"{labels[protocol]} (÷cost)", color=colors[protocol], alpha=0.7)
    
    ax2.set_xlabel('Communication Range (Rd)', fontsize=12)
    ax2.set_ylabel('Cost-Adjusted Performance (Tasks/Unit Cost)', fontsize=12)
    ax2.set_title('Cost-Adjusted Performance (Accounting for Agent Costs)',
                  fontsize=13, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.legend(fontsize=10)
    
    # Plot 3: Raw vs Cost-Adjusted for Auction
    ax3 = fig.add_subplot(gs[2, 0])
    ax3.plot(communication_ranges, results['auction']['mean_rates'],
            marker='o', linewidth=2, label='Raw', color='purple')
    ax3.plot(communication_ranges, results_cost_adjusted['auction'],
            marker='s', linewidth=2, label='Cost-Adjusted', color='darkviolet', linestyle='--')
    ax3.set_xlabel('Comm Range (Rd)', fontsize=10)
    ax3.set_ylabel('Performance', fontsize=10)
    ax3.set_title('Auction: Raw vs Cost-Adjusted', fontsize=11, fontweight='bold')
    ax3.grid(True, alpha=0.3)
    ax3.legend()
    
    # Plot 4: Cost-adjusted comparison at optimal Rd
    ax4 = fig.add_subplot(gs[2, 1])
    optimal_idx = 4  # Rd=400
    raw_perfs = [results[p]['mean_rates'][optimal_idx] for p in labels.keys()]
    cost_adj_perfs = [results_cost_adjusted[p][optimal_idx] for p in labels.keys()]
    
    x = np.arange(len(labels))
    width = 0.35
    ax4.bar(x - width/2, raw_perfs, width, label='Raw', alpha=0.7,
           color=[colors[p] for p in labels.keys()])
    ax4.bar(x + width/2, cost_adj_perfs, width, label='Cost-Adjusted', alpha=0.7,
           color=[colors[p] for p in labels.keys()], hatch='//')
    ax4.set_xticks(x)
    ax4.set_xticklabels([labels[p] for p in labels.keys()])
    ax4.set_ylabel('Performance', fontsize=10)
    ax4.set_title(f'Rd=400: Raw vs Cost-Adjusted', fontsize=11, fontweight='bold')
    ax4.legend()
    ax4.grid(True, alpha=0.3, axis='y')
    
    # Plot 5: Cost efficiency ratio (auction/call-off)
    ax5 = fig.add_subplot(gs[2, 2])
    # Raw ratio
    raw_ratio = results['auction']['mean_rates'] / results['calloff']['mean_rates']
    # Cost-adjusted ratio
    cost_ratio = results_cost_adjusted['auction'] / results_cost_adjusted['calloff']
    
    ax5.plot(communication_ranges, raw_ratio, marker='o', linewidth=2,
            label='Raw Ratio', color='purple')
    ax5.plot(communication_ranges, cost_ratio, marker='s', linewidth=2,
            label='Cost-Adj Ratio', color='darkviolet', linestyle='--')
    ax5.axhline(y=1, color='black', linestyle=':', linewidth=1, label='Equal')
    ax5.set_xlabel('Comm Range (Rd)', fontsize=10)
    ax5.set_ylabel('Auction / Call-Off Ratio', fontsize=10)
    ax5.set_title('Relative Efficiency', fontsize=11, fontweight='bold')
    ax5.grid(True, alpha=0.3)
    ax5.legend()
    
    # Plot 6: Value proposition analysis
    ax6 = fig.add_subplot(gs[3, :])
    
    # Calculate value score: (performance gain × cost efficiency)
    calloff_baseline = results_cost_adjusted['calloff']
    callout_value = (results_cost_adjusted['callout'] - calloff_baseline) / calloff_baseline * 100
    auction_value = (results_cost_adjusted['auction'] - calloff_baseline) / calloff_baseline * 100
    
    width = 0.35
    x = np.arange(len(communication_ranges))
    ax6.bar(x - width/2, callout_value, width, label='Call-Out vs Call-Off',
           color='blue', alpha=0.7)
    ax6.bar(x + width/2, auction_value, width, label='Auction vs Call-Off',
           color='purple', alpha=0.7)
    ax6.axhline(y=0, color='black', linestyle='-', linewidth=1)
    ax6.set_xticks(x)
    ax6.set_xticklabels(communication_ranges)
    ax6.set_xlabel('Communication Range (Rd)', fontsize=11)
    ax6.set_ylabel('Cost-Adjusted Performance Difference (%)', fontsize=11)
    ax6.set_title('Value Proposition: Is Extra Cost Justified?',
                  fontsize=12, fontweight='bold')
    ax6.legend()
    ax6.grid(True, alpha=0.3, axis='y')
    
    plt.savefig('results/part2c_results.png', dpi=300, bbox_inches='tight')
    print(f"\n{'='*80}")
    print(f"Plot saved to: results/part2c_results.png")
    plt.show()
    
    # Detailed cost analysis
    print("\n" + "="*100)
    print("COST-BENEFIT ANALYSIS:")
    print("="*100)
    print(f"{'Rd':<8} {'Protocol':<12} {'Raw Perf':<12} {'Cost':<8} {'Adj Perf':<12} {'vs CallOff':<12}")
    print("-" * 100)
    
    for i, Rd in enumerate(communication_ranges):
        for protocol in ['callout', 'calloff', 'auction']:
            cost = auction_cost if protocol == 'auction' else swarm_cost
            raw = results[protocol]['mean_rates'][i]
            adj = results_cost_adjusted[protocol][i]
            vs_calloff = ((adj - results_cost_adjusted['calloff'][i]) / 
                         results_cost_adjusted['calloff'][i] * 100)
            
            print(f"{Rd:<8} {labels[protocol]:<12} {raw:<12.4f} {cost:<8} "
                  f"{adj:<12.4f} {vs_calloff:+11.2f}%")
    
    # Comprehensive findings
    print("\n" + "="*100)
    print("COMPREHENSIVE COST-BENEFIT FINDINGS:")
    print("="*100)
    
    # Calculate summary statistics
    avg_raw_calloff = np.mean(results['calloff']['mean_rates'])
    avg_raw_auction = np.mean(results['auction']['mean_rates'])
    avg_adj_calloff = np.mean(results_cost_adjusted['calloff'])
    avg_adj_auction = np.mean(results_cost_adjusted['auction'])
    
    raw_advantage = ((avg_raw_auction - avg_raw_calloff) / avg_raw_calloff * 100)
    cost_adjusted_advantage = ((avg_adj_auction - avg_adj_calloff) / avg_adj_calloff * 100)
    
    best_raw_auction = np.max(results['auction']['mean_rates'])
    best_adj_auction = np.max(results_cost_adjusted['auction'])
    best_raw_calloff = np.max(results['calloff']['mean_rates'])
    best_adj_calloff = np.max(results_cost_adjusted['calloff'])
    
    print(f"""
1. COST STRUCTURE:

   Per-Task Agent Costs:
   - Call-Out:  {swarm_cost} units ({required_agents} reactive @ 1 each)
   - Call-Off:  {swarm_cost} units ({required_agents} reactive @ 1 each)
   - Auction:   {auction_cost} units (1 strategic @ 2 + {required_agents-1} reactive @ 1)
   
   Cost Premium: Auction is {((auction_cost/swarm_cost - 1) * 100):.1f}% more expensive per task

2. RAW PERFORMANCE (Without Cost Adjustment):

   Average Performance:
   - Call-Off: {avg_raw_calloff:.4f} tasks/iteration
   - Auction:  {avg_raw_auction:.4f} tasks/iteration
   - Difference: {raw_advantage:+.2f}% {'(Auction better)' if raw_advantage > 0 else '(Call-Off better)'}
   
   Best Performance:
   - Call-Off: {best_raw_calloff:.4f}
   - Auction:  {best_raw_auction:.4f}
   - Winner: {'Auction' if best_raw_auction > best_raw_calloff else 'Call-Off'}

3. COST-ADJUSTED PERFORMANCE:

   Average Cost-Adjusted Performance:
   - Call-Off: {avg_adj_calloff:.4f} tasks/unit-cost
   - Auction:  {avg_adj_auction:.4f} tasks/unit-cost
   - Difference: {cost_adjusted_advantage:+.2f}% {'(Auction better)' if cost_adjusted_advantage > 0 else '(Call-Off better)'}
   
   Best Cost-Adjusted Performance:
   - Call-Off: {best_adj_calloff:.4f}
   - Auction:  {best_adj_auction:.4f}
   - Winner: {'Auction' if best_adj_auction > best_adj_calloff else 'Call-Off'}

4. COST-BENEFIT VERDICT:

   Raw Performance: Auction {'' if raw_advantage > 0 else 'does NOT '}provides {abs(raw_advantage):.1f}% advantage
   Cost-Adjusted:   Auction {'' if cost_adjusted_advantage > 0 else 'does NOT '}provides {abs(cost_adjusted_advantage):.1f}% advantage
   
   Cost Impact: {'Negative' if cost_adjusted_advantage < raw_advantage else 'Neutral/Positive'}
   
   The {auction_cost/swarm_cost:.1f}x cost premium {'is justified' if cost_adjusted_advantage > 5 else 'is NOT justified'}
   
   Recommendation: {
       'Use Auction - Cost justified by performance gains' if cost_adjusted_advantage > 5
       else 'Use Call-Off - Better cost-performance ratio' if cost_adjusted_advantage < -5
       else 'Mixed - Performance similar, choose based on other factors'
   }

5. DETAILED TRADE-OFF ANALYSIS:

   Factors Favoring Call-Off:
   {'✓ Better cost-adjusted performance' if cost_adjusted_advantage < 0 else '✗ Lower cost-adjusted performance'}
   ✓ Lower per-task cost ({swarm_cost} vs {auction_cost} units)
   ✓ Simpler implementation (all agents identical)
   ✓ Easier deployment and maintenance
   ✓ More robust (no specialized agents)
   
   Factors Favoring Auction:
   {'✓ Better raw performance' if raw_advantage > 0 else '✗ Lower raw performance'}
   ✓ Optimal agent selection (distance-based)
   ✓ Game-theoretic foundation
   ✓ Systematic coordination
   ✗ Higher complexity ({auction_cost/swarm_cost:.1f}x cost)
   ✗ Requires strategic agents

6. WHEN TO CHOOSE EACH PROTOCOL:

   Choose Call-Off when:
   • Cost efficiency is priority
   • System simplicity valued
   • All agents should be equivalent
   • Robust to agent failures needed
   {'• Performance adequate for needs' if cost_adjusted_advantage < 5 else ''}
   
   Choose Auction when:
   {'• Raw performance is critical' if raw_advantage > 5 else ''}
   • Optimal allocation needed
   • Strategic agents available
   • Game-theoretic guarantees desired
   • Cost premium acceptable

7. BREAK-EVEN ANALYSIS:

   For auction to be cost-effective, need:
   Performance gain > Cost premium
   
   Required improvement: {((auction_cost/swarm_cost - 1) * 100):.1f}%
   Actual improvement: {raw_advantage:.1f}%
   
   Break-even: {'YES - Auction pays for itself' if raw_advantage > ((auction_cost/swarm_cost - 1) * 100)
                else 'NO - Auction does not pay for cost premium'}

8. PRACTICAL IMPLICATIONS:

   Resource Budget Analysis:
   If budget allows N total agent-units:
   
   With Call-Off: N/{swarm_cost} = {100//swarm_cost} tasks (if 100 units available)
   With Auction:  N/{auction_cost} = {100//auction_cost} tasks (if 100 units available)
   
   Throughput difference: {((100//swarm_cost - 100//auction_cost)/(100//auction_cost) * 100):.1f}% {'more' if 100//swarm_cost > 100//auction_cost else 'fewer'} tasks with Call-Off
   
   For equal throughput, Auction needs:
   {auction_cost/swarm_cost:.1f}x more budget than Call-Off

9. FINAL RECOMMENDATION:

   Based on cost-benefit analysis with Tc={required_agents}:
   
   {'★★★ CALL-OFF IS RECOMMENDED ★★★' if cost_adjusted_advantage < 0
    else '★★★ AUCTION IS RECOMMENDED ★★★' if cost_adjusted_advantage > 5
    else '★★★ BOTH PROTOCOLS VIABLE ★★★'}
   
   Reasoning:
   {f'Call-Off provides {abs(cost_adjusted_advantage):.1f}% better cost-adjusted performance'
    if cost_adjusted_advantage < -2
    else f'Auction provides {cost_adjusted_advantage:.1f}% better cost-adjusted performance'
    if cost_adjusted_advantage > 5
    else 'Cost-adjusted performance is similar (within 5%)'}
   
   The simpler, more cost-effective protocol should be preferred
   unless there are specific requirements for game-theoretic optimality.
    """)
    
    return results, results_cost_adjusted

if __name__ == "__main__":
    run_part2c()