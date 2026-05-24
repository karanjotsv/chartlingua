import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

fig = go.Figure()

# Extract data from JSON
x_values = chart_data.get('x_axis', [])
series_data = chart_data.get('chart_data', [])
texts = chart_data.get('texts', {})
colors = chart_data.get('colors', [])

# Add traces for each data series
for i, series in enumerate(series_data):
    fig.add_trace(go.Scatter(
        x=x_values,
        y=series.get('y', []),
        name=series.get('name', ''),
        mode='lines+markers',
        line=dict(color=colors[i % len(colors)], width=2.5),
        marker=dict(color=colors[i % len(colors)], size=7),
        connectgaps=False
    ))

# Build title and source strings
title_text = texts.get('title') or ''
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

source_text = texts.get('source') or ''
if texts.get('note'):
    source_text += f"<br>{texts['note']}"

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickvals=x_values,
        showgrid=False,
        linecolor='black'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 31],
        tickformat=',.0f',
        ticksuffix='%',
        gridcolor='#dddddd'
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=80, r=40, t=60, b=150),
    annotations=[
        dict(
            text=source_text,
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.99,
            y=-0.28,
            xanchor='right',
            yanchor='bottom',
            align='right',
            font=dict(size=10, color="#7f7f7f")
        )
    ]
)

# Generate and save the output image
output_filename_base = pathlib.Path(json_file_path).stem
output_path = f"{output_filename_base}.png"
fig.write_image(output_path, scale=2)

print(f"Chart saved to {output_path}")