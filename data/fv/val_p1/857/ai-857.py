import sys
import json
import plotly.graph_objects as go
import os

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>", file=sys.stderr)
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}", file=sys.stderr)
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}", file=sys.stderr)
    sys.exit(1)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

fig = go.Figure()

for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        mode='lines',
        line=dict(color=colors[i], width=2),
        showlegend=False
    ))

title_text = f"<span style='font-size: 28px;'><b>{texts['title']}</b></span><br><span style='font-size: 18px;'>{texts['subtitle']}</span>"

fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.01,
        xanchor='left',
        yanchor='top'
    ),
    xaxis_title=dict(text=texts['x_axis_title'], standoff=15, font=dict(size=20)),
    yaxis_title=dict(text=texts['y_axis_title'], standoff=15, font=dict(size=20)),
    font=dict(
        family="Arial",
        size=16,
        color="black"
    ),
    xaxis=dict(
        tickvals=[2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018],
        ticktext=["'06", "'07", "'08", "'09", "'10", "'11", "'12", "'13", "'14", "'15", "'16", "'17", "'18"],
        showgrid=True,
        gridwidth=1,
        gridcolor='#dddddd',
        zeroline=False,
        showline=False,
        range=[2005.8, 2018.8]
    ),
    yaxis=dict(
        range=[-10, 650],
        tick0=0,
        dtick=100,
        showgrid=True,
        gridwidth=1,
        gridcolor='#dddddd',
        zeroline=False,
        showline=False
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=90, r=40, t=120, b=80)
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")