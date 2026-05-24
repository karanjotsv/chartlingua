import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
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

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

labels = [d['label'] for d in chart_data]
values = [d['value'] for d in chart_data]
text_labels = [f"{d['label']} {d['value']}%" for d in chart_data]

trace = go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#ffffff', width=1)),
    sort=False,
    direction='counterclockwise',
    rotation=-30,
    text=text_labels,
    textinfo='text',
    textposition='outside',
    textfont=dict(family="Arial", size=12, color='#000000'),
    hovertemplate='%{label}: %{value}%<extra></extra>'
)

fig = go.Figure(data=[trace])

annotations = []
if texts.get('source'):
    annotations.append(
        dict(
            text=texts['source'],
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=0,
            xanchor='right',
            yanchor='bottom',
            font=dict(family="Arial", size=10, color="grey")
        )
    )

fig.update_layout(
    font=dict(family="Arial"),
    showlegend=False,
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(l=100, r=100, t=40, b=40),
    annotations=annotations
)

output_filename = json_path.rsplit('.', 1)[0] + '.png'
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")