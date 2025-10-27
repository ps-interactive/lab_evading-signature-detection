#!/usr/bin/env python3
import sys
import os
import math
from collections import Counter

def calculate_entropy(filepath):
    """Calculate Shannon entropy of a file"""
    with open(filepath, 'rb') as f:
        data = f.read()
    
    if not data:
        return 0
    
    # Count byte frequencies
    frequencies = Counter(data)
    
    # Calculate entropy
    entropy = 0
    data_len = len(data)
    
    for count in frequencies.values():
        if count > 0:
            probability = float(count) / data_len
            entropy -= probability * math.log2(probability)
    
    return entropy

def main():
    if len(sys.argv) != 2:
        print("Usage: check_entropy.py <directory_or_file>")
        sys.exit(1)
    
    path = sys.argv[1]
    
    if os.path.isfile(path):
        entropy = calculate_entropy(path)
        print(f"File: {os.path.basename(path)} - Entropy: {entropy:.1f}")
    elif os.path.isdir(path):
        for filename in os.listdir(path):
            if filename.endswith('.exe'):
                filepath = os.path.join(path, filename)
                try:
                    entropy = calculate_entropy(filepath)
                    print(f"File: {filename} - Entropy: {entropy:.1f}")
                except Exception as e:
                    print(f"Error processing {filename}: {e}")
    else:
        print(f"Error: {path} is not a valid file or directory")
        sys.exit(1)

if __name__ == "__main__":
    main()
