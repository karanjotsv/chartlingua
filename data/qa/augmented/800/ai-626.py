import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
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
    textfont=dict(family="Arial", size=12, color='black'),
    texttemplate='%{text}'
))

title_text = ""
if texts.get('title'):
    title_text += f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

source_text = texts.get('source', '')

fig.update_layout(
    title=dict(
        text=title_text if title_text else None,
        x=0.05,
        xanchor='left',
        font=dict(family="Arial")
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        zeroline=False,
        tickfont=dict(family="Arial")
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='#e0e0e0',
        range=[0, 1000],
        dtick=200,
        tickfont=dict(family="Arial"),
        title_font=dict(family="Arial"),
        zeroline=True,
        zerolinecolor='black'
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=90, r=40, t=50, b=100),
    annotations=[
        dict(
            showarrow=False,
            text=source_text,
            xref="paper",
            yref="paper",
            x=1,
            y=-0.2,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(family="Arial", size=12)
        )
    ] if source_text else []
)

base_filename = json_path.split('/')[-1].rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")