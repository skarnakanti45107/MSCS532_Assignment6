import random
import time

# ==========================================
# 1. Randomized Selection (Expected O(n))
# ==========================================
def randomized_select(arr, k):
    """
    Finds the k-th smallest element in an array using Randomized Quickselect.
    k is 1-indexed (e.g., k=1 is the minimum element).
    """
    if not arr:
        return None
    
    # Choose a random pivot to ensure expected linear time
    pivot = random.choice(arr)
    
    # Three-way partition to handle duplicates efficiently
    lows = [el for el in arr if el < pivot]
    pivots = [el for el in arr if el == pivot]
    highs = [el for el in arr if el > pivot]
    
    # Check which partition the k-th element falls into
    if k <= len(lows):
        return randomized_select(lows, k)
    elif k <= len(lows) + len(pivots):
        return pivot
    else:
        return randomized_select(highs, k - len(lows) - len(pivots))

# ==========================================
# 2. Deterministic Selection (Worst-case O(n))
# ==========================================
def deterministic_select(arr, k):
    """
    Finds the k-th smallest element in an array using the Median of Medians algorithm.
    k is 1-indexed.
    """
    if not arr:
        return None
    
    # Divide the array into chunks of 5 elements
    chunks = [arr[i:i+5] for i in range(0, len(arr), 5)]
    
    # Find the median of each chunk (sorting chunks of max size 5 is O(1))
    medians = [sorted(chunk)[len(chunk) // 2] for chunk in chunks]
    
    # Find the median of the medians array to use as our pivot
    if len(medians) <= 5:
        pivot = sorted(medians)[len(medians) // 2]
    else:
        # Recursively call deterministic_select to find the exact median of medians
        pivot = deterministic_select(medians, len(medians) // 2 + 1)
        
    # Three-way partition to handle duplicates efficiently
    lows = [el for el in arr if el < pivot]
    pivots = [el for el in arr if el == pivot]
    highs = [el for el in arr if el > pivot]
    
    # Check which partition the k-th element falls into
    if k <= len(lows):
        return deterministic_select(lows, k)
    elif k <= len(lows) + len(pivots):
        return pivot
    else:
        return deterministic_select(highs, k - len(lows) - len(pivots))

# ==========================================
# 3. Empirical Performance Testing
# ==========================================
def run_empirical_analysis():
    """
    Tests both algorithms against different sizes and distributions 
    to gather data for the performance analysis report.
    """
    sizes = [1000, 5000, 10000]
    distributions = ['random', 'sorted', 'reverse_sorted', 'duplicates']
    
    print(f"{'Size':<8} | {'Distribution':<15} | {'Algorithm':<22} | {'Time (Seconds)'}")
    print("-" * 65)
    
    for size in sizes:
        for dist in distributions:
            # Generate the datasets based on the distribution type
            if dist == 'random':
                arr = [random.randint(0, 100000) for _ in range(size)]
            elif dist == 'sorted':
                arr = list(range(size))
            elif dist == 'reverse_sorted':
                arr = list(range(size, 0, -1))
            elif dist == 'duplicates':
                arr = [random.choice([1, 2, 3, 4, 5]) for _ in range(size)]
                
            k = size // 2 # Searching for the median
            
            # Test Randomized Quickselect
            start_time = time.perf_counter()
            randomized_select(arr, k)
            rand_time = time.perf_counter() - start_time
            
            # Test Median of Medians
            start_time = time.perf_counter()
            deterministic_select(arr, k)
            det_time = time.perf_counter() - start_time
            
            print(f"{size:<8} | {dist:<15} | {'Randomized':<22} | {rand_time:.6f}")
            print(f"{size:<8} | {dist:<15} | {'Deterministic':<22} | {det_time:.6f}")
        print("-" * 65)

if __name__ == "__main__":
    # Run a quick functional test
    test_arr = [12, 3, 5, 7, 4, 19, 26, 7, 7, 7, 7]
    k_val = 5
    print(f"Array: {test_arr}")
    print(f"Finding k={k_val} (1-indexed) smallest element...\n")
    
    print(f"Randomized Result: {randomized_select(test_arr, k_val)}")
    print(f"Deterministic Result: {deterministic_select(test_arr, k_val)}\n")
    
    print("Starting Empirical Analysis Harness...\n")
    run_empirical_analysis()