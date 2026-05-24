import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts from the config
chart_data = chart_config.get("chart_data", {})
texts = chart_config.get("texts", {})
colors = chart_config.get("colors", [])
categories = chart_data.get("categories", [])
series = chart_data.get("series", [])

# Initialize figure
fig = go.Figure()

# Add traces for each series
for i, s in enumerate(series):
    fig.add_trace(go.Bar(
        x=categories,
        y=s.get("values", []),
        name=s.get("name", ""),
        marker_color=colors[i % len(colors)],
        text=[f'{v}%' for v in s.get("values", [])],
        textposition='auto',
        insidetextanchor='middle',
        textfont=dict(color='white', family='Arial, bold', size=14)
    ))

# Build title string
title_text = texts.get("title", "")
if texts.get("subtitle"):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

# Configure layout
fig.update_layout(
    barmode='stack',
    title=dict(
        text=title_text if title_text else None,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts.get("x_axis_title"),
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    yaxis=dict(
        title_text=texts.get("y_axis_title"),
        range=[0, 125],
        tickvals=[0, 25, 50, 75, 100, 125],
        ticktext=['0%', '25%', '50%', '75%', '100%', '125%'],
        gridcolor='#E0E0E0'
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=80, r=40, t=40, b=120),
    annotations=[]
)

# Add source and note annotations
annotations = []
if texts.get("note"):
    annotations.append(dict(
        xref='paper', yref='paper',
        x=0, y=-0.35,
        xanchor='left', yanchor='bottom',
        text=texts['note'],
        showarrow=False,
        font=dict(size=12, color='#0073e5')
    ))
if texts.get("source"):
    annotations.append(dict(
        xref='paper', yref='paper',
        x=1, y=-0.35,
        xanchor='right', yanchor='bottom',
        text=texts['source'],
        showarrow=False,
        font=dict(size=12)
    ))
fig.update_layout(annotations=annotations)


# Define output filename and save the image
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")