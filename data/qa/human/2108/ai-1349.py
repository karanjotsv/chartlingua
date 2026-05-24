import sys
import json
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Load data from JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data from the loaded JSON
chart_data = chart_config.get('chart_data', {})
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])
categories = chart_data.get('categories', [])
series_data = chart_data.get('series', [])

# Initialize Figure
fig = go.Figure()

# Add traces for each data series
for i, series in enumerate(series_data):
    # Format text labels to have space as a thousands separator
    bar_texts = [f"{val:,}".replace(",", " ") for val in series.get('data', [])]
    
    fig.add_trace(go.Bar(
        x=categories,
        y=series.get('data', []),
        name=series.get('name', ''),
        marker_color=colors[i % len(colors)],
        text=bar_texts,
        textposition='outside',
        hoverinfo='none',
        cliponaxis=False
    ))

# Combine title and subtitle if they exist
title_text = texts.get('title')
subtitle_text = texts.get('subtitle')
full_title = ""
if title_text:
    full_title += f"<b>{title_text}</b>"
if subtitle_text:
    if full_title:
        full_title += "<br>"
    full_title += f"<i>{subtitle_text}</i>"

# Update layout
fig.update_layout(
    barmode='group',
    title_text=full_title if full_title else None,
    yaxis_title=texts.get('y_axis_title'),
    xaxis_title=texts.get('x_axis_title'),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='#E0E0E0',
        zeroline=False,
        range=[0, 36000],
        separatethousands=True,
        tickformat=','
    ),
    xaxis=dict(
        showline=True,
        linewidth=1,
        linecolor='black',
        tickfont=dict(size=12)
    ),
    margin=dict(l=80, r=40, t=50, b=120),
    bargap=0.2,
    bargroupgap=0.1
)

# Update traces for consistent text styling
fig.update_traces(
    textfont=dict(family="Arial", size=12, color='black')
)

# Add source annotation
if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0.99,
        y=-0.3,
        xanchor='right',
        yanchor='bottom',
        font=dict(size=10, color='#666666')
    )

# Define output filename and save the image
output_filename_base = json_path.rsplit('.', 1)[0]
output_filename = f"{output_filename_base}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")