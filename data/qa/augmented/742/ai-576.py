import sys
import json
import pathlib
import plotly.graph_objects as go

# Check if a file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = pathlib.Path(sys.argv[1])

# Verify the JSON file exists
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Read and parse the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors from the JSON object
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly trace
x_values = [d['x'] for d in chart_data]
y_values = [d['y'] for d in chart_data]
text_labels = [d.get('label', d['y']) for d in chart_data]

# Create the figure object
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    text=text_labels,
    textposition='outside',
    marker_color=colors[0] if colors else None,
    cliponaxis=False,
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
))

# Build title string from JSON data
title_text = ""
if texts.get("title"):
    title_text += f"<b>{texts.get('title')}</b>"
if texts.get("subtitle"):
    if title_text:
        title_text += "<br>"
    title_text += texts.get("subtitle")

# Update layout for a clean, accurate look
fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    title=dict(
        text=title_text,
        x=0.01,
        y=0.98,
        xanchor='left',
        yanchor='top'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickvals=x_values,
        ticktext=[str(x) for x in x_values],
        showgrid=False,
        linecolor='black',
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 1800],
        tickvals=[0, 250, 500, 750, 1000, 1250, 1500, 1750],
        ticktext=["0", "250", "500", "750", "1 000", "1 250", "1 500", "1 750"],
        gridcolor='#e0e0e0',
        linecolor='black',
        zeroline=False
    ),
    plot_bgcolor='white',
    paper_bgcolor='#ffffff',
    showlegend=False,
    margin=dict(l=80, r=40, t=40, b=120),
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.99,
            y=-0.18, # Positioned below x-axis
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=10)
        )
    ]
)

# Define the output filename based on the input JSON file's name
output_filename = json_file_path.stem + ".png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")