import pandas as pd
import numpy as np
import webcolors

# Load the color dataset
df = pd.read_csv("data/colors.csv")

def get_closest_color(r, g, b):
    """
    Returns the closest CSS3 color name for the given RGB values.
    
    Args:
        r (int): Red component (0-255)
        g (int): Green component (0-255)
        b (int): Blue component (0-255)
        
    Returns:
        str: Closest CSS3 color name
    """
    min_distance = None
    closest_color_name = None

    for hex_value, color_name in webcolors.CSS3_HEX_TO_NAMES.items():
        # Convert HEX to RGB
        r_c, g_c, b_c = webcolors.hex_to_rgb(hex_value)
        
        # Calculate Euclidean distance between the colors
        distance = (int(r) - int(r_c)) ** 2 + (int(g) - int(g_c)) ** 2 + (int(b) - int(b_c)) ** 2
        
        if (min_distance is None) or (distance < min_distance):
            min_distance = distance
            closest_color_name = color_name
    
    return closest_color_name
# Test the function
if __name__ == "__main__":
    test_rgb = (250, 180, 30)  # Example color
    print("Closest color:", get_closest_color(*test_rgb))
