#!/usr/bin/env python3
"""
Command Line Interface for Password Generator
"""
import argparse
import sys
import logging
from password_generator import PasswordGenerator

# Setup CLI-specific logging
cli_logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Generate secure random passwords",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                          # Generate a 12-character password
  %(prog)s -l 16                    # Generate a 16-character password
  %(prog)s -l 20 --no-symbols       # Generate without special symbols
  %(prog)s -c 5 -l 14               # Generate 5 passwords, 14 chars each
  %(prog)s --exclude-similar        # Exclude similar characters (i, l, 1, L, o, 0, O)
  %(prog)s --check "MyP@ssw0rd"     # Check password strength
  %(prog)s --history                # Show password generation history
  %(prog)s --history-stats          # Show generation statistics
  %(prog)s --export-history backup.json  # Export history to file
  %(prog)s --clear-history          # Clear all password history
        """
    )
    
    parser.add_argument(
        "-l", "--length",
        type=int,
        default=12,
        help="Password length (default: 12, minimum: 4)"
    )
    
    parser.add_argument(
        "-c", "--count",
        type=int,
        default=1,
        help="Number of passwords to generate (default: 1)"
    )
    
    parser.add_argument(
        "--no-uppercase",
        action="store_true",
        help="Exclude uppercase letters"
    )
    
    parser.add_argument(
        "--no-lowercase",
        action="store_true",
        help="Exclude lowercase letters"
    )
    
    parser.add_argument(
        "--no-digits",
        action="store_true",
        help="Exclude digits"
    )
    
    parser.add_argument(
        "--no-symbols",
        action="store_true",
        help="Exclude special symbols"
    )
    
    parser.add_argument(
        "--exclude-similar",
        action="store_true",
        help="Exclude similar characters (i, l, 1, L, o, 0, O)"
    )
    
    parser.add_argument(
        "--check",
        type=str,
        metavar="PASSWORD",
        help="Check strength of an existing password"
    )
    
    # History management arguments
    parser.add_argument(
        "--history",
        action="store_true",
        help="Show password generation history"
    )
    
    parser.add_argument(
        "--history-limit",
        type=int,
        default=10,
        metavar="N",
        help="Limit history entries to show (default: 10)"
    )
    
    parser.add_argument(
        "--history-stats",
        action="store_true",
        help="Show password generation statistics"
    )
    
    parser.add_argument(
        "--clear-history",
        action="store_true",
        help="Clear all password history"
    )
    
    parser.add_argument(
        "--export-history",
        type=str,
        metavar="FILE",
        help="Export history to file (JSON or CSV)"
    )
    
    parser.add_argument(
        "--no-history",
        action="store_true",
        help="Disable history logging for this session"
    )
    
    args = parser.parse_args()
    
    # Initialize generator with history enabled/disabled
    generator = PasswordGenerator(enable_history=not args.no_history)
    cli_logger.info(f"CLI started with history={'enabled' if not args.no_history else 'disabled'}")
    
    # Check password strength mode
    if args.check:
        result = generator.check_strength(args.check)
        print(f"Password: {result['password']}")
        print(f"Strength: {result['strength']} ({result['score']}/{result['max_score']})")
        if result['feedback']:
            print("\nSuggestions:")
            for suggestion in result['feedback']:
                print(f"  - {suggestion}")
        return
    
    # History management modes
    if args.clear_history:
        if generator.clear_history():
            print("Password history cleared successfully.")
        else:
            print("History is disabled or could not be cleared.")
        return
    
    if args.history_stats:
        stats = generator.get_history_statistics()
        if stats:
            print("Password Generation Statistics:")
            print(f"  Total Generated: {stats['total_generated']}")
            print(f"  Average Length: {stats['average_length']}")
            print(f"  Most Common Length: {stats['most_common_length']}")
            print(f"  Strength Distribution:")
            for strength, count in stats['strength_distribution'].items():
                print(f"    {strength}: {count}")
        else:
            print("History is disabled or no data available.")
        return
    
    if args.export_history:
        # Determine format from file extension
        if args.export_history.endswith('.csv'):
            format_type = 'csv'
        else:
            format_type = 'json'
        
        if generator.export_history(args.export_history, format_type):
            print(f"History exported to {args.export_history} ({format_type.upper()})")
        else:
            print("Failed to export history. History may be disabled.")
        return
    
    if args.history:
        history = generator.get_history(limit=args.history_limit)
        if history:
            print(f"Password History (showing last {len(history)} entries):")
            print("=" * 60)
            for i, entry in enumerate(history, 1):
                timestamp = entry['timestamp'][:19]  # Show only date-time part
                password_masked = entry['password'][:4] + "*" * (len(entry['password']) - 4)
                print(f"{i}. {timestamp}")
                print(f"   Password: {password_masked}")
                print(f"   Length: {entry['length']}, Strength: {entry.get('strength', 'N/A')}")
                print()
        else:
            print("History is disabled or no passwords generated yet.")
        return
    
    # Generate passwords
    try:
        cli_logger.info(f"Generating {args.count} password(s) with length={args.length}")
        passwords = generator.generate_multiple(
            count=args.count,
            length=args.length,
            use_uppercase=not args.no_uppercase,
            use_lowercase=not args.no_lowercase,
            use_digits=not args.no_digits,
            use_symbols=not args.no_symbols,
            exclude_similar=args.exclude_similar
        )
        cli_logger.info(f"Successfully generated {args.count} password(s)")
        
        if args.count == 1:
            print(passwords[0])
        else:
            for i, password in enumerate(passwords, 1):
                print(f"{i}. {password}")
                
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
