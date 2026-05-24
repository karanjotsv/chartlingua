import sys
import json
import plotly.graph_objects as go
import pathlib

# Load data from JSON file provided as a command-line argument
json_filepath = pathlib.Path(sys.argv[1])
with open(json_filepath, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for plotting
data_series = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']
categories = data_series[0]['x']

# Create the figure
fig = go.Figure()

# Add traces for each data series, preserving the order from the JSON file
for i, series in enumerate(data_series):
    # Format text labels to be bold and display one decimal place only if it's not .0
    text_labels = [f"<b>{y:.1f}%</b>".replace('.0%', '%') for y in series['y']]
    
    fig.add_trace(go.Bar(
        name=series['name'],
        x=series['x'],
        y=series['y'],
        marker_color=colors[i],
        text=text_labels,
        textposition='inside',
        textfont=dict(color='white', size=12),
        insidetextanchor='middle'
    ))

# Combine title and subtitle if they exist
title_text = ""
if texts.get("title"):
    title_text += f"<b>{texts['title']}</b>"
if texts.get("subtitle"):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Update layout for a professional appearance similar to the original image
fig.update_layout(
    barmode='stack',
    title_text=title_text,
    title_x=0.5,
    font=dict(
        family="Arial",
        size=12
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickmode='array',
        tickvals=categories,
        showgrid=False,
        linecolor='lightgray'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 125],
        tickvals=[0, 25, 50, 75, 100, 125],
        ticksuffix='%',
        showgrid=True,
        gridcolor='lightgray'
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="center",
        x=0.5
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=80, r=40, t=50, b=120)
)

# Add source annotation if it exists
if texts.get("source"):
    fig.add_annotation(
        text=texts['source'],
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1.0,
        y=-0.25,
        font=dict(size=10, color="gray")
    )

# Generate the output PNG filename from the input JSON filename stem
output_filename = json_filepath.stem + ".png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")