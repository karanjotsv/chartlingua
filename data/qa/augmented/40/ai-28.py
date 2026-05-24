import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
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

x_values = [d['category'] for d in chart_data]
y_values = [d['value'] for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0],
    text=y_values,
    textposition='outside',
    cliponaxis=False,
    texttemplate='%{y}',
    textfont=dict(family="Arial", size=12, color='black')
))

title_text = ""
if texts.get('title'):
    title_text += f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    if title_text:
        title_text += "<br>"
    title_text += texts['subtitle']

fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    font=dict(family="Arial", size=12, color="black"),
    title=dict(text=title_text, x=0.05, xanchor='left'),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showline=True,
        linecolor='black',
        linewidth=1,
        showgrid=False,
        ticks='outside'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 6000],
        tickmode='linear',
        tick0=0,
        dtick=1000,
        showgrid=True,
        gridcolor='lightgray',
        griddash='dot',
        gridwidth=1,
        showline=False,
        ticks=''
    ),
    margin=dict(l=80, r=40, b=80, t=50)
)

if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        xref="paper",
        yref="paper",
        x=0.99,
        y=-0.15,
        showarrow=False,
        xanchor='right',
        yanchor='top',
        font=dict(family="Arial", size=12, color="grey")
    )

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")