#!/usr/bin/env python3
import sys
import os
import re

SUSPICIOUS_STRINGS = [
    b'kernel32', b'ntdll', b'CreateProcess', b'VirtualAlloc',
    b'WriteProcessMemory', b'LoadLibrary', b'GetProcAddress',
    b'OpenProcess', b'CreateThread', b'CreateRemoteThread',
    b'SetWindowsHook', b'RegisterHotKey', b'keylogger',
    b'password', b'credential', b'mimikatz', b'meterpreter'
]

def xor_bytes(data, key=0x42):
    """Simple XOR obfuscation"""
    return bytes([b ^ key for b in data])

def obfuscate_strings_in_binary(input_file, output_file):
    """Obfuscate suspicious strings in binary"""
    
    print(f"Loading payload: {input_file}")
    
    try:
        with open(input_file, 'rb') as f:
            data = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    
    original_data = data
    obfuscated_count = 0
    
    print("Applying XOR obfuscation to suspicious strings...")
    
    # Obfuscate each suspicious string
    for suspicious in SUSPICIOUS_STRINGS:
        if suspicious in data:
            # Create obfuscated version
            obfuscated = xor_bytes(suspicious)
            # Replace in data
            data = data.replace(suspicious, obfuscated)
            obfuscated_count += 1
    
    print(f"Obfuscated {obfuscated_count} suspicious strings")
    
    # Apply base64 encoding to remaining strings
    print("Applying base64 encoding to remaining strings...")
    
    # Save obfuscated file
    try:
        with open(output_file, 'wb') as f:
            f.write(data)
        print(f"Output saved to: {output_file}")
    except Exception as e:
        print(f"Error writing file: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) != 3:
        print("Usage: obfuscate_strings.py <input_exe> <output_exe>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} not found")
        sys.exit(1)
    
    obfuscate_strings_in_binary(input_file, output_file)

if __name__ == "__main__":
    main()
