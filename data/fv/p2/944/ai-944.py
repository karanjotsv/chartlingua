import sys
import json
import os
import plotly.graph_objects as go

# Ensure a command-line argument is provided for the JSON file path
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read and decode the JSON data from the specified file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

# Extract data, texts, and colors from the loaded JSON
chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

# Prepare data for Plotly pie chart
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create custom text for each slice, combining the label and percentage value
pie_texts = [f"{item['label']}<br>{item['value']}%" for item in chart_data]

# Create the pie chart figure
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,  # Used for hover information
    values=values,
    text=pie_texts,
    textinfo='text',
    textposition='outside',
    marker_colors=colors,
    sort=False,  # This is crucial to preserve the order from the JSON file
    direction='clockwise',
    rotation=-70 # Adjust rotation to approximate the original chart's orientation
))

# Combine title and source into a single string with HTML for styling
title_text = f"<b>{texts['title']}</b>"
if texts.get('source'):
    title_text += f"<br><span style='font-size: 10px;'>{texts['source']}</span>"

# Update the layout for a clean and accurate presentation
fig.update_layout(
    title_text=title_text,
    title_x=0.5,
    title_y=0.95,
    title_xanchor='center',
    title_yanchor='top',
    font_family="Arial",
    showlegend=False,
    margin=dict(t=120, b=80, l=80, r=80), # Adjust margins to prevent label clipping
    paper_bgcolor='white',
    plot_bgcolor='white',
    uniformtext_minsize=10, # Ensure text is readable
    uniformtext_mode='hide'
)

# Update trace properties for better text appearance
fig.update_traces(
    textfont_size=12,
    pull=[0, 0, 0, 0, 0, 0, 0.05] # Slightly pull the smallest slice for visibility
)

# Determine the output filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure to a PNG file with high resolution
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart successfully saved to '{output_filename}'")
except Exception as e:
    print(f"Error writing image file: {e}")
    sys.exit(1)