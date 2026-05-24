import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    sys.exit("Usage: python <script_name>.py <json_file_path>")

json_path = sys.argv[1]

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

fig = go.Figure()

for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        mode='lines',
        fill='tozeroy',
        fillcolor=colors[i],
        line=dict(color='black', width=1.5),
        showlegend=False
    ))

title_text = f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        y=0.95,
        xanchor='center',
        yanchor='top',
        font=dict(size=18)
    ),
    font=dict(family="Arial", size=12),
    xaxis=dict(
        tickvals=chart_data[0]['x'],
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        ticks='outside'
    ),
    yaxis=dict(
        range=[0, 60000],
        tickvals=[0, 10000, 20000, 30000, 40000, 50000, 60000],
        ticktext=["0", "10.000", "20.000", "30.000", "40.000", "50.000", "60.000"],
        showgrid=True,
        gridcolor='black',
        gridwidth=1,
        zeroline=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        ticks='outside'
    ),
    plot_bgcolor='white',
    margin=dict(l=70, r=30, t=80, b=80),
)

if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        xref="paper", yref="paper",
        x=0, y=-0.22,
        showarrow=False,
        xanchor='left',
        yanchor='top',
        align='left',
        font=dict(size=12)
    )

base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")