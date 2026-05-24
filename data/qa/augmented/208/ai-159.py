import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: The file {json_file_path} was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file {json_file_path} is not a valid JSON.")
    sys.exit(1)

data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

categories = [item['category'] for item in data]
values = [item['value'] for item in data]

text_labels = []
for v in values:
    if v == int(v):
        text_labels.append(f'{int(v)}%')
    else:
        text_labels.append(f'{v}%')

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0],
    text=text_labels,
    textposition='outside',
    textfont=dict(family='Arial', size=12, color='black'),
    cliponaxis=False
))

fig.update_layout(
    font=dict(family="Arial", size=12, color="#000000"),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=100),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showgrid=False,
        showline=False,
        ticks='',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        showgrid=True,
        gridcolor='#e6e6e6',
        gridwidth=1,
        showline=False,
        ticks='',
        range=[0, 10.5],
        tickvals=[0, 2, 4, 6, 8, 10],
        ticktext=['0%', '2%', '4%', '6%', '8%', '10%'],
        tickfont=dict(size=12)
    ),
    annotations=[
        dict(
            text=texts['source'],
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.25,
            xanchor='right',
            yanchor='top',
            font=dict(family='Arial', size=12, color='#666666')
        )
    ]
)

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_path = f"{base_filename}.png"
fig.write_image(output_image_path, scale=2)

print(f"Chart generated and saved as {output_image_path}")