#helper class

#Attendance/utils

from datetime import datetime
import pytz 
from .logger import get_log

logger = get_log(__name__)

def current_date(timezone_str='UTC'):
    """
    Returns the current date and time for a specific timezone.
    Defaults to UTC if no timezone is provided.
    """
    try:
        # Define the timezone object
        tz = pytz.timezone(timezone_str)
        # Get the current time in that timezone
        now = datetime.now(tz)
        return now.strftime("%Y-%m-%d %H:%M:%S")
        
    except Exception as e:
        logger.exception(f"Failed to compute date for {timezone_str}")
        # Fallback to UTC date string
        return datetime.now().strftime("%Y-%m-%d")
    
    
