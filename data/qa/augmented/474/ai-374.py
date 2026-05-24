import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

x_values = [d['x'] for d in data]
y_values = [d['y'] for d in data]
text_labels = [d['text'] for d in data]

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=x_values,
    y=y_values,
    mode='lines+markers+text',
    line=dict(color=colors[0], width=2.5),
    marker=dict(color=colors[0], size=7),
    text=text_labels,
    textposition='top center',
    textfont=dict(
        family="Arial",
        size=11,
        color='black'
    ),
    hoverinfo='none'
))

fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='#f8f9fa',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickvals=x_values,
        ticktext=[str(x) for x in x_values],
        tickangle=-45,
        showgrid=True,
        gridcolor='#f0f0f0',
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[100, 350],
        dtick=50,
        showgrid=True,
        gridcolor='#e0e0e0',
        zeroline=False
    ),
    margin=dict(l=90, r=40, t=40, b=120),
    annotations=[
        dict(
            xref='paper', yref='paper',
            x=0.99, y=-0.32,
            xanchor='right', yanchor='bottom',
            text=f"{texts.get('source', '')}<br>{texts.get('note', '')}",
            showarrow=False,
            align='right',
            font=dict(size=12)
        )
    ]
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_path = f"{base_filename}.png"
fig.write_image(output_path, scale=2)

print(f"Chart saved to {output_path}")