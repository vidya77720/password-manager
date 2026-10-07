"""
New Features Demonstration
Shows the three new features: Professional Logging, Configuration Management, and GUI
"""

from password_generator import PasswordGenerator
from config_manager import ConfigManager


def demo_logging():
    """Demonstrate professional logging system"""
    print("=" * 60)
    print("Demo 1: Professional Logging System")
    print("=" * 60)
    
    print("Generating passwords with logging enabled...")
    print("Check 'password_generator.log' file for detailed logs")
    print()
    
    generator = PasswordGenerator()
    
    # Generate some passwords to trigger logging
    for i in range(3):
        password = generator.generate(length=12)
        print(f"  {i+1}. {password}")
    
    print("\n[OK] Logging is working. Check password_generator.log for details")
    print()


def demo_configuration():
    """Demonstrate configuration management"""
    print("=" * 60)
    print("Demo 2: Configuration Management System")
    print("=" * 60)
    
    config = ConfigManager()
    
    print("Current Configuration:")
    for key, value in config.get_all().items():
        print(f"  {key}: {value}")
    
    print("\nChanging default_length to 16...")
    config.set("default_length", 16)
    
    print("Validating configuration...")
    is_valid = config.validate_config()
    print(f"Configuration valid: {is_valid}")
    
    print("\nExporting configuration...")
    config.export_config("demo_config.json")
    print("[OK] Configuration exported to demo_config.json")
    
    print("\nResetting to defaults...")
    config.reset_to_defaults()
    print("[OK] Configuration reset to defaults")
    print()


def demo_config_integration():
    """Demonstrate configuration integration with password generator"""
    print("=" * 60)
    print("Demo 3: Configuration Integration")
    print("=" * 60)
    
    config = ConfigManager()
    
    # Set custom configuration
    print("Setting custom configuration...")
    config.set("default_length", 16)
    config.set("use_symbols", False)
    
    # Create generator with config
    generator = PasswordGenerator()
    
    print("Generating password with config defaults (None parameters)...")
    password = generator.generate()  # Will use config defaults
    print(f"Generated: {password}")
    print(f"Length: {len(password)} (should be 16 from config)")
    
    # Reset config
    config.reset_to_defaults()
    print("[OK] Configuration integration working")
    print()


def main():
    """Run all new feature demonstrations"""
    print("\n" + "=" * 60)
    print("NEW FEATURES DEMONSTRATION")
    print("=" * 60 + "\n")
    
    demo_logging()
    demo_configuration()
    demo_config_integration()
    
    print("=" * 60)
    print("New Features Demo Completed!")
    print("=" * 60)
    print("\nTo run the GUI application:")
    print("  python gui_app.py")
    print("\nCheck these files:")
    print("  - password_generator.log (logging output)")
    print("  - config.json (configuration file)")
    print("  - demo_config.json (exported configuration)")
    print("=" * 60)


if __name__ == "__main__":
    main()

