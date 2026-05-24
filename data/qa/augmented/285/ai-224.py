import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

if not os.path.exists(json_path):
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories[::-1],
    x=values[::-1],
    orientation='h',
    marker=dict(color=colors[0]),
    name=''
))

fig.update_layout(
    font=dict(family="Arial", size=12, color="#000000"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=120, r=40, t=50, b=100),
    showlegend=False,
    xaxis=dict(
        title_text=texts['x_axis_title'],
        title_standoff=15,
        showgrid=True,
        gridcolor='#EAEAEA',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        showline=False,
        tickvals=[i * 200 for i in range(10)],
        ticktext=[f"{val:,}".replace(",", " ") for val in [i * 200 for i in range(10)]],
        range=[0, 1850]
    ),
    yaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=True,
        ticks=''
    )
)

if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0.98,
        y=-0.15,
        xanchor='right',
        yanchor='top',
        font=dict(size=12, color="#666666")
    )

base_filename = os.path.splitext(json_path)[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")