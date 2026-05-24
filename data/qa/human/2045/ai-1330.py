import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# --- 1. Load Configuration from JSON ---
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# --- 2. Prepare Data for Plotting ---
categories = [item.get('category', '') for item in chart_data]
values = [item.get('value', 0) for item in chart_data]

# --- 3. Create the Chart Figure ---
fig = go.Figure()

# --- 4. Add Bar Trace ---
# The primary bar trace with data, styling, and text labels.
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else '#1f77b4',
    text=[f'{v}%' for v in values],
    textposition='outside',
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    ),
    cliponaxis=False  # Prevents text labels from being cut off at the top of the chart
))

# --- 5. Configure Layout and Styling ---
fig.update_layout(
    font=dict(family="Arial", size=12, color='black'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showline=True,
        linecolor='black',
        linewidth=1,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=[0, 80],
        tickvals=[0, 20, 40, 60, 80],
        ticktext=[f'{v}%' for v in [0, 20, 40, 60, 80]],
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        zeroline=False,
        showline=False
    ),
    margin=dict(t=50, b=120, l=80, r=40)
)

# --- 6. Add Source Annotation ---
# Add source text at the bottom right, outside the plot area.
if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        xref="paper", yref="paper",
        x=0.99, y=-0.25,  # Positioned at the bottom right
        showarrow=False,
        xanchor='right',
        yanchor='top',
        font=dict(size=12)
    )

# --- 7. Output the Chart ---
output_path = Path(json_path)
output_filename = output_path.with_suffix('.png').name
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")