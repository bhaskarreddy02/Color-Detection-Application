import pandas as pd
import numpy as np
from math import sqrt

import pandas as pd

# Load the color dataset
colors = pd.read_csv("data/colors.csv")

def get_closest_color(r, g, b):
    if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
        raise ValueError("RGB values must be in the range 0-255")

    min_distance = float("inf")
    closest_color = None
    
    for _, row in colors.iterrows():
        distance = sqrt(
            (r - float(row["red"])) ** 2 +
                    (g - float(row["green"])) ** 2 +
                    (b - float(row["blue"])) ** 2) 
        # print(row['color_name'], distance)
        if distance < min_distance:
            min_distance = distance
            closest_color = row
    # print("closest color: ", closest_color['color_name'], r, g, b )
    return closest_color["color_name"]



# def get_closest_color(r, g, b):
#     """
#     Returns the closest CSS3 color name for the given RGB values.
    
#     Args:
#         r (int): Red component (0-255)
#         g (int): Green component (0-255)
#         b (int): Blue component (0-255)
        
#     Returns:
#         str: Closest CSS3 color name
#     """
#     min_distance = None
#     closest_color_name = None

#     for hex_value, color_name in webcolors.CSS3_HEX_TO_NAMES.items():
#         # Convert HEX to RGB
#         r_c, g_c, b_c = webcolors.hex_to_rgb(hex_value)
        
#         # Calculate Euclidean distance between the colors
#         distance = (int(r) - int(r_c)) ** 2 + (int(g) - int(g_c)) ** 2 + (int(b) - int(b_c)) ** 2
        
#         if (min_distance is None) or (distance < min_distance):
#             min_distance = distance
#             closest_color_name = color_name
    
#     return closest_color_name
# Test the function
if __name__ == "__main__":
    test_rgb = (54, 55, 52)  # Example color
    print("Closest color:", get_closest_color(*test_rgb))
