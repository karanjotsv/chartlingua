import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = sys.argv[1]

# Read the JSON data
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# Extract data for plotting
categories = [item['category'] for item in chart_data['chart_data']]
values = [item['value'] for item in chart_data['chart_data']]
texts = chart_data['texts']
colors = chart_data['colors']

# Create the plot
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=values,
    y=categories,
    orientation='h',
    marker=dict(color=colors),
    text=[str(v) for v in values],
    textposition='outside',
    textfont=dict(family="Arial", size=12, color='black'),
    cliponaxis=False
))

# Update layout
fig.update_layout(
    title_text=f"<b>{texts['title']}</b><br><span style='font-size: 14px; color: #555555;'>{texts['subtitle']}</span>",
    title_x=0.01,
    title_y=0.97,
    title_xanchor='left',
    title_yanchor='top',
    font=dict(family="Arial", size=12, color='black'),
    xaxis=dict(
        showgrid=True,
        gridcolor='#E5E5E5',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        side='bottom',
        ticks='outside',
        ticklen=5,
        showline=True,
        linecolor='black',
        mirror=True
    ),
    yaxis=dict(
        autorange='reversed',
        showgrid=False,
        zeroline=False,
        ticks='',
        showline=True,
        linecolor='black',
        mirror=True
    ),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=100, r=60, t=140, b=80),
    height=700,
    bargap=0.4
)

# Add source and note annotations
fig.add_annotation(
    text=texts['source'],
    xref="paper", yref="paper",
    x=0, y=-0.12,
    xanchor='left', yanchor='top',
    showarrow=False,
    font=dict(family="Arial", size=12, color='#555555')
)

fig.add_annotation(
    text=texts['note'],
    xref="paper", yref="paper",
    x=1, y=-0.12,
    xanchor='right', yanchor='top',
    showarrow=False,
    font=dict(family="Arial", size=12, color='#555555')
)

# Determine output filename and save the image
output_filename = Path(json_file_path).stem + ".png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")