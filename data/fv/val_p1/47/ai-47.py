import sys
import json
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data from the loaded JSON
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Create subplots for the two pie charts
fig = make_subplots(
    rows=1,
    cols=2,
    specs=[[{'type': 'domain'}, {'type': 'domain'}]]
)

# Add a pie chart trace for each dataset in chart_data
for i, data in enumerate(chart_data):
    fig.add_trace(go.Pie(
        labels=data['labels'],
        values=data['values'],
        marker_colors=colors[i],
        sort=False,  # Preserve the order from the JSON file
        direction='clockwise',
        marker=dict(line=dict(color='#000000', width=1.5)),
        textfont=dict(size=11, family="Arial", color="black"),
    ), row=1, col=i + 1)

# Update trace properties for all pie charts
fig.update_traces(
    textposition='inside',
    textinfo='label',
    insidetextorientation='radial',
    hoverinfo='label+percent'
)

# Create annotations for subplot titles and the main source text
annotations = []
# Subplot titles
if len(chart_data) > 0:
    annotations.append(dict(
        text=chart_data[0]['title'], x=0.22, y=0.1, xref='paper', yref='paper',
        showarrow=False, font=dict(size=12, family="Arial")
    ))
if len(chart_data) > 1:
    annotations.append(dict(
        text=chart_data[1]['title'], x=0.78, y=0.1, xref='paper', yref='paper',
        showarrow=False, font=dict(size=12, family="Arial")
    ))

# Source text
source_text = texts.get('source')
if source_text:
    annotations.append(dict(
        text=source_text, x=0.5, y=-0.05, xref='paper', yref='paper',
        xanchor='center', yanchor='top', align='center', showarrow=False,
        font=dict(size=11, family="Arial")
    ))

# Update layout
fig.update_layout(
    showlegend=False,
    font=dict(family="Arial"),
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(l=20, r=20, t=20, b=120),
    annotations=annotations
)

# Generate output filename and save the image
if '.' in json_path:
    output_filename = json_path.rsplit('.', 1)[0] + '.png'
else:
    output_filename = json_path + '.png'

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")