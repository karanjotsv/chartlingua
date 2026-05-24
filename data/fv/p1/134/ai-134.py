import sys
import json
from pathlib import Path
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

fig = go.Figure()

# Add data traces from JSON
for series in chart_data['chart_data']:
    name = series['name']
    color = chart_data['colors'].get(name)

    # Add scatter plot for individual data points
    fig.add_trace(go.Scatter(
        x=series['scatter_x'],
        y=series['scatter_y'],
        mode='markers',
        marker=dict(
            color=color,
            size=series['marker_sizes']
        ),
        showlegend=False,
        name=name
    ))

    # Add line plot for the trend
    fig.add_trace(go.Scatter(
        x=series['line_x'],
        y=series['line_y'],
        mode='lines',
        line=dict(
            color=color,
            width=2
        ),
        showlegend=False,
        name='' 
    ))

# Custom legend using annotations
annotations = []
legend_y_start = 0.8
legend_y_step = -0.05
for i, item in enumerate(chart_data['texts']['legend_items']):
    series_name = item['name']
    color = chart_data['colors'].get(series_name)
    y_pos = legend_y_start + i * legend_y_step

    # Add marker symbol
    annotations.append(
        go.layout.Annotation(
            x=0.88,
            y=y_pos,
            xref='paper',
            yref='paper',
            text='•',
            showarrow=False,
            xanchor='left',
            yanchor='middle',
            font=dict(color=color, size=20)
        )
    )
    # Add text label
    annotations.append(
        go.layout.Annotation(
            x=0.9,
            y=y_pos,
            xref='paper',
            yref='paper',
            text=item['text'],
            showarrow=False,
            xanchor='left',
            yanchor='middle',
            font=dict(color='black', size=12)
        )
    )

# Build title and subtitle string
title_text = ''
if chart_data['texts'].get('title'):
    title_text += chart_data['texts']['title']
if chart_data['texts'].get('subtitle'):
    title_text += f"<br><sup>{chart_data['texts']['subtitle']}</sup>"

# Update layout
fig.update_layout(
    template='plotly_white',
    font=dict(family="Arial"),
    title=dict(text=title_text, x=0.05, xanchor='left'),
    width=900,
    height=500,
    margin=dict(l=50, r=50, t=50, b=50),
    xaxis=dict(
        domain=[0, 0.85],
        tickvals=chart_data['axes']['x_tickvals'],
        ticktext=chart_data['axes']['x_ticktext'],
        showgrid=True,
        gridcolor='lightgrey',
        showline=True,
        linecolor='black',
        linewidth=1
    ),
    yaxis=dict(
        range=chart_data['axes']['y_range'],
        dtick=5,
        showgrid=True,
        gridcolor='lightgrey',
        showline=True,
        linecolor='black',
        linewidth=1
    ),
    showlegend=False,
    annotations=annotations
)

output_filename = json_path.stem + ".png"
fig.write_image(output_filename, scale=2)
print(f"Chart saved as {output_filename}")