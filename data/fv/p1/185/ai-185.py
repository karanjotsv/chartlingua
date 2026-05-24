import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker_colors=colors,
    textposition='outside',
    sort=False,
    direction='clockwise',
    rotation=90,
    domain=dict(x=[0, 0.6]),
    pull=[0] * len(values)
))

title_text = f"<b>{texts.get('title', '')}</b>"

fig.update_layout(
    width=700,
    height=450,
    title_text=title_text,
    title_x=0.3,
    title_font=dict(family="Arial", size=24, color='black'),
    font=dict(family="Arial", size=14, color='black'),
    showlegend=True,
    legend=dict(
        traceorder='normal',
        x=0.65,
        y=0.5,
        xanchor='left',
        yanchor='middle'
    ),
    margin=dict(l=40, r=40, t=80, b=40),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

fig.update_traces(
    texttemplate='%{value:.1f}%',
    textfont_size=14
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")