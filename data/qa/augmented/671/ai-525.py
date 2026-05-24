import sys
import json
import plotly.graph_objects as go
import pathlib

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line arguments
json_path = sys.argv[1]

# Read and load the JSON file, ensuring UTF-8 encoding for multilingual support
with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Extract data, texts, and colors from the loaded JSON object
chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']
series_names = texts['legend_labels']

# Prepare data for Plotly traces
categories = [d['category'] for d in chart_data]
series_data = {name: [d.get(name) for d in chart_data] for name in series_names}

# Initialize a Plotly Figure
fig = go.Figure()

# Iterate through the series names from the JSON to create a bar trace for each
for i, name in enumerate(series_names):
    fig.add_trace(go.Bar(
        x=categories,
        y=series_data[name],
        name=name,
        marker_color=colors[i],
        text=series_data[name],
        textposition='outside',
        texttemplate='%{text:,.0f}'.replace(',', ' '), # Use space as separator
        cliponaxis=False,
        textfont=dict(
            family="Arial",
            size=11,
            color='black'
        )
    ))

# Construct the title string, handling null values
title_text = texts.get('title') or ''
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Update the figure layout with styles and text from the JSON
fig.update_layout(
    barmode='group',
    plot_bgcolor='white',
    font=dict(family="Arial", size=12, color='black'),
    title=dict(text=title_text, x=0.01, y=0.95, xanchor='left', yanchor='top'),
    xaxis=dict(
        title=texts['x_axis_title'],
        showgrid=False,
        linecolor='black',
        zeroline=False,
        tickangle=0
    ),
    yaxis=dict(
        title=texts['y_axis_title'],
        range=[-5000, 20000],
        dtick=5000,
        tickformat=" ",
        gridcolor='#e0e0e0',
        linecolor='black',
        zeroline=True,
        zerolinecolor='black'
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=80, r=40, b=150, t=50)
)

# Add the source text as a layout annotation for precise positioning
fig.add_annotation(
    showarrow=False,
    text=texts['source'],
    xref="paper",
    yref="paper",
    x=1.0,
    y=-0.37,
    xanchor='right',
    yanchor='bottom',
    align='right',
    font=dict(family="Arial", size=12)
)

# Derive the output filename from the input JSON filename
base_filename = pathlib.Path(json_path).stem
output_filename = f"{base_filename}.png"

# Write the figure to a high-resolution PNG image file
fig.write_image(output_filename, scale=2)

# Print a confirmation message to standard output
print(f"Chart saved to {output_filename}")