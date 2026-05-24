import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

fig = go.Figure()

for i, series in enumerate(data):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        mode='lines+markers',
        name=series.get('name', ''),
        line=dict(color=colors[i % len(colors)], width=2.5),
        marker=dict(color=colors[i % len(colors)], size=7)
    ))

title_text = ""
if texts.get('title'):
    title_text += f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

source_note_text = ""
if texts.get('source'):
    source_note_text += texts['source']
if texts.get('note'):
    source_note_text += f"<br>{texts['note']}"

shapes = []
x_vals = data[0]['x']
for i, year in enumerate(x_vals):
    if i % 2 == 1:
        shapes.append(go.layout.Shape(
            type="rect",
            xref="x",
            yref="paper",
            x0=year - 0.5,
            y0=0,
            x1=year + 0.5,
            y1=1,
            fillcolor="#F7F7F7",
            opacity=1,
            layer="below",
            line_width=0,
        ))

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickvals=x_vals,
        tickangle=315,
        showgrid=False,
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        gridcolor='#E5E5E5',
        griddash='dash',
        zeroline=False,
        range=[110, 150.5],
        dtick=5
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(
        family="Arial",
        size=12,
        color="#333333"
    ),
    showlegend=False,
    margin=dict(l=80, r=40, t=60, b=120),
    shapes=shapes
)

if source_note_text:
    fig.add_annotation(
        text=source_note_text,
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1,
        y=-0.28,
        xanchor='right',
        yanchor='top'
    )

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2, width=900, height=550)

print(f"Chart saved to {output_filename}")