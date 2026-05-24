import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

x_values = [item['x'] for item in chart_data]
y_values = [item['y'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=x_values,
    y=y_values,
    mode='lines+markers+text',
    line=dict(color=colors[0], width=3),
    marker=dict(color=colors[0], size=8),
    text=[f'<b>{y}</b>' for y in y_values],
    textposition='top center',
    textfont=dict(
        family="Arial",
        size=14,
        color='black'
    ),
    hoverinfo='none'
))

title_text = texts.get('title') or ''
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

annotations = []
if texts.get('source_left'):
    annotations.append(dict(
        xref='paper', yref='paper',
        x=0, y=-0.15,
        xanchor='left', yanchor='top',
        text=f"<span style='color:#0073e5;'>{texts['source_left']}</span>",
        showarrow=False,
        font=dict(family="Arial", size=12)
    ))

if texts.get('source_right'):
    source_right_text = texts['source_right'].replace('© Statista 2021', "<span style='color:#666666;'>© Statista 2021</span>").replace('Show source', "<span style='color:#0073e5;'>Show source</span>")
    annotations.append(dict(
        xref='paper', yref='paper',
        x=1, y=-0.15,
        xanchor='right', yanchor='top',
        text=source_right_text,
        align='right',
        showarrow=False,
        font=dict(family="Arial", size=12)
    ))

fig.update_layout(
    font=dict(family="Arial", size=12),
    title_text=title_text,
    title_x=0.05,
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=[3.2, 3.95],
        tickmode='linear',
        tick0=3.2,
        dtick=0.1,
        gridcolor='#EAEAEA',
        zeroline=False
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        tickmode='array',
        tickvals=x_values,
        gridcolor='#FFFFFF',
        zeroline=False
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=90, r=40, t=50, b=120),
    annotations=annotations
)

output_path = pathlib.Path(json_path).with_suffix(".png")
fig.write_image(str(output_path), scale=2)

print(f"Chart saved to {output_path}")