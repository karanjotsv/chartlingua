import sys
import json
import plotly.graph_objects as go
import os

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: The file {json_file_path} was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file {json_file_path} is not a valid JSON file.")
    sys.exit(1)

chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

fig = go.Figure()

if chart_data:
    categories = [d['category'] for d in chart_data]
    values = [d['value'] for d in chart_data]
    data_labels_suffix = texts.get('data_labels_suffix', '')
    
    bar_texts = [f"{v}{data_labels_suffix}" for v in values]

    fig.add_trace(go.Bar(
        x=categories,
        y=values,
        text=bar_texts,
        textposition='outside',
        textfont=dict(
            family="Arial",
            size=12,
            color='black'
        ),
        marker_color=colors[0] if colors else None,
        cliponaxis=False # Ensures text outside the plot area is visible
    ))

# Build title and source strings
title_text = texts.get('title')
source_text = texts.get('source')

# Update layout
fig.update_layout(
    title=dict(
        text=title_text if title_text else '',
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showline=True,
        linecolor='black',
        linewidth=1,
        tickfont=dict(family="Arial", size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 12.5],
        tickvals=[0, 2, 4, 6, 8, 10, 12],
        ticksuffix='%',
        showgrid=True,
        gridcolor='#e0e0e0',
        griddash='dot',
        zeroline=False,
        showline=False,
        tickfont=dict(family="Arial", size=12)
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    showlegend=False,
    margin=dict(l=60, r=40, b=80, t=80, pad=4),
    annotations=[
        dict(
            text=source_text if source_text else '',
            showarrow=False,
            xref="paper",
            yref="paper",
            x=1.0,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(
                family="Arial",
                size=12
            )
        )
    ]
)

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")