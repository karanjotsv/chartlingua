import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_file_path = sys.argv[1]
output_filename_base = pathlib.Path(json_file_path).stem

# Read and parse the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# Extract data and texts from the loaded JSON
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', ['#1f77b4'])

# Prepare data for Plotly
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker_color=colors[0],
    texttemplate='%{x}%',
    textposition='outside',
    cliponaxis=False,  # Prevents text from being clipped
    textfont=dict(family="Arial", size=12, color='black')
))

# Update layout for a clean, professional look
fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#e0e0e0',
        griddash='dot',
        ticksuffix='%',
        zeroline=False,
        # Set range to provide space for the text labels on the right
        range=[0, max(values) * 1.18]
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True, # Faint horizontal lines
        gridcolor='#e0e0e0',
        griddash='dot',
        autorange='reversed'  # To display categories from top to bottom
    ),
    bargap=0.4,
    margin=dict(l=100, r=40, t=30, b=80),
    # Use annotation for the source text for precise placement
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref="paper", yref="paper",
            x=0.98, y=-0.15,
            xanchor='right', yanchor='top',
            font=dict(family="Arial", size=10, color='grey')
        )
    ]
)

# Define the output PNG filename
output_png_path = f"{output_filename_base}.png"

# Save the figure as a PNG image
fig.write_image(output_png_path, scale=2)

print(f"Chart successfully generated and saved to {output_png_path}")