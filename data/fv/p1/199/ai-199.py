import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

x_values = [str(item['x']) for item in chart_data]
y_values = [item['y'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0],
    name=''
))

title_text = texts['title']
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        font=dict(size=24)
    ),
    xaxis_title=texts['x_axis_title'],
    yaxis_title=texts['y_axis_title'],
    font=dict(
        family="Arial",
        size=14
    ),
    plot_bgcolor='white',
    xaxis=dict(
        type='category',
        showgrid=False,
        linecolor='black',
        mirror=True,
        title_font=dict(size=18),
        tickfont=dict(size=14)
    ),
    yaxis=dict(
        range=[0, 60],
        showgrid=True,
        gridcolor='lightgray',
        linecolor='black',
        mirror=True,
        title_font=dict(size=18),
        tickfont=dict(size=14)
    ),
    margin=dict(l=90, r=40, t=90, b=80),
    showlegend=False
)

base_filename = json_file_path.rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)