import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
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

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

text_labels = []
for v in values:
    if isinstance(v, int) or v == int(v):
        text_labels.append(str(int(v)))
    else:
        text_labels.append(f'{v:.2f}')

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker_color=colors[0] if colors else '#3182CE',
    text=text_labels,
    textposition='outside',
    textfont=dict(family="Arial", size=12, color='black'),
    cliponaxis=False
))

source_text = ""
if texts.get('source'):
    source_text += texts['source']
if texts.get('note'):
    source_text += f"<br>{texts['note']}"

fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#EAEAEA',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        range=[0, 18.5],
        tickmode='linear',
        dtick=2.5
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        showgrid=False,
        autorange='reversed'
    ),
    margin=dict(l=320, r=40, t=30, b=80),
    showlegend=False,
    annotations=[]
)

if source_text:
    fig.add_annotation(
        showarrow=False,
        text=source_text,
        xref="paper",
        yref="paper",
        x=1,
        y=-0.15,
        xanchor='right',
        yanchor='top',
        align='right'
    )

base_name = json_path.split('/')[-1].rsplit('.', 1)[0]
output_filename = f"{base_name}.png"

fig.write_image(output_filename, scale=2, width=800, height=600)

print(f"Chart saved to {output_filename}")