import sys
import json
import plotly.graph_objects as go
import os

if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

categories = [item['category'] for item in data]
values = [item['value'] for item in data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0],
    text=values,
    texttemplate='%{y}%',
    textposition='auto',
    insidetextanchor='end'
))

fig.update_traces(
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
)

fig.update_layout(
    font=dict(family="Arial"),
    title=dict(
        text=(f"<b>{texts['title']}</b><br>{texts['subtitle']}" if texts.get('title') and texts.get('subtitle')
              else f"<b>{texts['title']}</b>" if texts.get('title')
              else texts.get('subtitle') or ''),
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 105],
        tickvals=[0, 20, 40, 60, 80, 100],
        ticksuffix='%',
        showgrid=True,
        gridcolor='#E5E5E5',
        gridwidth=1,
        zeroline=False,
        tickfont=dict(size=12)
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=60, b=120),
    annotations=[
        dict(
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.2,
            text=texts.get('source', ''),
            showarrow=False,
            xanchor='right',
            yanchor='bottom',
            align='right',
            font=dict(size=12)
        )
    ]
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")