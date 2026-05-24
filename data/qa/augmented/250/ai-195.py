import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: File not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=values,
    textposition='outside',
    marker_color=colors[0],
    cliponaxis=False,
    texttemplate='%{text}',
    textfont=dict(family="Arial", size=12)
))

title_text = ""
if texts.get('title'):
    title_text += f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    title_text=title_text,
    title_x=0.05,
    title_font_family="Arial",
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12, color='#000000'),
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showline=True,
        linewidth=1,
        linecolor='black',
        tickfont=dict(family="Arial"),
        showgrid=True,
        gridcolor='#F0F0F0',
        gridwidth=1
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showline=False,
        showgrid=True,
        gridwidth=1,
        gridcolor='#E0E0E0',
        range=[0, 105],
        tickfont=dict(family="Arial")
    ),
    margin=dict(l=80, r=40, t=40, b=100),
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref='paper', yref='paper',
            x=0.98, y=-0.2,
            xanchor='right', yanchor='top',
            align='right',
            font=dict(family="Arial", size=10, color='grey')
        )
    ]
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")