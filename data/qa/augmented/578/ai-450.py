import sys
import json
import plotly.graph_objects as go
from pathlib import Path

if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]
if not Path(json_path).is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

output_filename = f"{Path(json_path).stem}.png"

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

bar_text_labels = [f"{v:,.2f}".replace(",", " ") for v in values]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=bar_text_labels,
    textposition='outside',
    marker_color=colors[0],
    hoverinfo='none',
    cliponaxis=False,
    textfont=dict(
        family="Arial",
        size=12
    )
))

y_axis_tickvals = [0, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000]
y_axis_ticktext = [f"{v:,}".replace(",", " ") for v in y_axis_tickvals]

fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=20, t=50, b=80),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=False,
        ticks='',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 4100],
        gridcolor='#E5E5E5',
        showline=False,
        zeroline=False,
        tickvals=y_axis_tickvals,
        ticktext=y_axis_ticktext,
        tickfont=dict(size=12)
    ),
)

if texts.get('source'):
    fig.add_annotation(
        showarrow=False,
        text=texts['source'],
        xref="paper",
        yref="paper",
        x=0.99,
        y=-0.15,
        xanchor='right',
        yanchor='top',
        align='right',
        font=dict(size=12, color='#666666')
    )

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")