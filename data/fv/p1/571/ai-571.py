import sys
import json
import pathlib
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

# Extract data for plotting
chart_data = chart_info.get("chart_data", [])
colors = chart_info.get("colors", [])
texts = chart_info.get("texts", {})

# Create subplots for the two pie charts
fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])

# Add the two pie charts to the subplots
for i, chart in enumerate(chart_data):
    labels = [d['label'] for d in chart['data']]
    values = [d['value'] for d in chart['data']]
    
    fig.add_trace(go.Pie(
        labels=labels,
        values=values,
        marker=dict(
            colors=colors[i],
            line=dict(color='#000000', width=1.5)
        ),
        pull=[0.05] * len(values),
        textposition='outside',
        textinfo='label',
        sort=False,  # Preserve the original data order
        direction='clockwise',
        hoverinfo='none',
        domain=dict(x=[0, 0.48] if i == 0 else [0.52, 1.0])
    ), row=1, col=i + 1)

# Update layout for a clean, professional look
fig.update_layout(
    showlegend=False,
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    height=450,
    width=800,
    margin=dict(l=20, r=20, t=20, b=100),
    annotations=[
        dict(
            text=chart_data[0]['title'],
            x=0.20, y=0,
            xref="paper", yref="paper",
            xanchor='center', yanchor='top',
            showarrow=False,
            font=dict(size=14, family="Arial")
        ),
        dict(
            text=chart_data[1]['title'],
            x=0.80, y=0,
            xref="paper", yref="paper",
            xanchor='center', yanchor='top',
            showarrow=False,
            font=dict(size=14, family="Arial")
        )
    ]
)

# Derive output filename from JSON path and save the image
filename_base = pathlib.Path(json_path).stem
output_filename = f"{filename_base}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")