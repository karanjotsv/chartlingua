import sys
import json
import os
import plotly.graph_objects as go

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Load data from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for the chart
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])

# Prepare data for Plotly
labels = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the donut chart trace
# The data needs to be reordered to match the visual clockwise layout starting from the largest slice
# Original legend order: Highly, Quite, The basics, Not at all
# Visual clockwise order: Not at all, Highly, Quite, The basics
# To match the visual, we reorder the data and colors based on the visual representation.
visual_order_indices = [3, 0, 1, 2] # Indices from original data to match visual layout
ordered_labels = [labels[i] for i in visual_order_indices]
ordered_values = [values[i] for i in visual_order_indices]
ordered_colors = [colors[i] for i in visual_order_indices]

# The legend, however, should follow the original logical order.
# We will create the plot with the visual order and then manually set legend item order.
# Plotly's traceorder for pie charts defaults to 'data', so we control the legend by data order.
# Let's use the original order for both data and legend and let Plotly arrange it.
# The visual clockwise starting point can be controlled with 'rotation'.
# After inspection, the largest slice (46%) starts at roughly 45 degrees.
# Let's stick to the legend order in the data, as it's more robust. Plotly will arrange it.

fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    hole=0.5,
    marker=dict(
        colors=colors,
        line=dict(color='white', width=3)
    ),
    texttemplate='%{value}%',
    textposition='inside',
    textfont=dict(color='white', size=16, family="Arial"),
    hoverinfo='label+percent',
    sort=False,  # This is crucial to preserve the order from the JSON data
    direction='clockwise',
    rotation=100 # Adjust rotation to place the largest slice at the top-right
)])

# Update layout for title, fonts, legend, and margins
fig.update_layout(
    title=dict(
        text=texts.get('title'),
        x=0.5,
        xanchor='center',
        y=0.95,
        yanchor='top'
    ),
    font=dict(
        family="Arial",
        size=14
    ),
    legend=dict(
        x=0.5,
        y=-0.05,
        xanchor='center',
        yanchor='top',
        orientation='h', # Use horizontal legend to better fit below
        traceorder='normal'
    ),
    showlegend=True,
    margin=dict(l=40, r=40, t=140, b=80),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

# Generate the output filename from the input JSON path
base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

# Save the chart as a PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved as {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    print("Please ensure you have 'kaleido' installed (`pip install kaleido`) for image export.")
    sys.exit(1)