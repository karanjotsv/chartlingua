import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

x_data = [d['x'] for d in chart_data]
y_data = [d['y'] for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=x_data,
    y=y_data,
    text=y_data,
    textposition='outside',
    marker_color=colors[0],
    cliponaxis=False,
    textfont=dict(family="Arial", size=12, color='black')
))

source_text = ""
if texts.get('source'):
    source_text += texts['source']
if texts.get('note'):
    if source_text:
        source_text += f"<br>{texts['note']}"
    else:
        source_text = texts['note']

fig.update_layout(
    font_family="Arial",
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickmode='array',
        tickvals=x_data,
        ticktext=[str(x) for x in x_data],
        showgrid=False,
        linecolor='black',
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 35],
        dtick=5,
        gridcolor='#E5E5E5',
        showline=False,
        zeroline=False
    ),
    margin=dict(l=80, r=40, t=40, b=120),
    annotations=[
        dict(
            showarrow=False,
            text=source_text,
            xref="paper", yref="paper",
            x=1, y=-0.25,
            xanchor='right', yanchor='top',
            align='right',
            font=dict(size=12, color='black')
        )
    ]
)

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_path = f"{base_filename}.png"

fig.write_image(output_image_path, scale=2, width=800, height=600)

print(f"Chart saved to {output_image_path}")