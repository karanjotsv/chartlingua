import sys
import json
import os
import plotly.graph_objects as go

# --- 1. Load Data from JSON ---
# The script must be called with the JSON file path as the first argument.
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Ensure the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Derive the output filename from the input JSON filename
filename_base = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{filename_base}.png"

# Read the JSON data with UTF-8 encoding to support multilingual text
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors from the loaded JSON
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# --- 2. Create the Plotly Figure ---
fig = go.Figure()

# --- 3. Add Data Traces ---
# Iterate through the data series in the JSON and add them to the figure
for i, series in enumerate(chart_data):
    color = colors[i % len(colors)] if colors else '#000000'
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        mode='lines+markers',
        line=dict(color=color, width=2),
        marker=dict(color=color, symbol='diamond', size=6),
        showlegend=False
    ))

# --- 4. Configure Layout and Styling ---
fig.update_layout(
    # Title
    title=dict(
        text=texts.get('title'),
        x=0.5,
        y=0.95,
        font=dict(
            family="Arial",
            size=20,
            color='black'
        )
    ),

    # X-Axis
    xaxis=dict(
        title=dict(
            text=texts.get('x_axis_title'),
            font=dict(family="Arial", size=14, color='black')
        ),
        tickfont=dict(family="Arial", size=12, color='black'),
        showgrid=False,
        showline=True,
        linecolor='gray',
        linewidth=1,
        range=[1889, 1951],
        tickmode='array',
        tickvals=[1890, 1900, 1910, 1920, 1930, 1940, 1950]
    ),

    # Y-Axis
    yaxis=dict(
        title=dict(
            text=texts.get('y_axis_title'),
            font=dict(family="Arial", size=14, color='black')
        ),
        tickfont=dict(family="Arial", size=12, color='black'),
        showgrid=True,
        gridcolor='lightgrey',
        showline=True,
        linecolor='gray',
        linewidth=1,
        range=[-6000, 12500],
        tickmode='array',
        tickvals=[-6000, -4000, -2000, 0, 2000, 4000, 6000, 8000, 10000, 12000],
        zeroline=False
    ),

    # General Layout Properties
    font=dict(family="Arial"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=80, r=40, t=100, b=80),  # Adjust margins to prevent clipping
    autosize=False,
    width=700,
    height=550
)

# Bolden the titles using layout.font.family for broad application
# Plotly's support for bold weight can be inconsistent across renderers;
# this approach via annotations or direct title font dict is more reliable.
fig.update_layout(
    title_font_weight="bold",
    xaxis_title_font_weight="bold",
    yaxis_title_font_weight="bold"
)

# --- 5. Output the Chart ---
# Save the figure to a high-resolution PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")