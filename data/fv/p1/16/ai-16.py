import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

labels = [d['label'] for d in chart_data]
values = [d['value'] for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    hole=0,
    marker=dict(
        colors=colors['slices'],
        line=dict(color='#FFFFFF', width=1) # Add a thin white line between slices
    ),
    textinfo='percent',
    textposition='outside',
    hoverinfo='label+percent',
    sort=False,
    direction='counter-clockwise',
    rotation=0
))

fig.update_traces(
    textfont=dict(
        family="Arial",
        size=14,
        color='black'
    )
)

fig.update_layout(
    title=dict(
        text=texts['title'],
        x=0.5,
        y=0.95,
        xanchor='center',
        yanchor='top',
        font=dict(family="Arial", size=24, color='black')
    ),
    font=dict(
        family="Arial",
        size=12,
        color='black'
    ),
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.15,
        xanchor="center",
        x=0.5,
        font=dict(family="Arial", size=12)
    ),
    paper_bgcolor=colors['background'],
    plot_bgcolor=colors['background'],
    margin=dict(t=120, b=100, l=40, r=40)
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")