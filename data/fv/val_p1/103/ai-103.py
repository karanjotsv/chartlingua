import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

if not os.path.exists(json_file_path):
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0],
    name=''
))

title_text = texts['title']
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    title={
        'text': title_text,
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {'size': 22}
    },
    xaxis_title=texts['x_axis_title'],
    yaxis_title=texts['y_axis_title'],
    font=dict(
        family="Arial"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=20, t=80, b=60),
    xaxis=dict(
        type='category',
        showline=True,
        linewidth=1,
        linecolor='grey',
        mirror=True,
        tickfont=dict(size=14),
        title_font=dict(size=16)
    ),
    yaxis=dict(
        range=[0, 20],
        dtick=5,
        showline=True,
        linewidth=1,
        linecolor='grey',
        mirror=True,
        gridcolor='#C0C0C0',
        tickfont=dict(size=14),
        title_font=dict(size=16)
    )
)

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")