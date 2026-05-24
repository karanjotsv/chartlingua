import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load Data from JSON ---
# Check if a command-line argument is provided
if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_path = pathlib.Path(sys.argv[1])

# Verify the JSON file exists
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Read the JSON data
with open(json_path, 'r', encoding='utf-8') as f:
    chart_data_json = json.load(f)

# --- 2. Extract Data and Texts for Plotting ---
chart_data = chart_data_json['chart_data']
texts = chart_data_json['texts']
colors = chart_data_json['colors']

# Prepare data for the pie chart trace
labels = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# --- 3. Create the Chart Figure ---
fig = go.Figure()

# Add the pie chart trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#000000', width=1)),
    sort=False,  # Preserve the order from the JSON file
    direction='clockwise',
    textinfo='none',  # No text on slices as per original
    pull=[0.01] * len(labels), # Slight pull for visual separation
    hovertemplate='%{label}<br>%{value}%<extra></extra>'
))

# --- 4. Configure Layout and Styling ---
# Combine title and subtitle
title_text = f"<b>{texts['title']}</b>"
if texts['subtitle']:
    title_text += f"<br>{texts['subtitle']}"

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        xanchor='center',
        y=0.95,
        yanchor='top'
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    showlegend=True,
    legend=dict(
        orientation="v",
        x=0.5,
        xanchor='center',
        y=-0.1,  # Position legend below the chart area
        yanchor='top',
        bgcolor='rgba(0,0,0,0)' # Transparent background
    ),
    margin=dict(t=100, b=250, l=40, r=40), # Ample margin for title, legend, and source
    paper_bgcolor='white',
    plot_bgcolor='white',
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.5,
            y=-0.22, # Position below the legend
            xanchor='center',
            yanchor='top',
            align='center',
            font=dict(size=10)
        )
    ]
)

# --- 5. Output the Image ---
# Derive output filename from the input JSON filename
output_filename_base = json_path.stem
output_path = f"{output_filename_base}.png"

# Write the image file
fig.write_image(output_path, scale=2)

print(f"Chart saved to '{output_path}'")