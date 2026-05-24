import sys
import json
import plotly.graph_objects as go
import os

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)

data = chart_config['chart_data']
texts = chart_config['texts']
colors = chart_config['colors']

x_values = [d['x'] for d in data]
y_values = [d['y'] for d in data]

fig = go.Figure()

bar_texts = [f'{y:,}'.replace(',', ' ') for y in y_values]

fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0],
    text=bar_texts,
    textposition='outside',
    texttemplate='%{text}',
    cliponaxis=False,
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
))

y_axis_max = 600000
fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12, color='black'),
    margin=dict(l=80, r=40, t=40, b=100),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        showgrid=True,
        gridcolor='#E0E0E0',
        griddash='dot',
        range=[0, y_axis_max],
        tickvals=[val for val in range(100000, y_axis_max + 1, 100000)],
        ticktext=[f'{val:,}'.replace(',', ' ') for val in range(100000, y_axis_max + 1, 100000)]
    ),
    showlegend=False,
    annotations=[
        dict(
            xref='paper', yref='paper',
            x=0, y=-0.2,
            xanchor='left', yanchor='bottom',
            text=f"ⓘ {texts['additional_info']}" if texts.get('additional_info') else "",
            showarrow=False,
            font=dict(color='#0073B2', size=12)
        ),
        dict(
            xref='paper', yref='paper',
            x=1, y=-0.2,
            xanchor='right', yanchor='bottom',
            text=texts['source'],
            showarrow=False,
            font=dict(size=12)
        )
    ]
)

output_filename_base = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_path = f"{output_filename_base}.png"
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")