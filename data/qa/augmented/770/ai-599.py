import sys
import json
import plotly.graph_objects as go
from pathlib import Path

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_file_path = Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']
categories = chart_data['categories']
series = chart_data['series']

fig = go.Figure()

for i, s in enumerate(series):
    fig.add_trace(go.Bar(
        x=categories,
        y=s['values'],
        name=s['name'],
        marker_color=colors[i],
        text=s['values'],
        textposition='inside',
        texttemplate="<b>%{text}</b>",
        insidetextanchor='middle',
        textfont=dict(
            family="Arial",
            size=12,
            color='white'
        )
    ))

fig.update_layout(
    barmode='stack',
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    margin=dict(l=80, r=40, b=120, t=40),
    yaxis=dict(
        title=texts['y_axis_title'],
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        zeroline=True,
        zerolinecolor='black',
        zerolinewidth=1,
        range=[0, 2100],
        dtick=500
    ),
    xaxis=dict(
        showgrid=False,
        zeroline=False
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5
    ),
    showlegend=True
)

if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0,
        y=-0.2,
        xanchor='left',
        yanchor='top',
        font=dict(size=10)
    )

output_filename = f"{json_file_path.stem}.png"
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")