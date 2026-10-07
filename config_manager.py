"""
Configuration Management System
Manages user preferences and default settings for password generator
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class ConfigManager:
    """Manages configuration settings for password generator"""
    
    DEFAULT_CONFIG = {
        "default_length": 12,
        "use_uppercase": True,
        "use_lowercase": True,
        "use_digits": True,
        "use_symbols": True,
        "exclude_similar": False,
        "enable_history": True,
        "history_file": "password_history.json",
        "log_file": "password_generator.log",
        "log_level": "INFO"
    }
    
    def __init__(self, config_file: str = "config.json"):
        """
        Initialize configuration manager
        
        Args:
            config_file: Path to configuration file (default: config.json)
        """
        self.config_file = Path(config_file)
        self.config: Dict[str, Any] = {}
        self._load_config()
    
    def _load_config(self) -> None:
        """Load configuration from file or create default"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                # Merge with defaults (user config overrides defaults)
                self.config = {**self.DEFAULT_CONFIG, **user_config}
                logger.info(f"Configuration loaded from {self.config_file}")
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"Could not load config file. Using defaults. Error: {e}")
                self.config = self.DEFAULT_CONFIG.copy()
        else:
            logger.info(f"Config file {self.config_file} not found. Creating with defaults.")
            self.config = self.DEFAULT_CONFIG.copy()
            self._save_config()
    
    def _save_config(self) -> None:
        """Save current configuration to file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            logger.info(f"Configuration saved to {self.config_file}")
        except IOError as e:
            logger.error(f"Could not save config file. Error: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value
        
        Args:
            key: Configuration key
            default: Default value if key not found
        
        Returns:
            Configuration value or default
        """
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value
        
        Args:
            key: Configuration key
            value: Value to set
        """
        self.config[key] = value
        self._save_config()
        logger.info(f"Configuration updated: {key} = {value}")
    
    def get_all(self) -> Dict[str, Any]:
        """Get all configuration values"""
        return self.config.copy()
    
    def reset_to_defaults(self) -> None:
        """Reset all configuration to default values"""
        self.config = self.DEFAULT_CONFIG.copy()
        self._save_config()
        logger.info("Configuration reset to defaults")
    
    def validate_config(self) -> bool:
        """
        Validate current configuration
        
        Returns:
            True if configuration is valid, False otherwise
        """
        try:
            # Validate numeric values
            if self.config.get("default_length", 0) < 4:
                logger.error("Invalid default_length: must be >= 4")
                return False
            
            # Validate boolean values
            bool_keys = ["use_uppercase", "use_lowercase", "use_digits", 
                        "use_symbols", "exclude_similar", "enable_history"]
            for key in bool_keys:
                if key in self.config and not isinstance(self.config[key], bool):
                    logger.error(f"Invalid {key}: must be boolean")
                    return False
            
            # Validate log level
            valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
            if self.config.get("log_level") not in valid_log_levels:
                logger.error(f"Invalid log_level: must be one of {valid_log_levels}")
                return False
            
            logger.info("Configuration validation passed")
            return True
            
        except Exception as e:
            logger.error(f"Configuration validation failed: {e}")
            return False
    
    def export_config(self, export_file: str) -> bool:
        """
        Export current configuration to a file
        
        Args:
            export_file: Path to export file
        
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(export_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            logger.info(f"Configuration exported to {export_file}")
            return True
        except IOError as e:
            logger.error(f"Could not export configuration. Error: {e}")
            return False
    
    def import_config(self, import_file: str) -> bool:
        """
        Import configuration from a file
        
        Args:
            import_file: Path to import file
        
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(import_file, 'r', encoding='utf-8') as f:
                imported_config = json.load(f)
            
            # Validate imported config
            self.config = {**self.DEFAULT_CONFIG, **imported_config}
            if self.validate_config():
                self._save_config()
                logger.info(f"Configuration imported from {import_file}")
                return True
            else:
                logger.error("Imported configuration validation failed")
                return False
                
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Could not import configuration. Error: {e}")
            return False


if __name__ == "__main__":
    # Demo usage
    config = ConfigManager()
    
    print("Configuration Manager Demo")
    print("=" * 40)
    
    # Get current config
    print("Current Configuration:")
    for key, value in config.get_all().items():
        print(f"  {key}: {value}")
    
    # Test setting a value
    print("\nSetting default_length to 16...")
    config.set("default_length", 16)
    
    # Validate config
    print("Validating configuration...")
    is_valid = config.validate_config()
    print(f"Configuration valid: {is_valid}")
    
    # Export config
    print("\nExporting configuration...")
    config.export_config("demo_config.json")
    print("Configuration exported to demo_config.json")