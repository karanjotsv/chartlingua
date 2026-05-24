import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for the required command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

# Use pathlib for robust path handling
json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Derive the output filename from the input JSON filename
output_path = json_path.with_suffix('.png')

# Read and parse the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data_json = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON file at {json_path}")
    sys.exit(1)

# Extract data and texts from the JSON structure
chart_data = chart_data_json['chart_data']
texts = chart_data_json['texts']
colors = chart_data_json['colors']

# Prepare data for Plotly pie chart
labels = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Generate text labels and their positions based on the original chart
# Large slices get inside labels, small ones get outside labels.
# Use HTML span tags to control text color for inside labels individually.
text_labels = []
text_positions = []

for item in chart_data:
    category = item['category']
    value = item['value']
    if category == "Soviet Union":
        text_labels.append(f'<span style="color:white">{category}<br>{value}%</span>')
        text_positions.append('inside')
    elif category == "China":
        text_labels.append(f'<span style="color:black">{category}<br>{value}%</span>')
        text_positions.append('inside')
    else:
        text_labels.append(f"{category} {value}%")
        text_positions.append('outside')

# Create the pie chart trace
pie_trace = go.Pie(
    labels=labels,
    values=values,
    text=text_labels,
    textinfo='text',  # Use the custom text labels provided
    textposition=text_positions,
    marker=dict(
        colors=colors,
        line=dict(color='black', width=1) # Add a border to slices
    ),
    sort=False,  # Preserve the order from the JSON file
    direction='clockwise',
    insidetextfont=dict(family="Arial", size=14),
    outsidetextfont=dict(family="Arial", size=12, color="black")
)

# Create the figure and update layout
fig = go.Figure(data=[pie_trace])

# Combine title and subtitle using HTML for formatting
title_text = f"<b>{texts['title']}</b><br>{texts['subtitle']}"

fig.update_layout(
    title_text=title_text,
    title_x=0.5,
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    showlegend=False,
    margin=dict(t=120, b=40, l=40, r=40),
    paper_bgcolor='white',
    width=800,
    height=600
)

# Save the figure as a PNG image
try:
    fig.write_image(output_path, scale=2)
    print(f"Chart saved to {output_path}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)