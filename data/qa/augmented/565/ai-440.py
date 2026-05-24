import sys
import json
import os
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

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0],
    text=[f'{v:,}'.replace(',', ' ') for v in values],
    textposition='outside',
    cliponaxis=False
))

fig.update_layout(
    title_text=texts['title'],
    yaxis_title_text=texts['y_axis_title'],
    xaxis_title_text=texts['x_axis_title'],
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    yaxis=dict(
        range=[0, 3500],
        tickmode='linear',
        tick0=0,
        dtick=500,
        gridcolor='#E5E5E5',
        showline=False,
        zeroline=False,
        tickformat=' '
    ),
    xaxis=dict(
        showgrid=False,
        showline=True,
        linecolor='black',
        ticks='outside',
        tickcolor='black'
    ),
    margin=dict(l=80, r=40, t=60, b=80),
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.98,
            y=-0.18,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=12)
        )
    ]
)

fig.update_traces(
    textfont=dict(family="Arial", size=12, color='black')
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")