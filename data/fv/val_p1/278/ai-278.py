import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# --- 1. Load Data ---
# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <path_to_json_file>")
    sys.exit(1)

json_path = Path(sys.argv[1])
filename_base = json_path.stem

# Read the chart data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# --- 2. Create Chart ---
# Initialize the figure
fig = go.Figure()

# Add a trace for each data series
for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        mode='lines',
        line=dict(color=colors[i % len(colors)]),
        showlegend=False
    ))
    # Add annotation for the line label
    label_pos = series.get('label_pos', {})
    fig.add_annotation(
        x=label_pos.get('x'),
        y=label_pos.get('y'),
        text=series.get('name', ''),
        showarrow=False,
        font=dict(family="Arial", size=14),
        xanchor='left',
        yanchor='middle'
    )

# Add general annotations from the JSON
for ann in texts.get('annotations', []):
    fig.add_annotation(
        x=ann.get('x'),
        y=ann.get('y'),
        text=ann.get('text', ''),
        showarrow=False,
        font=dict(family="Arial", size=14),
        align='center',
        xanchor='left' if ann.get('x', 0) > 1.0 else 'right'
    )
    
# Add the vertical line separating the regions
fig.add_vline(x=1.0, line_width=1, line_dash="solid", line_color="black")


# --- 3. Configure Layout ---
# Combine title and subtitle using HTML for formatting
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Update the layout of the figure
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        font=dict(family="Arial", size=18)
    ),
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=dict(
        text=texts.get('y_axis_title'),
        standoff=10
    ),
    font=dict(family="Arial", size=12),
    xaxis=dict(
        range=[0, 2.05],
        tickmode='linear',
        tick0=0,
        dtick=0.2,
        showgrid=False,
        zeroline=False,
        linecolor='black',
        mirror=True,
        ticks='outside'
    ),
    yaxis=dict(
        range=[0, 5.1],
        tickmode='linear',
        tick0=1.00,
        dtick=1.00,
        tickformat=".2f",
        showgrid=False,
        zeroline=False,
        linecolor='black',
        mirror=True,
        ticks='outside'
    ),
    plot_bgcolor='white',
    margin=dict(l=70, r=50, t=80, b=80),
    width=800,
    height=500
)

# --- 4. Output Image ---
# Define the output filename and save the figure as a PNG image
output_filename = f"{filename_base}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")