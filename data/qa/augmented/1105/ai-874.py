import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data for plotting
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']
categories = chart_data['categories']
series = chart_data['series']

# Initialize figure
fig = go.Figure()

# Add bar traces for each series
for i, s in enumerate(series):
    fig.add_trace(go.Bar(
        x=categories,
        y=s['data'],
        name=s['name'],
        marker_color=colors[i],
        hoverinfo='skip'
    ))

# This chart has custom annotations instead of standard bar text
boys_data = series[0]['data']
girls_data = series[1]['data']

# Add annotations for the 'Boys' series (inside the blue bars)
for i, val in enumerate(boys_data):
    fig.add_annotation(
        x=categories[i],
        y=val / 2,
        text=f"{val:,}".replace(",", " "),
        showarrow=False,
        font=dict(family="Arial", size=11, color="white")
    )

# Add annotations for the 'Girls' series (in black boxes above the bars)
for i, val in enumerate(girls_data):
    total_height = boys_data[i] + val
    fig.add_annotation(
        x=categories[i],
        y=total_height,
        text=f"{val:,}".replace(",", " "),
        showarrow=False,
        font=dict(family="Arial", size=11, color="white"),
        bgcolor=colors[1],
        borderpad=2,
        yshift=8
    )

# Update layout
fig.update_layout(
    barmode='stack',
    plot_bgcolor='white',
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showgrid=False,
        linecolor='black',
        ticks=''
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 350000],
        gridcolor='#E5E5E5',
        tickformat=',.0f',
        zeroline=False,
        ticks='outside',
        tickcolor='#d9d9d9'
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=80, r=40, t=40, b=100)
)

# Add source annotation
if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1.0,
        y=-0.22,
        xanchor='right',
        yanchor='bottom'
    )

# Determine output filename and save the image
base_filename = Path(json_path).stem
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")