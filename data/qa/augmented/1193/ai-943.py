import sys
import json
from pathlib import Path
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <json_file_path>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = Path(sys.argv[1])

# Check if the JSON file exists
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read data from the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data and texts from the loaded JSON
data = chart_data['chart_data']
texts = chart_data['texts']
series_names = chart_data['series_names']
colors = chart_data['colors']
categories = [d['category'] for d in data]

# Create the figure
fig = go.Figure()

# Add traces for each series
for i, series_name in enumerate(series_names):
    y_values = [d['values'][i] for d in data]
    # Format text to match original image (with spaces as thousands separators)
    bar_texts = [f"<b>{value:,}</b>".replace(",", " ") for value in y_values]
    
    fig.add_trace(go.Bar(
        x=categories,
        y=y_values,
        name=series_name,
        marker_color=colors[i],
        text=bar_texts,
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(
            family='Arial',
            size=12,
            color='white'
        )
    ))

# Combine title and subtitle if they exist
title_text = texts.get('title') or ''
if texts.get('subtitle'):
    title_text += f"<br><sup>{texts['subtitle']}</sup>"

# Update layout
fig.update_layout(
    barmode='stack',
    title_text=title_text,
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=80, r=20, t=50, b=120),
    xaxis=dict(
        showline=True,
        linewidth=1,
        linecolor='lightgray',
        ticks='',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        range=[0, 125000],
        tickvals=[0, 25000, 50000, 75000, 100000, 125000],
        showgrid=True,
        gridcolor='lightgray',
        tickfont=dict(size=12),
        tickformat=" " # Use space as thousands separator
    ),
    # Add source annotation
    annotations=[
        dict(
            showarrow=False,
            text=texts.get('source', ''),
            xref="paper",
            yref="paper",
            x=1,
            y=-0.28,
            xanchor='right',
            yanchor='top',
            font=dict(size=12)
        )
    ]
)

# Define output filename and save the image
output_filename = json_file_path.stem + ".png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")