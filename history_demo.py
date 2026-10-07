"""
Password History Feature Demonstration
This script shows how to use the password history management system
"""

from password_generator import PasswordGenerator


def demo_basic_history():
    """Basic history tracking demonstration"""
    print("=" * 60)
    print("Demo 1: Basic History Tracking")
    print("=" * 60)
    
    # Create generator with history enabled (default)
    generator = PasswordGenerator()
    
    # Generate some passwords
    print("Generating passwords...")
    for i in range(3):
        password = generator.generate(length=12)
        print(f"  {i+1}. {password}")
    
    # View history
    print("\nPassword History:")
    history = generator.get_history(limit=5)
    for i, entry in enumerate(history, 1):
        timestamp = entry['timestamp'][:19]  # Show date-time only
        print(f"  {i}. {timestamp} - {entry['password'][:10]}...")
    print()


def demo_history_statistics():
    """History statistics demonstration"""
    print("=" * 60)
    print("Demo 2: History Statistics")
    print("=" * 60)
    
    generator = PasswordGenerator()
    
    # Generate various passwords
    print("Generating passwords with different settings...")
    generator.generate(length=8, use_symbols=False)
    generator.generate(length=12)
    generator.generate(length=16, use_symbols=False)
    generator.generate(length=20)
    generator.generate(length=12, exclude_similar=True)
    
    # Get statistics
    stats = generator.get_history_statistics()
    print("\nGeneration Statistics:")
    print(f"  Total Generated: {stats['total_generated']}")
    print(f"  Average Length: {stats['average_length']}")
    print(f"  Most Common Length: {stats['most_common_length']}")
    print(f"  Strength Distribution:")
    for strength, count in stats['strength_distribution'].items():
        print(f"    {strength}: {count}")
    print()


def demo_recent_passwords():
    """Recent passwords retrieval demonstration"""
    print("=" * 60)
    print("Demo 3: Recent Passwords")
    print("=" * 60)
    
    generator = PasswordGenerator()
    
    # Generate some passwords
    print("Generating passwords...")
    for i in range(5):
        password = generator.generate(length=14)
        print(f"  {i+1}. {password}")
    
    # Get recent passwords
    print("\nLast 3 Recent Passwords:")
    recent = generator.get_recent_passwords(count=3)
    for i, password in enumerate(recent, 1):
        print(f"  {i}. {password}")
    print()


def demo_export_history():
    """History export demonstration"""
    print("=" * 60)
    print("Demo 4: Export History")
    print("=" * 60)
    
    generator = PasswordGenerator()
    
    # Generate some passwords
    print("Generating passwords for export...")
    for i in range(3):
        password = generator.generate(length=12)
        print(f"  {i+1}. {password}")
    
    # Export to JSON
    json_success = generator.export_history("demo_history.json", "json")
    if json_success:
        print("[OK] History exported to demo_history.json")
    
    # Export to CSV
    csv_success = generator.export_history("demo_history.csv", "csv")
    if csv_success:
        print("[OK] History exported to demo_history.csv")
    
    print()


def demo_clear_history():
    """History clearing demonstration"""
    print("=" * 60)
    print("Demo 5: Clear History")
    print("=" * 60)
    
    generator = PasswordGenerator()
    
    # Generate some passwords
    print("Generating passwords...")
    for i in range(3):
        password = generator.generate(length=12)
        print(f"  {i+1}. {password}")
    
    # Check history count
    print(f"\nHistory entries before clear: {generator.get_history_count()}")
    
    # Clear history
    success = generator.clear_history()
    if success:
        print("[OK] History cleared successfully")
        print(f"History entries after clear: {generator.get_history_count()}")
    print()


def demo_no_history_mode():
    """Demonstration of disabling history"""
    print("=" * 60)
    print("Demo 6: Disable History Mode")
    print("=" * 60)
    
    # Create generator with history disabled
    generator = PasswordGenerator(enable_history=False)
    
    print("Generating passwords with history disabled...")
    for i in range(3):
        password = generator.generate(length=12)
        print(f"  {i+1}. {password}")
    
    # Try to get history
    history = generator.get_history()
    if history is None:
        print("[OK] History is disabled - no tracking")
    else:
        print("[ERROR] History should be disabled")
    print()


def main():
    """Run all history demonstrations"""
    print("\n" + "=" * 60)
    print("PASSWORD HISTORY FEATURE DEMONSTRATIONS")
    print("=" * 60 + "\n")
    
    demo_basic_history()
    demo_history_statistics()
    demo_recent_passwords()
    demo_export_history()
    demo_clear_history()
    demo_no_history_mode()
    
    print("=" * 60)
    print("All history demonstrations completed!")
    print("Check the generated files: demo_history.json, demo_history.csv")
    print("=" * 60)


if __name__ == "__main__":
    main()
