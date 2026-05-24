import sys
import json
import os
import plotly.graph_objects as go

# Check if a file path is provided
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

# Get the file path from the command line arguments
json_file_path = sys.argv[1]

# Check if the file exists
if not os.path.exists(json_file_path):
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON in {json_file_path}")
    sys.exit(1)

# Create the figure
fig = go.Figure()

# Add traces for each data series
for i, series in enumerate(chart_data['chart_data']):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        mode='lines+markers',
        name=series.get('name', ''),
        line=dict(color=chart_data['colors'][i], width=2),
        marker=dict(color=chart_data['colors'][i], size=6)
    ))

# Add data labels as annotations
if 'annotations' in chart_data and 'data_labels' in chart_data['annotations']:
    for ann in chart_data['annotations']['data_labels']:
        series_color = chart_data['colors'][ann['series_index']]
        fig.add_annotation(
            x=ann['x'],
            y=ann['y'],
            text=ann['text'],
            showarrow=False,
            font=dict(
                family="Arial",
                size=12,
                color=series_color
            ),
            yshift=ann.get('y_offset', 0),
            xshift=ann.get('x_offset', 0)
        )

# Add legend-like labels as annotations
if 'annotations' in chart_data and 'legend_labels' in chart_data['annotations']:
    for ann in chart_data['annotations']['legend_labels']:
        fig.add_annotation(
            x=ann['x'],
            y=ann['y'],
            text=ann['text'],
            showarrow=False,
            xanchor='left',
            yanchor='top',
            align=ann.get('align', 'left'),
            font=dict(
                family="Arial",
                size=13,
                color=ann['color']
            )
        )

# Update layout
texts = chart_data['texts']
title_text = f"<b>{texts['title']}</b>" if texts.get('title') else ""

fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.05,
        xanchor='left',
        yanchor='top',
        font=dict(size=20)
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font_family="Arial",
    showlegend=False,
    xaxis=dict(
        showline=True,
        linewidth=1,
        linecolor='black',
        showgrid=False,
        tickmode='array',
        tickvals=[1993, 1999, 2003, 2008, 2011],
        ticktext=[str(y) for y in [1993, 1999, 2003, 2008, 2011]],
        ticks='outside'
    ),
    yaxis=dict(
        visible=False,
        range=[25, 80]
    ),
    margin=dict(l=20, r=20, t=80, b=80),
)

# Add source annotation
if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        xref="paper",
        yref="paper",
        x=0,
        y=-0.15,
        showarrow=False,
        align="left",
        xanchor="left",
        font=dict(size=11, color='black')
    )

# Define output filename and save the image
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_path = f"{base_filename}.png"
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")