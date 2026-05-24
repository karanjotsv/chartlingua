import sys
import json
from pathlib import Path
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

# Read data from JSON file
json_path = Path(sys.argv[1])
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

# Extract data and texts
data_series = chart_info['chart_data'][0]
texts = chart_info['texts']
colors = chart_info['colors']

# Create the figure
fig = go.Figure()

# Add the line trace with markers and text labels
fig.add_trace(go.Scatter(
    x=data_series['x'],
    y=data_series['y'],
    mode='lines+markers+text',
    name=data_series.get('name', ''),
    line=dict(color=colors[0], width=2.5),
    marker=dict(color=colors[0], size=8),
    text=[str(val) for val in data_series['y']],
    textposition='top center',
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
))

# Configure the layout
fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    title_text=None,
    yaxis_title=texts['y_axis_title'],
    xaxis_title=texts.get('x_axis_title'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=80),
    xaxis=dict(
        showline=False,
        showgrid=False,
        tickmode='array',
        tickvals=data_series['x'],
        ticktext=[str(year) for year in data_series['x']],
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        showline=False,
        showgrid=True,
        gridcolor='#EAEAEA',
        gridwidth=1,
        range=[757.5, 779],
        dtick=2.5,
        tickfont=dict(size=12)
    )
)

# Add source annotation
fig.add_annotation(
    text=texts.get('source', ''),
    align='left',
    showarrow=False,
    xref='paper',
    yref='paper',
    x=0.98,
    y=-0.12,
    xanchor='right',
    yanchor='top',
    font=dict(size=12)
)

# Generate and save the output image
output_filename = json_path.stem + ".png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")