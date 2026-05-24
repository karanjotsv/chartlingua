import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script.py> <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]
output_image_path = json_file_path.rsplit('.', 1)[0] + '.png'

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

categories = [item['category'] for item in data][::-1]
values = [item['value'] for item in data][::-1]

text_labels = []
for v in values:
    if v == int(v):
        text_labels.append(f'{int(v)}%')
    else:
        text_labels.append(f'{v}%')

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=text_labels,
    textposition='outside',
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    ),
    cliponaxis=False
))

fig.update_layout(
    height=650,
    plot_bgcolor='white',
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    xaxis=dict(
        title=texts['x_axis_label'],
        showgrid=True,
        gridcolor='#EAEAEA',
        gridwidth=1,
        zeroline=False,
        showline=False,
        ticksuffix='%',
        range=[0, max(values) * 1.15]
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False
    ),
    margin=dict(l=120, r=50, t=30, b=80),
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.12,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(
                size=12,
                color='grey'
            )
        )
    ]
)

try:
    fig.write_image(output_image_path, scale=2)
    print(f"Chart saved to {output_image_path}")
except Exception as e:
    print(f"Error writing image file: {e}")
    sys.exit(1)