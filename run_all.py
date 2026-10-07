"""
Run All Password Generator Features
This script runs all demonstrations at once
"""

from password_generator import PasswordGenerator

def main():
    print("=" * 60)
    print("PASSWORD GENERATOR - COMPLETE DEMO")
    print("=" * 60)
    print()
    
    generator = PasswordGenerator()
    
    # 1. Basic Password
    print("1. Basic Password (12 chars):")
    password = generator.generate(length=12)
    print(f"   {password}")
    print()
    
    # 2. Custom Password
    print("2. Custom Password (16 chars with all options):")
    custom = generator.generate(length=16, use_uppercase=True, use_lowercase=True, 
                                use_digits=True, use_symbols=True)
    print(f"   {custom}")
    print()
    
    # 3. Without Symbols
    print("3. Without Symbols (14 chars):")
    no_symbols = generator.generate(length=14, use_symbols=False)
    print(f"   {no_symbols}")
    print()
    
    # 4. Multiple Passwords
    print("4. Multiple Passwords (5 passwords, 12 chars each):")
    passwords = generator.generate_multiple(count=5, length=12)
    for i, pwd in enumerate(passwords, 1):
        print(f"   {i}. {pwd}")
    print()
    
    # 5. Strength Check
    print("5. Password Strength Check:")
    test_passwords = ["weak", "password123", "MyP@ssw0rd", custom]
    for pwd in test_passwords:
        result = generator.check_strength(pwd)
        print(f"   {pwd:20s} - {result['strength']:8s} ({result['score']}/6)")
    print()
    
    # 6. Different Lengths
    print("6. Different Password Lengths:")
    for length in [8, 12, 16, 20]:
        pwd = generator.generate(length=length)
        print(f"   {length:2d} chars: {pwd}")
    print()
    
    print("=" * 60)
    print("Demo completed! Try CLI tool: python cli.py --help")
    print("=" * 60)

if __name__ == "__main__":
    main()
