import sys
import json
import os
import plotly.graph_objects as go

# Check if the correct number of arguments is provided
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Derive the output filename from the input JSON filename
output_base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{output_base_name}.png"

# Load all data and text from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in '{json_path}'")
    sys.exit(1)

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Initialize the figure
fig = go.Figure()

# Add a trace for each data series from the JSON
for i, series in enumerate(chart_data):
    color = colors[i % len(colors)]
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        name=series.get('name', ''),
        mode='lines+markers',
        line=dict(color=color, width=2),
        marker=dict(color=color, size=5),
        showlegend=False
    ))
    
    # Add direct labels next to the end of each line
    fig.add_annotation(
        x=series['x'][-1],
        y=series['y'][-1],
        text=f"<span style='font-size: 16px; color:{color};'>●</span> {series['name']}",
        showarrow=False,
        xanchor='left',
        yanchor='middle',
        xshift=8,
        font=dict(
            family="Arial",
            size=12,
            color='#333333'
        )
    )

# Combine title and subtitle using HTML for styling
title_text = f"<b>{texts.get('title', '')}</b><br><span style='font-size: 16px; color: #555555;'>{texts.get('subtitle', '')}</span>"

# Configure the layout of the chart
fig.update_layout(
    font_family="Arial",
    title=dict(
        text=title_text,
        x=0.01,
        y=0.98,
        xanchor='left',
        yanchor='top',
        font=dict(size=20)
    ),
    xaxis=dict(
        tickmode='array',
        tickvals=[1999, 2000, 2001, 2002, 2003],
        showgrid=False,
        zeroline=False,
        linecolor='lightgrey',
        ticks='outside'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        tickformat='.0%',
        range=[0, 0.14],
        tickvals=[0, 0.02, 0.04, 0.06, 0.08, 0.10, 0.12],
        gridcolor='#e0e0e0',
        griddash='dash',
        gridwidth=1,
        zeroline=False,
        linecolor='lightgrey',
        ticks='outside'
    ),
    plot_bgcolor='white',
    margin=dict(l=60, r=130, t=140, b=80),
    height=600,
    width=900
)

# Add source and note as annotations at the bottom of the chart
fig.add_annotation(
    x=0,
    y=-0.12,
    xref='paper',
    yref='paper',
    text=texts.get('source', ''),
    showarrow=False,
    xanchor='left',
    yanchor='top',
    align='left',
    font=dict(size=12, color='#555555')
)

fig.add_annotation(
    x=1,
    y=-0.12,
    xref='paper',
    yref='paper',
    text=texts.get('note', ''),
    showarrow=False,
    xanchor='right',
    yanchor='top',
    align='right',
    font=dict(size=12, color='#555555')
)

# Generate the PNG image file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")