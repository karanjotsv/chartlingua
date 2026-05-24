import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=data['x_values'],
    y=data['y_values'],
    mode='lines+markers+text',
    line=dict(color=colors[0], width=2.5),
    marker=dict(color=colors[0], size=8),
    text=data['labels'],
    textposition='top center',
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
))

fig.update_layout(
    font=dict(family="Arial"),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=60, r=40, t=40, b=100),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        tickmode='linear',
        tick0=1999,
        dtick=1,
        tickangle=0,
        tickformat='d',
        showgrid=True,
        gridcolor='#F0F0F0',
        zeroline=False,
        showline=False
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[1.5, 4.1],
        dtick=0.5,
        ticksuffix='%',
        showgrid=True,
        gridcolor='#E5E5E5',
        zeroline=False,
        showline=False
    ),
    annotations=[
        dict(
            xref='paper', yref='paper',
            x=0, y=-0.2,
            xanchor='left', yanchor='top',
            text=texts['note'],
            showarrow=False,
            font=dict(family="Arial", size=12, color='#0073C0')
        ),
        dict(
            xref='paper', yref='paper',
            x=1, y=-0.2,
            xanchor='right', yanchor='top',
            text=texts['source'],
            showarrow=False,
            font=dict(family="Arial", size=12)
        )
    ]
)

base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")