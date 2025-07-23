"""
State Validation Utility - Validates US state names and abbreviations
"""

# US State abbreviations and full names mapping
US_STATES = {
    # Standard state abbreviations
    'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California',
    'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia',
    'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa',
    'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
    'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri',
    'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey',
    'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio',
    'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
    'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont',
    'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming',
    
    # US Territories and Districts
    'DC': 'District of Columbia', 'PR': 'Puerto Rico', 'VI': 'US Virgin Islands',
    'AS': 'American Samoa', 'GU': 'Guam', 'MP': 'Northern Mariana Islands'
}

# Create reverse mapping for full names
FULL_NAME_TO_ABBREV = {full_name.upper(): abbrev for abbrev, full_name in US_STATES.items()}

# Common state name variations and misspellings
STATE_ALIASES = {
    'CALIF': 'CA', 'CALI': 'CA', 'CALIFORNIA': 'CA',
    'TEXAS': 'TX', 'TEX': 'TX',
    'FLORIDA': 'FL', 'FLA': 'FL',
    'NEW YORK': 'NY', 'NEWYORK': 'NY', 'NY STATE': 'NY',
    'PENNSYLVANIA': 'PA', 'PENN': 'PA',
    'MASSACHUSETTS': 'MA', 'MASS': 'MA',
    'NORTH CAROLINA': 'NC', 'N CAROLINA': 'NC', 'N.C.': 'NC',
    'SOUTH CAROLINA': 'SC', 'S CAROLINA': 'SC', 'S.C.': 'SC',
    'NEW JERSEY': 'NJ', 'N JERSEY': 'NJ', 'N.J.': 'NJ',
    'NEW HAMPSHIRE': 'NH', 'N HAMPSHIRE': 'NH', 'N.H.': 'NH',
    'NEW MEXICO': 'NM', 'N MEXICO': 'NM', 'N.M.': 'NM',
    'WEST VIRGINIA': 'WV', 'W VIRGINIA': 'WV', 'W.V.': 'WV',
    'NORTH DAKOTA': 'ND', 'N DAKOTA': 'ND', 'N.D.': 'ND',
    'SOUTH DAKOTA': 'SD', 'S DAKOTA': 'SD', 'S.D.': 'SD',
    'WASHINGTON': 'WA', 'WASH': 'WA',
    'DISTRICT OF COLUMBIA': 'DC', 'D.C.': 'DC', 'WASHINGTON DC': 'DC',
    'PUERTO RICO': 'PR',
}


class StateValidator:
    """Validates and normalizes US state names and abbreviations"""
    
    def __init__(self):
        """Initialize the state validator"""
        self.valid_states = US_STATES
        self.aliases = STATE_ALIASES
        self.full_names = FULL_NAME_TO_ABBREV
    
    def validate_state(self, state_input):
        """
        Validate and normalize a state input
        
        Args:
            state_input (str): User input for state (abbreviation or full name)
        """
        if not state_input or not state_input.strip():
            return True, None, None  # Empty state is allowed
        
        # Clean and normalize input
        clean_input = state_input.strip().upper()
        
        # Direct match with abbreviations
        if clean_input in self.valid_states:
            return True, clean_input, None
        
        # Check aliases and variations
        if clean_input in self.aliases:
            return True, self.aliases[clean_input], None
        
        # Check full names
        if clean_input in self.full_names:
            return True, self.full_names[clean_input], None
        
        # Try to find close matches for suggestions
        suggestion = self._find_closest_match(clean_input)
        
        return False, None, suggestion
    
    def _find_closest_match(self, invalid_input):
        """
        Find the closest matching state for suggestions
        
        Args:
            invalid_input (str): The invalid state input
            
        Returns:
            str: Suggested state name or None if no close match found
        """
        invalid_input = invalid_input.upper()
        
        # Check for partial matches in abbreviations
        for abbrev in self.valid_states:
            if invalid_input.startswith(abbrev[:2]) or abbrev.startswith(invalid_input[:2]):
                return f"{abbrev} ({self.valid_states[abbrev]})"
        
        # Check for partial matches in full names
        for abbrev, full_name in self.valid_states.items():
            if (invalid_input in full_name.upper() or 
                full_name.upper().startswith(invalid_input) or
                any(word.startswith(invalid_input) for word in full_name.upper().split())):
                return f"{abbrev} ({full_name})"
        
        # Check for partial matches in aliases
        for alias, abbrev in self.aliases.items():
            if invalid_input in alias or alias.startswith(invalid_input):
                return f"{abbrev} ({self.valid_states[abbrev]})"
        
        return None
    
    def get_state_full_name(self, state_abbrev):
        """
        Get full state name from abbreviation
        Returns:
            str: Full state name or None if not found
        """
        return self.valid_states.get(state_abbrev.upper() if state_abbrev else None)
    
    def get_all_states(self):
        """
        Get all valid state abbreviations and names
        
        Returns:
            dict: Dictionary of state abbreviations to full names
        """
        return self.valid_states.copy()
    
    def format_state_list(self):
        """
        Format a readable list of valid states for error messages
        
        Returns:
            str: Formatted string of valid states
        """
        states_list = []
        for abbrev, full_name in sorted(self.valid_states.items()):
            states_list.append(f"{abbrev} ({full_name})")
        
        # Group by regions for better readability
        return "Valid states include: " + ", ".join(states_list[:10]) + "... (and 40+ more)"
