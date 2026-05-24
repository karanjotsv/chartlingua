import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <json_file_path>")
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

data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']
categories = data['categories']
series = data['series']

fig = go.Figure()

for i, s in enumerate(series):
    fig.add_trace(go.Bar(
        x=categories,
        y=s['data'],
        name=s['name'],
        marker_color=colors[i],
        texttemplate='%{y}%',
        textposition='outside',
        textfont=dict(family='Arial', size=14, color='black'),
        hoverinfo='none'
    ))

fig.update_layout(
    barmode='group',
    plot_bgcolor='white',
    font=dict(family='Arial', size=12, color='black'),
    yaxis=dict(
        title=texts['y_axis_title'],
        range=[0, 105],
        showgrid=True,
        gridcolor='#E5E5E5',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        showline=False,
        ticksuffix='%',
        tickfont=dict(size=12)
    ),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        tickfont=dict(size=12),
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        zeroline=False
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.25,
        xanchor='center',
        x=0.5,
        font=dict(size=14)
    ),
    margin=dict(l=60, r=40, t=40, b=150),
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.99,
            y=-0.4,
            xanchor='right',
            yanchor='bottom',
            align='right',
            font=dict(family='Arial', size=12, color='grey')
        )
    ]
)

base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")