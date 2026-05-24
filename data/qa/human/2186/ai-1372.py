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
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

fig = go.Figure()

for i, s in enumerate(data['series']):
    fig.add_trace(go.Scatter(
        x=data['categories'],
        y=s['data'],
        name=s['name'],
        mode='lines+markers+text',
        line=dict(color=colors[i], width=2.5),
        marker=dict(color=colors[i], size=7),
        text=[f'{y:.1f}' for y in s['data']],
        textposition=s.get('textposition', 'top center'),
        textfont=dict(
            family="Arial",
            size=11,
            color='black'
        ),
        hoverinfo='skip'
    ))

fig.update_layout(
    font_family="Arial",
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    xaxis=dict(
        showgrid=False,
        showline=True,
        linecolor='#D3D3D3',
        linewidth=1,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        range=[25, 31],
        dtick=1,
        showgrid=True,
        gridcolor='#D3D3D3',
        gridwidth=1,
        showline=False,
        tickfont=dict(size=12)
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5,
        font=dict(size=12)
    ),
    margin=dict(l=60, r=40, t=50, b=120),
    showlegend=True
)

if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1.0,
        y=0,
        yshift=-100,
        xanchor='right',
        font=dict(
            family="Arial",
            size=12,
            color="grey"
        )
    )

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")