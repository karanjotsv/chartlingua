import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read the JSON data file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and text from the config
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])
legend_labels = texts.get('legend_labels', [])

# Prepare data for Plotly
categories = [item['category'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add a trace for each data series
for i in range(len(legend_labels)):
    values = [item['values'][i] for item in chart_data]
    fig.add_trace(go.Bar(
        y=categories,
        x=values,
        name=legend_labels[i],
        orientation='h',
        marker=dict(color=colors[i])
    ))

# Combine title and subtitle if available
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

# Update layout
fig.update_layout(
    barmode='stack',
    title=dict(
        text=title_text,
        x=0.5,
        font=dict(size=20)
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='lightgrey',
        zeroline=False
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        autorange='reversed',  # To display categories from top to bottom
        tickmode='array',
        tickvals=categories,
        ticktext=[cat.replace('...', '') for cat in categories] # Handle truncation for display
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.25,
        xanchor='right',
        x=1
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=350, r=40, t=80, b=100) # Increased left margin for long labels
)

# Generate output filename from input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error writing image file: {e}")
    sys.exit(1)