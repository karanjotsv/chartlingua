import sys
import json
import os
import plotly.graph_objects as go

# --- 1. Load Data from JSON ---
# The script requires the path to the JSON file as a command-line argument.
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read the JSON data file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# --- 2. Extract Data and Texts ---
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

# Prepare data for Plotly trace
x_values = [d['x'] for d in data]
y_values = [d['y'] for d in data]

# --- 3. Create the Chart ---
# Initialize the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0],
    text=y_values,
    textposition='outside',
    cliponaxis=False  # Prevent text labels from being clipped
))

# --- 4. Configure Layout and Styling ---
fig.update_layout(
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        type='category',
        title_text=texts.get('x_axis_title'),
        showline=True,
        linewidth=1,
        linecolor='black',
        tickfont=dict(size=12),
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 5100],
        dtick=1000,
        showgrid=True,
        gridcolor='#e0e0e0',
        zeroline=False
    ),
    margin=dict(l=80, r=20, t=50, b=80),
    # Add source annotation at the bottom
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref="paper", yref="paper",
            x=0.99, y=-0.15,
            xanchor='right', yanchor='top',
            align="right",
            font=dict(size=10)
        )
    ]
)

# Update trace text font specifically
fig.update_traces(
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    ),
    texttemplate='%{text:,}' # Format number with comma for thousands
)

# --- 5. Output the Image ---
# Derive the output filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")