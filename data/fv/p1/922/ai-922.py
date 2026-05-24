import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors,
    marker_line=dict(width=1, color='black'),
    text=values,
    textposition='outside',
    textfont=dict(family="Arial", size=10, color='black'),
    cliponaxis=False,
    hoverinfo='none'
))

title_text = texts.get('title') if texts.get('title') else ''
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

fig.update_layout(
    plot_bgcolor='#E0D9EF',
    paper_bgcolor='#E0D9EF',
    font=dict(family="Arial", color='black'),
    title=dict(text=title_text, x=0.05, xanchor='left'),
    showlegend=False,
    xaxis=dict(
        tickfont=dict(size=12),
        showgrid=False,
        title_text=texts.get('x_axis_title')
    ),
    yaxis=dict(
        range=[0, 1650],
        tickvals=[i for i in range(0, 1601, 100)],
        showgrid=True,
        gridcolor='black',
        gridwidth=0.5,
        zeroline=True,
        zerolinewidth=1,
        zerolinecolor='black',
        title_text=texts.get('y_axis_title')
    ),
    margin=dict(l=50, r=20, t=50, b=80),
    bargap=0.15
)

if texts.get('source'):
    fig.add_annotation(
        text=texts.get('source'),
        xref="paper", yref="paper",
        x=0, y=-0.15,
        showarrow=False,
        xanchor='left', yanchor='top',
        align='left',
        font=dict(family="Arial", size=10)
    )

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")