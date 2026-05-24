import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
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

# Reverse data for top-to-bottom display in a horizontal bar chart
categories = [item['category'] for item in chart_data][::-1]
values = [item['value'] for item in chart_data][::-1]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0], line=dict(width=0)),
    text=[f'<b>{v}</b>' for v in values],
    textposition='inside',
    insidetextanchor='end',
    textfont=dict(
        family='Arial',
        size=16,
        color='white'
    ),
    hoverinfo='none'
))

title_text = f"<b style='font-size:24px;'>{texts['title']}</b>" if texts.get('title') else ""

fig.update_layout(
    title=dict(
        text=title_text,
        x=0,
        y=0.95,
        xanchor='left',
        yanchor='top'
    ),
    font=dict(
        family="Arial"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        visible=False,
        showgrid=False,
        zeroline=False
    ),
    yaxis=dict(
        visible=False,
        showgrid=False,
        zeroline=False
    ),
    showlegend=False,
    margin=dict(l=200, r=20, t=100, b=20),
    bargap=0.3
)

# Use annotations for y-axis labels to control position and alignment
annotations = []
for i, category in enumerate(categories):
    annotations.append(dict(
        xref='paper',
        yref='y',
        x=-0.01,
        y=category,
        xanchor='right',
        text=category,
        font=dict(
            family='Arial',
            size=18,
            color='black'
        ),
        showarrow=False,
        align='right'
    ))

fig.update_layout(annotations=annotations)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2, width=800, height=500)