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
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

x_values = [d['category'] for d in chart_data]
y_values = [d['value'] for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0],
    text=y_values,
    textposition='outside',
    texttemplate='<b>%{y}</b>',
    textfont=dict(
        family="Arial",
        size=14,
        color='black'
    ),
    cliponaxis=False
))

fig.update_layout(
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        tickfont=dict(size=12),
        categoryorder='array',
        categoryarray=x_values
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=[0, 80],
        dtick=10,
        gridcolor='#E5E5E5',
        zeroline=False,
        showline=False
    ),
    margin=dict(l=80, r=40, t=40, b=100),
    annotations=[
        dict(
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.22,
            xanchor='left',
            yanchor='top',
            text=f"<span style='color:{colors[0]}; font-size:14px; font-weight:bold;'>ⓘ</span> <span style='color:{colors[0]};'>{texts['source_left']}</span>"
        ),
        dict(
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.22,
            xanchor='right',
            yanchor='top',
            align='right',
            text=f"{texts['source_right_main']}&nbsp;&nbsp;&nbsp;&nbsp;{texts['source_right_link']} <span style='color:{colors[0]}; font-size:14px; font-weight:bold;'>ⓘ</span>"
        )
    ]
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")