import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>", file=sys.stderr)
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}", file=sys.stderr)
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}", file=sys.stderr)
    sys.exit(1)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

x_values = [item['x'] for item in chart_data]
y_values = [item['y'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    text=[f'{y:g}' for y in y_values],
    textposition='outside',
    marker_color=colors[0],
    cliponaxis=False
))

title_text = ""
if texts.get('title'):
    title_text += texts['title']
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    title={
        'text': title_text if title_text else None,
        'x': 0.05,
        'xanchor': 'left',
        'yanchor': 'top',
        'y': 0.95
    },
    yaxis_title=texts.get('y_axis_title'),
    xaxis_title=texts.get('x_axis_title'),
    font=dict(family="Arial", size=12),
    showlegend=False,
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=80, r=40, t=60, b=120),
    xaxis=dict(
        showgrid=False,
        linecolor='black',
        ticks='outside',
        ticklen=5
    ),
    yaxis=dict(
        range=[0, 21],
        dtick=2.5,
        gridcolor='#e0e0e0',
        zeroline=False
    ),
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.22,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=10, color='grey')
        )
    ]
)

fig.update_traces(textfont_size=12, textfont_color='black')

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")