import random
import string
import logging
from typing import Optional, Dict
from password_history import PasswordHistory
from config_manager import ConfigManager

# Setup professional logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('password_generator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class PasswordGenerator:
    """A secure password generator with customizable options."""
    
    def __init__(self, enable_history: bool = True, history_file: str = "password_history.json", config_file: str = "config.json"):
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        # Initialize configuration management
        self.config = ConfigManager(config_file)
        
        # Initialize history management
        self.enable_history = enable_history
        self.history = PasswordHistory(history_file) if enable_history else None
        
        logger.info(f"PasswordGenerator initialized with history={'enabled' if enable_history else 'disabled'}")
    
    def generate(
        self,
        length: Optional[int] = None,
        use_uppercase: Optional[bool] = None,
        use_lowercase: Optional[bool] = None,
        use_digits: Optional[bool] = None,
        use_symbols: Optional[bool] = None,
        exclude_similar: Optional[bool] = None
    ) -> str:
        """
        Generate a secure random password.
        
        Args:
            length: Password length (None to use config default)
            use_uppercase: Include uppercase letters (None to use config default)
            use_lowercase: Include lowercase letters (None to use config default)
            use_digits: Include digits (None to use config default)
            use_symbols: Include special symbols (None to use config default)
            exclude_similar: Exclude similar characters (None to use config default)
        
        Returns:
            Generated password string
        
        Raises:
            ValueError: If no character types are selected or length is too short
        """
        # Use config values for None parameters
        if length is None:
            length = self.config.get("default_length", 12)
        if use_uppercase is None:
            use_uppercase = self.config.get("use_uppercase", True)
        if use_lowercase is None:
            use_lowercase = self.config.get("use_lowercase", True)
        if use_digits is None:
            use_digits = self.config.get("use_digits", True)
        if use_symbols is None:
            use_symbols = self.config.get("use_symbols", True)
        if exclude_similar is None:
            exclude_similar = self.config.get("exclude_similar", False)
        
        logger.info(f"Generating password with config defaults: length={length}")
        
        if length < 4:
            logger.error(f"Invalid password length requested: {length}")
            raise ValueError("Password length must be at least 4 characters")
        
        # Build character pool
        char_pool = ""
        if use_lowercase:
            char_pool += self.lowercase
        if use_uppercase:
            char_pool += self.uppercase
        if use_digits:
            char_pool += self.digits
        if use_symbols:
            char_pool += self.symbols
        
        if not char_pool:
            logger.error("No character types selected for password generation")
            raise ValueError("At least one character type must be selected")
        
        # Exclude similar characters if requested
        if exclude_similar:
            similar_chars = "il1Lo0O"
            char_pool = "".join(c for c in char_pool if c not in similar_chars)
            if not char_pool:
                raise ValueError("No characters available after excluding similar ones")
        
        # Generate password ensuring at least one character from each selected type
        password = []
        required_chars = []
        
        if use_lowercase:
            required_chars.append(random.choice(self.lowercase))
        if use_uppercase:
            required_chars.append(random.choice(self.uppercase))
        if use_digits:
            required_chars.append(random.choice(self.digits))
        if use_symbols:
            required_chars.append(random.choice(self.symbols))
        
        # Filter required chars if exclude_similar is True
        if exclude_similar:
            similar_chars = "il1Lo0O"
            required_chars = [c for c in required_chars if c not in similar_chars]
        
        password.extend(required_chars)
        
        # Fill remaining length with random characters
        remaining_length = length - len(password)
        for _ in range(remaining_length):
            password.append(random.choice(char_pool))
        
        # Shuffle to avoid predictable patterns
        random.shuffle(password)
        
        final_password = "".join(password)
        
        logger.info(f"Generated password: length={length}, strength_check_pending=True")
        
        # Log to history if enabled
        if self.enable_history and self.history:
            options = {
                "use_uppercase": use_uppercase,
                "use_lowercase": use_lowercase,
                "use_digits": use_digits,
                "use_symbols": use_symbols,
                "exclude_similar": exclude_similar
            }
            strength_result = self.check_strength(final_password)
            self.history.add_password(final_password, length, options, strength_result["strength"])
        
        return final_password
    
    def generate_multiple(
        self,
        count: int,
        length: int = 12,
        **kwargs
    ) -> list[str]:
        """
        Generate multiple passwords at once.
        
        Args:
            count: Number of passwords to generate
            length: Password length for each password
            **kwargs: Additional arguments passed to generate()
        
        Returns:
            List of generated passwords
        """
        return [self.generate(length, **kwargs) for _ in range(count)]
    
    def check_strength(self, password: str) -> dict:
        """
        Check the strength of a password.
        
        Args:
            password: Password to check
        
        Returns:
            Dictionary with strength analysis
        """
        score = 0
        feedback = []
        
        if len(password) >= 8:
            score += 1
        else:
            feedback.append("Password should be at least 8 characters")
        
        if len(password) >= 12:
            score += 1
        else:
            feedback.append("Consider using 12+ characters for better security")
        
        if any(c.islower() for c in password):
            score += 1
        else:
            feedback.append("Add lowercase letters")
        
        if any(c.isupper() for c in password):
            score += 1
        else:
            feedback.append("Add uppercase letters")
        
        if any(c.isdigit() for c in password):
            score += 1
        else:
            feedback.append("Add numbers")
        
        if any(c in self.symbols for c in password):
            score += 1
        else:
            feedback.append("Add special symbols")
        
        # Determine strength level
        if score <= 2:
            strength = "Weak"
        elif score <= 4:
            strength = "Medium"
        else:
            strength = "Strong"
        
        return {
            "password": password,
            "strength": strength,
            "score": score,
            "max_score": 6,
            "feedback": feedback
        }
    
    def get_history(self, limit: Optional[int] = None):
        """
        Get password generation history
        
        Args:
            limit: Maximum number of entries to return (None for all)
        
        Returns:
            List of history entries or None if history disabled
        """
        if self.enable_history and self.history:
            return self.history.get_history(limit)
        return None
    
    def get_recent_passwords(self, count: int = 5) -> list:
        """
        Get most recently generated passwords
        
        Args:
            count: Number of recent passwords to return
        
        Returns:
            List of password strings or empty list if history disabled
        """
        if self.enable_history and self.history:
            return self.history.get_recent_passwords(count)
        return []
    
    def get_history_statistics(self) -> Dict:
        """
        Get statistics about password generation history
        
        Returns:
            Dictionary with statistics or empty dict if history disabled
        """
        if self.enable_history and self.history:
            return self.history.get_statistics()
        return {}
    
    def clear_history(self) -> bool:
        """
        Clear password generation history
        
        Returns:
            True if successful, False if history disabled
        """
        if self.enable_history and self.history:
            self.history.clear_history()
            return True
        return False
    
    def export_history(self, export_file: str, format: str = "json") -> bool:
        """
        Export password history to a file
        
        Args:
            export_file: Path to export file
            format: Export format ('json' or 'csv')
        
        Returns:
            True if successful, False if history disabled or export fails
        """
        if self.enable_history and self.history:
            return self.history.export_history(export_file, format)
        return False
    
    def get_history_count(self) -> int:
        """
        Get total number of entries in history
        
        Returns:
            Number of history entries or 0 if history disabled
        """
        if self.enable_history and self.history:
            return self.history.get_history_count()
        return 0


if __name__ == "__main__":
    # Demo usage
    generator = PasswordGenerator()
    
    print("Password Generator Demo")
    print("=" * 30)
    
    # Generate a simple password
    password = generator.generate(length=12)
    print(f"Generated Password: {password}")
    
    # Check strength
    strength = generator.check_strength(password)
    print(f"Strength: {strength['strength']} ({strength['score']}/{strength['max_score']})")
    
    # Generate multiple passwords
    print("\nMultiple Passwords:")
    passwords = generator.generate_multiple(count=5, length=16)
    for i, pwd in enumerate(passwords, 1):
        print(f"{i}. {pwd}")
