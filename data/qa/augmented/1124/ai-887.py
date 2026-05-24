import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
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

# Extract data and text from the JSON structure
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly
categories = [d['category'] for d in chart_data]
values = [d['value'] for d in chart_data]
bar_texts = [f"{v:.2f}%" for v in values]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=bar_texts,
    textposition='outside',
    marker_color=colors[0] if colors else None,
    cliponaxis=False
))

# Configure the layout
fig.update_layout(
    font_family="Arial",
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(t=30, b=100, l=80, r=20),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=[-10, 6],
        dtick=2.5,
        ticksuffix='%',
        gridcolor='#e9e9e9',
        zeroline=True,
        zerolinecolor='black',
        zerolinewidth=1.5
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=False,
        tickfont=dict(size=12)
    ),
    annotations=[
        dict(
            text=texts.get('note'),
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.18,
            xanchor='left',
            yanchor='top'
        ),
        dict(
            text=texts.get('source'),
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.18,
            xanchor='right',
            yanchor='top'
        )
    ]
)

fig.update_traces(
    textfont_size=12,
    textfont_color='black'
)


# Determine output filename and save the image
output_filename = Path(json_path).stem + '.png'
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")