import random
import string
from datetime import datetime


class OPFUN:
    def __init__(self, prefix="STAY"):
        """
        Initialize with an optional prefix
        Example: STAY1234
        """
        self.prefix = prefix.upper()

    def generate_custom_id(self, length=6, include_date=False):
        """
        Generate a custom ID with optional date inclusion.
        Parameters:
        - length (int): Number of random characters.
        - include_date (bool): If True, prepend current date (YYYYMMDD) to ID.
        Returns:
        - str: Generated custom ID.
        """
        chars = string.ascii_uppercase + string.digits
        random_part = ''.join(random.choice(chars) for _ in range(length))

        if include_date:
            date_part = datetime.now().strftime("%Y%m%d")
            return f"{self.prefix}{date_part}{random_part}"
        else:
            return f"{self.prefix}{random_part}"
