import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except json.JSONDecodeError as e:
    print(f"Error decoding JSON from '{json_path}': {e}")
    sys.exit(1)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

categories = [d['category'] for d in chart_data]
values = [d['value'] for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=[f'{v:.1f}' for v in values],
    textposition='outside',
    cliponaxis=False,
    marker_color=colors[0] if colors else None,
    hoverinfo='none'
))

title_text = f"<b>{texts.get('title', '')}</b>" if texts.get('title') else ""
if texts.get('subtitle'):
    title_text += f"<br>{texts.get('subtitle')}"

source_text = texts.get('source', '')
if texts.get('note'):
    source_text += f"<br>{texts.get('note', '')}"

shapes = []
for i in range(len(categories) - 1):
    shapes.append(go.layout.Shape(
        type="line",
        xref="x",
        yref="paper",
        x0=i + 0.5,
        y0=0,
        x1=i + 0.5,
        y1=1,
        line=dict(
            color="#F0F0F0",
            width=1,
        )
    ))

fig.update_layout(
    font_family="Arial",
    title=dict(
        text=title_text if title_text else None,
        x=0.01,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='#dddddd',
        zeroline=False,
        range=[0, 15.5],
        tickvals=[0, 2.5, 5, 7.5, 10, 12.5, 15]
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=100),
    shapes=shapes,
    annotations=[
        dict(
            text=source_text,
            showarrow=False,
            xref="paper", yref="paper",
            x=0.99, y=-0.18,
            xanchor='right', yanchor='top',
            align='right',
            font=dict(size=10)
        )
    ]
)

fig.update_traces(textfont_size=12, textfont_color='black')

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")