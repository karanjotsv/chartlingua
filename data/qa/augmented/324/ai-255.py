import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

fig = go.Figure()

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else None,
    name=''
))

title_parts = []
if texts.get('title'):
    title_parts.append(f"<b>{texts['title']}</b>")
if texts.get('subtitle'):
    title_parts.append(f"<span style='font-size: 14px;'>{texts['subtitle']}</span>")
full_title = "<br>".join(title_parts)

fig.update_layout(
    title_text=full_title,
    title_x=0.05,
    title_xanchor='left',
    font_family="Arial",
    plot_bgcolor='white',
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=False,
        tickfont=dict(size=12),
        categoryorder='array',
        categoryarray=categories
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 1200],
        tickvals=[0, 200, 400, 600, 800, 1000, 1200],
        gridcolor='#e0e0e0',
        griddash='dot',
        showline=False,
        zeroline=False,
        tickfont=dict(size=12)
    ),
    showlegend=False,
    margin=dict(l=80, r=40, t=80, b=120)
)

source_parts = []
if texts.get('source'):
    source_parts.append(texts['source'])
if texts.get('note'):
    source_parts.append(texts['note'])
full_source_note = "<br>".join(source_parts)

if full_source_note:
    fig.add_annotation(
        text=full_source_note,
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0,
        y=-0.2, # Adjusted for potential long text
        xanchor='left',
        yanchor='top'
    )
    
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")