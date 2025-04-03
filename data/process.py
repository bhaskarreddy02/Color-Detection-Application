
import pandas as pd

colors = {
    'color_name': [],
    'red': [],
    'green': [],
    'blue': []
}

with open('./raw_data.txt', 'r') as file:
    for line in file:
    
        split1 = line.split('#')
        color_name = split1[0]
        color_name = color_name.strip()

        rgb = split1[1].split("(")[1]
        rgb=rgb[:-2]
        r,g,b = rgb.split(',')

        colors['color_name'].append(color_name)
        colors['red'].append(r)
        colors['green'].append(g)
        colors['blue'].append(b)

        # print(color_name, r,g,b)


print(len(colors['blue']),len(colors['green']), len(colors['red']))
df = pd.DataFrame(colors)
df.set_index('color_name', inplace=True)

print(df.head())

df.to_csv('colors.csv')
print("done")


