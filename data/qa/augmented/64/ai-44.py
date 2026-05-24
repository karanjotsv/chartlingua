import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: File not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

categories = [item['category'] for item in data]
values = [item['value'] for item in data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0],
    text=values,
    textposition='outside',
    textfont=dict(
        family="Arial",
        size=14,
        color='black'
    ),
    cliponaxis=False
))

fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    title=dict(
        text= f"<b>{texts['title']}</b>" if texts.get('title') else "",
        x=0.05,
        xanchor='left'
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 30],
        tickmode='linear',
        tick0=0,
        dtick=5,
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        showline=False
    ),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        tickfont=dict(size=12)
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=90, r=30, t=30, b=100),
    showlegend=False,
    bargap=0.5
)

if texts.get('source'):
    fig.add_annotation(
        xref="paper", yref="paper",
        x=0.99, y=-0.18,
        xanchor='right', yanchor='top',
        text=texts['source'],
        showarrow=False,
        font=dict(family="Arial", size=11, color="#666666")
    )

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")