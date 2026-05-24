import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Load data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts from the JSON structure
chart_data = chart_config['chart_data']
texts = chart_config['texts']
colors = chart_config['colors']

# Prepare data lists for plotting, preserving order
categories = [d['category'] for d in chart_data]
rights = [d['right'] for d in chart_data]
centers = [d['center'] for d in chart_data]
lefts = [d['left'] for d in chart_data]

# Initialize the figure
fig = go.Figure()

# Add light grey bars connecting the 'right' and 'left' points
fig.add_trace(go.Bar(
    y=categories,
    x=[l - r for r, l in zip(rights, lefts)],
    base=rights,
    orientation='h',
    marker=dict(
        color=colors['bar'],
        line=dict(color=colors['bar'], width=1)
    ),
    showlegend=False,
    hoverinfo='none'
))

# Add scatter points for the 'right' political view
fig.add_trace(go.Scatter(
    y=categories,
    x=rights,
    mode='markers',
    name=texts['legend_right'],
    marker=dict(color=colors['series'][0], size=15, symbol='circle'),
    hoverinfo='x+y'
))

# Add scatter points for the 'center' political view
fig.add_trace(go.Scatter(
    y=categories,
    x=centers,
    mode='markers',
    name=texts['legend_center'],
    marker=dict(color=colors['series'][1], size=15, symbol='circle'),
    hoverinfo='x+y'
))

# Add scatter points for the 'left' political view
fig.add_trace(go.Scatter(
    y=categories,
    x=lefts,
    mode='markers',
    name=texts['legend_left'],
    marker=dict(color=colors['series'][2], size=15, symbol='circle'),
    hoverinfo='x+y'
))

# Update layout for a clean, accurate look
fig.update_layout(
    title=dict(
        text=texts['title'],
        x=0.5,
        xanchor='center',
        font=dict(size=20)
    ),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        range=[0, 100],
        ticksuffix='%',
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        autorange='reversed',
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1
    ),
    font=dict(
        family="Arial",
        size=14
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=120, r=40, t=100, b=80),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5
    ),
    barmode='stack'
)

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")