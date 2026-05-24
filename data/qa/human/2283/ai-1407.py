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
    chart_data = json.load(f)

fig = go.Figure()

categories = chart_data['categories']
data_series = chart_data['chart_data']
colors = chart_data['colors']
text_colors = chart_data['text_colors']
texts = chart_data['texts']

for i, series in enumerate(data_series):
    fig.add_trace(go.Bar(
        x=categories,
        y=series['y'],
        name=series['name'],
        marker_color=colors[i],
        text=series['y'],
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(
            family="Arial",
            color=text_colors[i],
            size=11
        )
    ))

fig.update_layout(
    barmode='stack',
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12, color='black'),
    yaxis=dict(
        title=texts['yaxis_title'],
        range=[0, 2.1],
        showgrid=True,
        gridcolor='#e0e0e0',
        zeroline=False
    ),
    xaxis=dict(
        title=texts['xaxis_title'],
        tickfont=dict(size=11),
        showgrid=False
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5,
        traceorder='normal'
    ),
    margin=dict(l=80, r=40, t=50, b=150),
    annotations=[
        dict(
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.35,
            xanchor='right',
            yanchor='bottom',
            text=texts['source'],
            showarrow=False,
            font=dict(size=12)
        )
    ]
)

output_filename = f"{json_file_path.stem}.png"
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")