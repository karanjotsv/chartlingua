import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts from the JSON structure
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']
series = chart_data['series'][0]

# --- Chart Creation ---
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=chart_data['categories'],
    y=series['values'],
    name=series['name'],
    marker_color=colors[0],
    text=[f"{v}%" for v in series['values']],
    textposition='outside',
    cliponaxis=False # Prevents text on tallest bar from being clipped
))

# --- Layout Configuration ---
fig.update_layout(
    template='plotly_white',
    font=dict(
        family="Arial",
        size=12
    ),
    showlegend=False,
    margin=dict(t=50, b=100, l=80, r=40),
    xaxis=dict(
        title_text=None,
        tickfont=dict(size=12),
        type='category' # Ensures the original order of categories is preserved
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        title_font=dict(size=14),
        tickfont=dict(size=12),
        range=[0, 8.5], # Give extra space for the 7% label
        tickvals=[0, 1, 2, 3, 4, 5, 6, 7, 8],
        ticktext=[f"{i}%" for i in range(9)],
        gridcolor='#e5e5e5'
    ),
    annotations=[
        dict(
            showarrow=False,
            text=texts.get('footer_left', ''),
            xref="paper",
            yref="paper",
            x=0,
            y=-0.2,
            xanchor='left',
            yanchor='bottom',
            font=dict(size=12, color="#0073B2")
        ),
        dict(
            showarrow=False,
            text=texts.get('footer_right', ''),
            xref="paper",
            yref="paper",
            x=1,
            y=-0.2,
            xanchor='right',
            yanchor='bottom',
            font=dict(size=12, color="#666666")
        )
    ]
)

# --- Output ---
# Derive the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")