import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0],
    text=values,
    textposition='outside',
    cliponaxis=False,
    texttemplate='%{text:.1f}'
))

fig.update_layout(
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=20, t=40, b=80),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showgrid=False,
        showline=True,
        linecolor='black',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 4.2],
        gridcolor='#E5E5E5',
        showline=False,
        tickfont=dict(size=12)
    ),
    annotations=[
        dict(
            xref="paper",
            yref="paper",
            x=1.0,
            y=-0.2,
            text=texts['source'],
            showarrow=False,
            xanchor='right',
            yanchor='bottom',
            align='right',
            font=dict(size=12)
        )
    ]
)

fig.update_traces(textfont_size=12)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")