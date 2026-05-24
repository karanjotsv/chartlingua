import sys
import json
import pathlib
import plotly.graph_objects as go

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data and text from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: The file {json_path} was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file {json_path} is not a valid JSON file.")
    sys.exit(1)

# Extract data for plotting
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Initialize the figure
fig = go.Figure()

# Add a bar trace for each data series
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        marker_color=colors[i % len(colors)],
        text=series['y'],
        texttemplate='%{text}%',
        textposition='outside',
        textfont=dict(size=12, family="Arial")
    ))

# Combine title and subtitle if they exist
title_text = texts.get('title') or ''
if texts.get('subtitle'):
    title_text += f"<br><sup>{texts.get('subtitle')}</sup>"

# Update layout for a professional look and feel
fig.update_layout(
    barmode='group',
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12, color='black'),
    title=dict(
        text=title_text if title_text else None,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showline=True,
        linewidth=1,
        linecolor='black',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 71],
        ticksuffix='%',
        showgrid=True,
        gridcolor='lightgray',
        zeroline=False,
        tickfont=dict(size=12)
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,  # Position legend below the x-axis
        xanchor="center",
        x=0.5
    ),
    margin=dict(t=50, b=120, l=80, r=40), # Add bottom margin for legend and source
    annotations=[
        dict(
            showarrow=False,
            text=texts.get('source', ''),
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.35, # Position below the chart area
            xanchor='right',
            yanchor='bottom',
            align='right',
            font=dict(size=10)
        )
    ]
)

# Derive the output filename from the input JSON path
output_path = pathlib.Path(json_path).with_suffix('.png')

# Save the figure as a high-resolution PNG image
fig.write_image(str(output_path), scale=2)

print(f"Chart saved to {output_path}")