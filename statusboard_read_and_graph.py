
# ██ ███    ███ ██████   ██████  ██████  ████████ ███████
# ██ ████  ████ ██   ██ ██    ██ ██   ██    ██    ██
# ██ ██ ████ ██ ██████  ██    ██ ██████     ██    ███████
# ██ ██  ██  ██ ██      ██    ██ ██   ██    ██         ██
# ██ ██      ██ ██       ██████  ██   ██    ██    ███████

import pandas as pd ### Standard dataframe manipulation library in Python – use to create 'dataframes' conceptually equivalent to excel tables
# https://pandas.pydata.org
import json # json reading library
from pandas.io.json import json_normalize ## Useful for more advanced json wrangling, flattens JSON into tables
# https://pandas.pydata.org/docs/reference/api/pandas.json_normalize.html
import matplotlib.pyplot as plt ## Matplotlib is the standard Python plotting library, good for simple bar or line plotting


# ███████ ██    ██ ███    ██  ██████ ████████ ██  ██████  ███    ██ ███████
# ██      ██    ██ ████   ██ ██         ██    ██ ██    ██ ████   ██ ██
# █████   ██    ██ ██ ██  ██ ██         ██    ██ ██    ██ ██ ██  ██ ███████
# ██      ██    ██ ██  ██ ██ ██         ██    ██ ██    ██ ██  ██ ██      ██
# ██       ██████  ██   ████  ██████    ██    ██  ██████  ██   ████ ███████


def read_in_data(file_path):
# Read JSON data from a file
    with open(file_path, 'r') as file:
        data = json.load(file)
    # Extract the graph title
    graph_title = data["graph"]["title"]
    # Prepare data for the DataFrame and plotting
    rows = []
    colors = {}  # Store colors for each series
    series_titles={} # store each series title, e,g, X-Cola, Y-Cola etc
    plot_type = data["graph"].get("type", "bar")  # Default to bar if type is not specified
    # Loop through datasequences
    for series in data["graph"]["datasequences"]: # read through each data sequence entry
        series_title = series["title"] # read in the data title e.g, X-Cola
        series_color = series.get("color", "blue")  # Default to a blue color if not specified
        colors[series_title] = series_color
        series_titles[series_title] = series  # Add series_title to series_titles
        for point in series["datapoints"]:
            x_value = point["title"]
            y_value = point["value"]
            rows.append( {"x_value": x_value, f"{series_title}": y_value})
    # Convert rows to a DataFrame
    df = pd.DataFrame(rows)
    # Reshape the DataFrame to combine the same years into rows
    df = df.pivot_table(index=[ "x_value"], aggfunc='first').reset_index()
    return locals() # return all local variables as a python dictonary object


def plot_graph(in_dict):
    plt.style.use('dark_background')  # Set black background
    fig, ax = plt.subplots(figsize=(10, 6))
    df =in_dict['df']
    plot_type=in_dict['plot_type']
    colors =in_dict['colors']
    graph_title=in_dict['graph_title']
    if plot_type == "bar":
        df.plot(kind='bar', ax=ax, color=[colors[col] for col in df.columns[1:]], legend=False)
    elif plot_type == "line":
        df.plot(kind='line', ax=ax, color=[colors[col] for col in df.columns[1:]], legend=False)
    else:
        raise ValueError(f"Unsupported plot type: {plot_type}")
        # Add labels and title
    plt.title(graph_title)
    # Add labels above each bar
    for container in ax.containers:
        ax.bar_label(container, fmt="%.1f", label_type="edge", color="white", fontsize=10)
    # Set x-axis labels to df['x_value']
    ax.set_xticks(range(len(df)))
    ax.set_xticklabels(df['x_value'], fontsize=12, color='white')
    plt.xticks(rotation=0)
    # Hide the y-axis labels
    ax.set_yticklabels([])
    plt.legend(frameon=False, fontsize=10, title_fontsize=12)
    # Remove axis borders
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    # Save the plot before displaying it
    plt.tight_layout()
    plt.draw()  # Ensure the plot is fully drawn
    plt.savefig('example_output.png')  # Save the plot
    plt.show()  # Display the plot
    plt.close()  # Close the figure to avoid memory issues






# ██████  ███████  █████  ██████      ██ ███    ██     ████████ ██   ██ ███████     ██████   █████  ████████  █████
# ██   ██ ██      ██   ██ ██   ██     ██ ████   ██        ██    ██   ██ ██          ██   ██ ██   ██    ██    ██   ██
# ██████  █████   ███████ ██   ██     ██ ██ ██  ██        ██    ███████ █████       ██   ██ ███████    ██    ███████
# ██   ██ ██      ██   ██ ██   ██     ██ ██  ██ ██        ██    ██   ██ ██          ██   ██ ██   ██    ██    ██   ██
# ██   ██ ███████ ██   ██ ██████      ██ ██   ████        ██    ██   ██ ███████     ██████  ██   ██    ██    ██   ██


data_dict =read_in_data('json_example.json')
# e.g., data_dict['df'] will return the data frame in format like
#   graph_title x_value  X-Cola  Y-Cola
# 0  Soft Drink Sales    2008    22.0    18.4
# 1  Soft Drink Sales    2009    24.0    20.1
# 2  Soft Drink Sales    2010    25.5    24.8
# 3  Soft Drink Sales    2011    27.9    26.1
# 4  Soft Drink Sales    2012    31.0    29.0


# ██████  ██       ██████  ████████     ██ ████████
# ██   ██ ██      ██    ██    ██        ██    ██
# ██████  ██      ██    ██    ██        ██    ██
# ██      ██      ██    ██    ██        ██    ██
# ██      ███████  ██████     ██        ██    ██



plot_graph(data_dict)



# ███████ ███    ██ ██████
# ██      ████   ██ ██   ██
# █████   ██ ██  ██ ██   ██
# ██      ██  ██ ██ ██   ██
# ███████ ██   ████ ██████
