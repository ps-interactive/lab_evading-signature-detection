#!/usr/bin/env python3
import sys
import re
import argparse

def extract_strings(filepath, min_length=4):
    """Extract ASCII strings from binary file"""
    strings = []
    pattern = re.compile(b'[\x20-\x7E]{%d,}' % min_length)
    
    try:
        with open(filepath, 'rb') as f:
            data = f.read()
            matches = pattern.findall(data)
            strings = [s.decode('ascii', errors='ignore') for s in matches]
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    
    return strings

def main():
    if len(sys.argv) != 3:
        print("Usage: extract_strings.py <input_file> <output_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    print(f"Extracting strings from: {input_file}")
    strings = extract_strings(input_file)
    
    # Remove duplicates
    unique_strings = list(set(strings))
    print(f"Found {len(unique_strings)} unique strings")
    
    # Save to file
    with open(output_file, 'w') as f:
        for string in unique_strings:
            f.write(string + '\n')
    
    print(f"Strings saved to: {output_file}")

if __name__ == "__main__":
    main()
