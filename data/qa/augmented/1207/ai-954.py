import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_path = pathlib.Path(sys.argv[1])

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data_json = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data, texts, and colors from JSON
chart_data = chart_data_json.get('chart_data', [])
texts = chart_data_json.get('texts', {})
colors = chart_data_json.get('colors', [])
output_filename_base = json_path.stem

# Prepare data for Plotly
x_values = [d['x'] for d in chart_data]
y_values = [d['y'] for d in chart_data]
text_labels = [f"{d['y']}%" for d in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    text=text_labels,
    textposition='outside',
    marker_color=colors[0] if colors else None,
    cliponaxis=False  # Prevents text labels from being clipped
))

# Construct title and source strings
title_text = texts.get('title') or ''
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

source_text = texts.get('source') or ''
if texts.get('note'):
    source_text += f"<br>{texts.get('note')}"

# Update layout
fig.update_layout(
    font_family="Arial",
    title_text=title_text,
    title_x=0.05,
    title_font_size=20,
    plot_bgcolor='white',
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 60],
        ticksuffix='%',
        showgrid=True,
        gridcolor='lightgray',
        tickfont=dict(size=12)
    ),
    margin=dict(l=80, r=40, t=50, b=100),
    showlegend=False,
    annotations=[
        dict(
            showarrow=False,
            text=source_text,
            xref="paper",
            yref="paper",
            x=1.0,
            y=-0.2,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=12)
        )
    ]
)

# Set the bar text font size
fig.update_traces(textfont_size=12)

# Save the figure to a PNG file
output_path = f"{output_filename_base}.png"
fig.write_image(output_path, scale=2)

print(f"Chart saved to {output_path}")