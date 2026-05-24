import sys
import json
import plotly.graph_objects as go
import os

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data_full = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = chart_data_full['chart_data']
chart_texts = chart_data_full['texts']
colors = chart_data_full['colors']

fig = go.Figure()

for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        mode='lines+markers',
        line=dict(color=colors[i], width=2),
        marker=dict(color=colors[i], size=6),
        showlegend=False
    ))
    
    # Add direct label annotation
    fig.add_annotation(
        x=series['x'][-1],
        y=series['y'][-1],
        text=series['name'],
        font=dict(color=colors[i], size=12, family="Arial"),
        showarrow=False,
        xanchor='left',
        yanchor='middle',
        xshift=10
    )

title_text = chart_texts['title']
if chart_texts.get('subtitle'):
    title_text += f"<br><sub>{chart_texts['subtitle']}</sub>"

fig.update_layout(
    title=dict(
        text=title_text,
        font=dict(size=22, family="Arial"),
        x=0.05,
        xanchor='left'
    ),
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        title_text=chart_texts['x_axis_title'],
        tickvals=[2011, 2012, 2013, 2014, 2015, 2016],
        ticktext=[str(y) for y in [2011, 2012, 2013, 2014, 2015, 2016]],
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        range=[2010.8, 2017.8]
    ),
    yaxis=dict(
        title_text=chart_texts['y_axis_title'],
        tickvals=[0, 10, 20, 30, 40, 50, 60],
        ticktext=[f"{v}%" for v in [0, 10, 20, 30, 40, 50, 60]],
        gridcolor='#dddddd',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        showline=False,
        range=[0, 75]
    ),
    margin=dict(l=60, r=180, t=100, b=80),
)

# Add source and note annotations
fig.add_annotation(
    text=chart_texts['source'],
    xref="paper", yref="paper",
    x=0, y=-0.15,
    xanchor='left', yanchor='top',
    showarrow=False,
    font=dict(size=12, family="Arial")
)

if chart_texts.get('note'):
    fig.add_annotation(
        text=chart_texts['note'],
        xref="paper", yref="paper",
        x=1, y=-0.15,
        xanchor='right', yanchor='top',
        showarrow=False,
        font=dict(size=12, family="Arial")
    )

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")