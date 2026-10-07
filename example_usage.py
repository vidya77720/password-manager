"""
Example Usage Demonstrations for Password Generator
This script shows various ways to use the PasswordGenerator class
"""

from password_generator import PasswordGenerator


def example_basic_usage():
    """Basic password generation example"""
    print("=" * 50)
    print("Example 1: Basic Usage")
    print("=" * 50)
    
    generator = PasswordGenerator()
    password = generator.generate(length=12)
    print(f"Generated Password: {password}")
    print()


def example_custom_options():
    """Example with custom options"""
    print("=" * 50)
    print("Example 2: Custom Options")
    print("=" * 50)
    
    generator = PasswordGenerator()
    
    # Generate with specific options
    password = generator.generate(
        length=16,
        use_uppercase=True,
        use_lowercase=True,
        use_digits=True,
        use_symbols=True
    )
    print(f"16-character password: {password}")
    
    # Generate without symbols
    password_no_symbols = generator.generate(
        length=14,
        use_symbols=False
    )
    print(f"Without symbols: {password_no_symbols}")
    
    # Generate with only letters and numbers
    password_alphanumeric = generator.generate(
        length=12,
        use_symbols=False
    )
    print(f"Alphanumeric only: {password_alphanumeric}")
    print()


def example_exclude_similar():
    """Example excluding similar characters"""
    print("=" * 50)
    print("Example 3: Exclude Similar Characters")
    print("=" * 50)
    
    generator = PasswordGenerator()
    
    # Normal password
    normal = generator.generate(length=12, exclude_similar=False)
    print(f"Normal: {normal}")
    
    # Excluding similar characters (i, l, 1, L, o, 0, O)
    clean = generator.generate(length=12, exclude_similar=True)
    print(f"Without similar chars: {clean}")
    print()


def example_multiple_passwords():
    """Example generating multiple passwords"""
    print("=" * 50)
    print("Example 4: Generate Multiple Passwords")
    print("=" * 50)
    
    generator = PasswordGenerator()
    
    # Generate 5 passwords
    passwords = generator.generate_multiple(count=5, length=14)
    print("5 passwords with 14 characters each:")
    for i, password in enumerate(passwords, 1):
        print(f"{i}. {password}")
    print()


def example_strength_checker():
    """Example password strength checker"""
    print("=" * 50)
    print("Example 5: Password Strength Checker")
    print("=" * 50)
    
    generator = PasswordGenerator()
    
    # Test different passwords
    test_passwords = [
        "weak",
        "password123",
        "MyP@ssw0rd",
        generator.generate(length=12),
        generator.generate(length=20)
    ]
    
    for pwd in test_passwords:
        result = generator.check_strength(pwd)
        print(f"Password: {pwd}")
        print(f"Strength: {result['strength']} ({result['score']}/{result['max_score']})")
        if result['feedback']:
            print("Suggestions:")
            for suggestion in result['feedback']:
                print(f"  - {suggestion}")
        print()


def example_different_lengths():
    """Example with different password lengths"""
    print("=" * 50)
    print("Example 6: Different Password Lengths")
    print("=" * 50)
    
    generator = PasswordGenerator()
    
    lengths = [8, 12, 16, 20, 24]
    print("Passwords of different lengths:")
    for length in lengths:
        password = generator.generate(length=length)
        print(f"{length} chars: {password}")
    print()


def example_character_combinations():
    """Example with different character combinations"""
    print("=" * 50)
    print("Example 7: Character Combinations")
    print("=" * 50)
    
    generator = PasswordGenerator()
    
    combinations = [
        ("Lowercase only", {"use_uppercase": False, "use_digits": False, "use_symbols": False}),
        ("Uppercase only", {"use_lowercase": False, "use_digits": False, "use_symbols": False}),
        ("Letters only", {"use_digits": False, "use_symbols": False}),
        ("Letters + Digits", {"use_symbols": False}),
        ("All characters", {})
    ]
    
    for name, options in combinations:
        password = generator.generate(length=12, **options)
        print(f"{name:20s}: {password}")
    print()


def main():
    """Run all examples"""
    print("\n" + "=" * 50)
    print("PASSWORD GENERATOR - USAGE EXAMPLES")
    print("=" * 50 + "\n")
    
    example_basic_usage()
    example_custom_options()
    example_exclude_similar()
    example_multiple_passwords()
    example_strength_checker()
    example_different_lengths()
    example_character_combinations()
    
    print("=" * 50)
    print("All examples completed!")
    print("=" * 50)


if __name__ == "__main__":
    main()
