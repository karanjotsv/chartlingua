import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_path = sys.argv[1]
json_path_obj = pathlib.Path(json_path)

# Check if the JSON file exists
if not json_path_obj.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Derive the output filename from the JSON filename
filename_base = json_path_obj.stem

# Load data from JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Initialize figure
fig = go.Figure()

# Add traces from chart_data
for i, series in enumerate(chart_data['chart_data']):
    fig.add_trace(go.Bar(
        x=series['x'],
        y=series['y'],
        text=series['text'],
        name=series.get('name', ''),
        marker_color=chart_data['colors'][i],
        marker_line_color='black',
        marker_line_width=1.5,
        textposition='inside',
        insidetextanchor='middle',
        insidetextfont=dict(
            family="Arial",
            size=24,
            color='black'
        ),
        hoverinfo='none'
    ))

# Build combined title string
texts = chart_data['texts']
title_text = ""
if texts.get('title'):
    title_text += f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    title_text += f"<br>{texts['subtitle']}"

# Update layout
fig.update_layout(
    title_text=title_text,
    font_family="Arial",
    plot_bgcolor='white',
    showlegend=False,
    bargap=0.3,
    margin=dict(t=30, b=40, l=40, r=20),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showticklabels=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        ticks='outside',
        tickcolor='black'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 2.75],
        dtick=0.25,
        showgrid=True,
        gridcolor='#CCCCCC',
        gridwidth=1,
        showline=True,
        linewidth=1,
        linecolor='black',
        ticks='outside',
        tickcolor='black'
    )
)

# Generate output PNG image
output_filename = f"{filename_base}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")