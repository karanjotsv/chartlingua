import sys
import json
import plotly.graph_objects as go
import os

if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']
categories = chart_data['categories']
series_data = chart_data['series']

fig = go.Figure()

for i, series in enumerate(series_data):
    fig.add_trace(go.Bar(
        x=categories,
        y=series['values'],
        name=series['name'],
        marker_color=colors[i],
        text=[f'{int(v) if v == int(v) else v}%' for v in series['values']],
        textposition='inside',
        textfont=dict(color='white', family='Arial', size=12, weight='bold'),
        insidetextanchor='middle'
    ))

title_text = ""
if texts.get('title'):
    title_text += f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

annotations = []
if texts.get('note'):
    annotations.append(
        dict(
            xref="paper", yref="paper",
            x=0, y=-0.25,
            xanchor='left', yanchor='top',
            text=texts['note'],
            showarrow=False,
            font=dict(family="Arial", size=12, color="#2481D8")
        )
    )
if texts.get('source'):
    annotations.append(
        dict(
            xref="paper", yref="paper",
            x=1, y=-0.25,
            xanchor='right', yanchor='top',
            text=texts['source'],
            showarrow=False,
            font=dict(family="Arial", size=12, color='grey')
        )
    )

fig.update_layout(
    barmode='stack',
    title=dict(text=title_text, x=0.05, xanchor='left'),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickmode='array',
        tickvals=categories,
        ticktext=[str(c) for c in categories],
        showgrid=False,
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='#e0e0e0',
        range=[0, 125],
        tickvals=[0, 25, 50, 75, 100, 125],
        ticktext=[f'{i}%' for i in [0, 25, 50, 75, 100, 125]],
        zeroline=False
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.15,
        xanchor="center",
        x=0.5
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12),
    margin=dict(l=60, r=40, b=150, t=50),
    annotations=annotations
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")