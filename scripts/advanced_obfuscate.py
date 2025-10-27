#!/usr/bin/env python3
import sys
import os
import random
import argparse
import struct
import math

def calculate_entropy(data):
    """Calculate Shannon entropy of data"""
    if not data:
        return 0
    
    entropy = 0
    byte_counts = {}
    
    # Count byte frequencies
    for byte in data:
        if byte in byte_counts:
            byte_counts[byte] += 1
        else:
            byte_counts[byte] = 1
    
    # Calculate entropy
    data_len = len(data)
    for count in byte_counts.values():
        if count > 0:
            p_i = float(count) / data_len
            entropy -= p_i * math.log2(p_i)
    
    return entropy

def add_garbage_code(data, amount=1024):
    """Add random garbage code sections"""
    # Generate random bytes that look like code
    garbage = bytearray()
    for _ in range(amount):
        # Mix of common x86 opcodes and random data
        if random.random() > 0.5:
            # Common x86 instructions
            opcodes = [0x90, 0x50, 0x51, 0x52, 0x53, 0x58, 0x59, 0x5A, 0x5B]
            garbage.append(random.choice(opcodes))
        else:
            garbage.append(random.randint(0, 255))
    
    # Insert garbage at random positions
    insert_pos = random.randint(len(data)//2, len(data))
    return data[:insert_pos] + bytes(garbage) + data[insert_pos:]

def byte_substitution(data):
    """Apply byte substitution cipher"""
    # Create substitution table
    sub_table = list(range(256))
    random.shuffle(sub_table)
    
    # Apply substitution
    result = bytearray()
    for byte in data:
        result.append(sub_table[byte])
    
    return bytes(result)

def manipulate_entropy(data, target_entropy=7.0):
    """Adjust entropy to target level"""
    current_entropy = calculate_entropy(data)
    
    if current_entropy < target_entropy:
        # Add random bytes to increase entropy
        random_bytes = os.urandom(int(len(data) * 0.1))
        data = data + random_bytes
    
    return data

def main():
    parser = argparse.ArgumentParser(description='Advanced payload obfuscation')
    parser.add_argument('--input', required=True, help='Input file')
    parser.add_argument('--output', required=True, help='Output file')
    parser.add_argument('--method', default='all', choices=['strings', 'bytes', 'garbage', 'entropy', 'all'])
    
    args = parser.parse_args()
    
    print("[+] Loading input file...")
    with open(args.input, 'rb') as f:
        data = f.read()
    
    original_size = len(data)
    original_entropy = calculate_entropy(data)
    
    if args.method in ['strings', 'all']:
        print("[+] Applying string obfuscation...")
        # Simple string obfuscation
        data = data.replace(b'kernel32', b'k\x00e\x00r\x00n\x00e\x00l\x003\x002')
        data = data.replace(b'KERNEL32', b'K\x00E\x00R\x00N\x00E\x00L\x003\x002')
    
    if args.method in ['bytes', 'all']:
        print("[+] Applying byte substitution...")
        data = byte_substitution(data)
    
    if args.method in ['garbage', 'all']:
        print("[+] Adding garbage code sections...")
        data = add_garbage_code(data)
    
    if args.method in ['entropy', 'all']:
        print("[+] Applying entropy manipulation...")
        data = manipulate_entropy(data)
    
    new_entropy = calculate_entropy(data)
    
    print("[+] Obfuscation complete!")
    print(f"[+] Original size: {original_size} bytes")
    print(f"[+] Obfuscated size: {len(data)} bytes")
    print(f"[+] Entropy change: {original_entropy:.1f} -> {new_entropy:.1f}")
    
    with open(args.output, 'wb') as f:
        f.write(data)

if __name__ == "__main__":
    main()
