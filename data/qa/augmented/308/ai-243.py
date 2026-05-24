import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {pathlib.Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

x_values = [d['x'] for d in chart_data]
y_values = [d['y'] for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    text=y_values,
    textposition='outside',
    marker_color=colors[0] if colors else None,
    cliponaxis=False,
    textfont=dict(family="Arial", size=12)
))

title_text = texts.get('title')
subtitle_text = texts.get('subtitle')
full_title = ""
if title_text:
    full_title += f"<b>{title_text}</b>"
if subtitle_text:
    full_title += f"<br><sub>{subtitle_text}</sub>"

source_text = texts.get('source', '')

fig.update_layout(
    title_text=full_title,
    title_x=0.05,
    title_font=dict(family="Arial"),
    plot_bgcolor='white',
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickmode='array',
        tickvals=x_values,
        ticktext=[str(x) for x in x_values],
        tickangle=-45,
        showgrid=False,
        linecolor='lightgray'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 500],
        tick0=0,
        dtick=100,
        showgrid=True,
        gridcolor='lightgray',
        gridwidth=1
    ),
    font=dict(family="Arial", size=12),
    margin=dict(l=80, r=40, t=50, b=120),
    showlegend=False,
    annotations=[
        dict(
            text=source_text,
            showarrow=False,
            xref='paper', yref='paper',
            x=1, y=-0.25,
            xanchor='right', yanchor='bottom',
            align='right',
            font=dict(family="Arial", size=10)
        )
    ]
)

output_filename = json_path.stem + ".png"
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")