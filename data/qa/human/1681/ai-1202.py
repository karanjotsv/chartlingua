import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

fig = go.Figure()

for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        mode='lines',
        line=dict(color=colors[i], width=2.5),
        showlegend=False
    ))
    fig.add_trace(go.Scatter(
        x=[series['x'][0], series['x'][-1]],
        y=[series['y'][0], series['y'][-1]],
        mode='markers',
        marker=dict(color=colors[i], size=6),
        showlegend=False
    ))

annotations = []
for i, series in enumerate(chart_data):
    annotations.append(
        dict(
            x=series['x'][-1],
            y=series['y'][-1],
            text=series['name'],
            font=dict(family="Arial", size=14, color=colors[i]),
            showarrow=False,
            xanchor='left',
            yanchor='middle',
            xshift=10
        )
    )

title_text = f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    title_text += f"<br><span style='font-size: 14px;'>{texts['subtitle']}</span>"

fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.01,
        xanchor='left',
        yanchor='top',
        font=dict(family="Arial", size=20)
    ),
    xaxis=dict(
        tickvals=chart_data[0]['x'],
        tickmode='array',
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        tickfont=dict(family="Arial", size=12)
    ),
    yaxis=dict(
        range=[0, 95],
        tickvals=[0, 20, 40, 60, 80],
        ticksuffix='%',
        gridcolor='#e0e0e0',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        showline=False,
        tickfont=dict(family="Arial", size=12)
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=50, r=180, t=100, b=80),
    annotations=annotations
)

fig.add_annotation(
    text=texts['source'],
    xref="paper", yref="paper",
    x=0, y=-0.12,
    showarrow=False,
    xanchor='left',
    yanchor='top',
    font=dict(family="Arial", size=12)
)

base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")