import matplotlib.pyplot as plt
import os

def main():
    figures_dir = os.path.join('output', 'latex', 'figures')
    os.makedirs(figures_dir, exist_ok=True)
    
    plt.figure(figsize=(8, 5))
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 6, 8, 10]
    
    plt.plot(x, y, marker='o', linestyle='-', color='b', label='Growth')
    plt.title('Agent Collaboration Growth')
    plt.xlabel('Number of Agents')
    plt.ylabel('Throughput')
    plt.grid(True)
    plt.legend()
    
    target_path = os.path.join(figures_dir, 'test_fig.png')
    plt.savefig(target_path, bbox_inches='tight')
    print(f"Graph generated and saved to {target_path}")

if __name__ == '__main__':
    main()
