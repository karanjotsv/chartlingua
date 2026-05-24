import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

data = chart_config['chart_data']
texts = chart_config['texts']
colors = chart_config['colors']

x_values = [item['category'] for item in data]
y_values = [item['value'] for item in data]

bar_texts = [f"{y}%" for y in y_values]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0],
    text=bar_texts,
    textposition='outside',
    cliponaxis=False,
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
))

annotations = []
if texts.get('note'):
    annotations.append(dict(
        xref='paper', yref='paper',
        x=0, y=-0.2,
        xanchor='left', yanchor='top',
        text=texts['note'],
        showarrow=False,
        font=dict(family="Arial", size=12, color="#007bff")
    ))

if texts.get('source'):
    annotations.append(dict(
        xref='paper', yref='paper',
        x=1, y=-0.2,
        xanchor='right', yanchor='top',
        text=texts['source'],
        showarrow=False,
        font=dict(family="Arial", size=12, color="#6c757d")
    ))

y_tickvals = [0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2]
y_ticktext = ['0%', '0.2%', '0.4%', '0.6%', '0.8%', '1%', '1.2%']

fig.update_layout(
    font_family="Arial",
    title_text=texts.get('title'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=40, b=120),
    xaxis=dict(
        showgrid=False,
        showline=True,
        linecolor='black',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 1.25],
        tickvals=y_tickvals,
        ticktext=y_ticktext,
        gridcolor='#e0e0e0',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        showline=False,
        tickfont=dict(size=12)
    ),
    annotations=annotations,
    bargap=0.4
)

base_filename, _ = os.path.splitext(json_path)
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")