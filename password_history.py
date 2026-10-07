"""
Password History Management System
Logs generated passwords with timestamps and provides history management
"""

import json
import os
import logging
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class PasswordHistory:
    """Manages password generation history with file-based persistence"""
    
    def __init__(self, history_file: str = "password_history.json"):
        """
        Initialize PasswordHistory manager
        
        Args:
            history_file: Path to the history JSON file (default: password_history.json)
        """
        self.history_file = Path(history_file)
        self.history: List[Dict] = []
        self._load_history()
    
    def _load_history(self) -> None:
        """Load history from file if it exists"""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
                logger.info(f"Loaded {len(self.history)} history entries from {self.history_file}")
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"Could not load history file. Starting fresh. Error: {e}")
                self.history = []
        else:
            logger.info(f"History file {self.history_file} does not exist. Starting fresh.")
            self.history = []
    
    def _save_history(self) -> None:
        """Save history to file"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Error: Could not save history file. Error: {e}")
    
    def add_password(
        self,
        password: str,
        length: int,
        options: Dict,
        strength: Optional[str] = None
    ) -> None:
        """
        Add a password to history
        
        Args:
            password: The generated password
            length: Password length
            options: Dictionary of generation options
            strength: Optional strength rating
        """
        entry = {
            "password": password,
            "timestamp": datetime.now().isoformat(),
            "length": length,
            "options": options,
            "strength": strength
        }
        
        self.history.append(entry)
        self._save_history()
        logger.info(f"Password added to history: length={length}, strength={strength}")
    
    def get_history(self, limit: Optional[int] = None) -> List[Dict]:
        """
        Get password history
        
        Args:
            limit: Maximum number of entries to return (None for all)
        
        Returns:
            List of history entries
        """
        if limit is None:
            return self.history.copy()
        return self.history[-limit:]
    
    def get_recent_passwords(self, count: int = 5) -> List[str]:
        """
        Get most recently generated passwords
        
        Args:
            count: Number of recent passwords to return
        
        Returns:
            List of password strings
        """
        recent = self.get_history(limit=count)
        return [entry["password"] for entry in recent]
    
    def search_history(self, pattern: str) -> List[Dict]:
        """
        Search history by password pattern
        
        Args:
            pattern: Pattern to search for in passwords
        
        Returns:
            List of matching history entries
        """
        return [
            entry for entry in self.history
            if pattern.lower() in entry["password"].lower()
        ]
    
    def get_statistics(self) -> Dict:
        """
        Get statistics about password generation
        
        Returns:
            Dictionary with generation statistics
        """
        if not self.history:
            return {
                "total_generated": 0,
                "average_length": 0,
                "most_common_length": 0,
                "strength_distribution": {}
            }
        
        total = len(self.history)
        lengths = [entry["length"] for entry in self.history]
        avg_length = sum(lengths) / total
        
        # Find most common length
        from collections import Counter
        length_counts = Counter(lengths)
        most_common_length = length_counts.most_common(1)[0][0]
        
        # Strength distribution
        strength_dist = {}
        for entry in self.history:
            strength = entry.get("strength", "Unknown")
            strength_dist[strength] = strength_dist.get(strength, 0) + 1
        
        return {
            "total_generated": total,
            "average_length": round(avg_length, 1),
            "most_common_length": most_common_length,
            "strength_distribution": strength_dist
        }
    
    def clear_history(self) -> None:
        """Clear all password history"""
        count = len(self.history)
        self.history = []
        self._save_history()
        logger.info(f"Cleared {count} history entries")
    
    def export_history(self, export_file: str, format: str = "json") -> bool:
        """
        Export history to a file
        
        Args:
            export_file: Path to export file
            format: Export format ('json' or 'csv')
        
        Returns:
            True if export successful, False otherwise
        """
        try:
            if format.lower() == "json":
                with open(export_file, 'w', encoding='utf-8') as f:
                    json.dump(self.history, f, indent=2, ensure_ascii=False)
            elif format.lower() == "csv":
                import csv
                with open(export_file, 'w', newline='', encoding='utf-8') as f:
                    if self.history:
                        writer = csv.DictWriter(f, fieldnames=self.history[0].keys())
                        writer.writeheader()
                        writer.writerows(self.history)
            else:
                return False
            return True
        except (IOError, ImportError) as e:
            print(f"Error: Could not export history. Error: {e}")
            return False
    
    def delete_entry(self, index: int) -> bool:
        """
        Delete a specific history entry by index
        
        Args:
            index: Index of entry to delete
        
        Returns:
            True if deletion successful, False otherwise
        """
        try:
            if 0 <= index < len(self.history):
                del self.history[index]
                self._save_history()
                return True
            return False
        except Exception:
            return False
    
    def get_history_count(self) -> int:
        """Get total number of entries in history"""
        return len(self.history)


if __name__ == "__main__":
    # Demo usage
    history = PasswordHistory()
    
    print("Password History Demo")
    print("=" * 40)
    
    # Add some sample entries
    history.add_password("Test123!@#", 12, {"use_symbols": True}, "Strong")
    history.add_password("Another456$", 11, {"use_symbols": True}, "Medium")
    
    # Get history
    print("Recent History:")
    for entry in history.get_history(limit=5):
        print(f"  {entry['password'][:20]}... - {entry['timestamp']}")
    
    # Get statistics
    stats = history.get_statistics()
    print(f"\nStatistics:")
    print(f"  Total Generated: {stats['total_generated']}")
    print(f"  Average Length: {stats['average_length']}")
