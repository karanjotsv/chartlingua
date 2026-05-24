import sys
import json
import plotly.graph_objects as go
from pathlib import Path

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Prepare data for Plotly
labels = [d['label'] for d in chart_data['chart_data']]
values = [d['value'] for d in chart_data['chart_data']]

# Create the pie chart
fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=chart_data['colors'], line=dict(color='#000000', width=1)),
    pull=chart_data.get('pull', [0] * len(labels)),
    texttemplate='%{label}<br>%{value:.2f}%',
    textposition='inside',
    insidetextfont=dict(family='Arial', size=20, color='black'),
    hoverinfo='label+percent',
    sort=False,
    direction='clockwise'
)])

# Update layout
fig.update_layout(
    title=dict(
        text=chart_data['texts']['title'],
        y=0.08,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(family='Arial', size=24)
    ),
    showlegend=False,
    font=dict(family='Arial'),
    margin=dict(l=40, r=40, t=40, b=120),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)

# Generate output image file path from input json path
output_path = Path(json_path)
output_filename = output_path.with_suffix('.png').name

# Save the figure
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")