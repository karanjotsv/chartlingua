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
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

fig = go.Figure()

categories = chart_data['chart_data']['categories']
series_data = chart_data['chart_data']['series']
colors = chart_data['colors']
texts = chart_data['texts']

for i, series in enumerate(series_data):
    fig.add_trace(go.Bar(
        x=categories,
        y=series['values'],
        name=series['name'],
        marker_color=colors[i],
        text=[f"{v}%" for v in series['values']],
        textposition='outside',
        textfont=dict(
            family="Arial",
            size=12,
            color='black'
        ),
        hoverinfo='skip'
    ))

title_text = ""
if texts.get('title'):
    title_text += texts['title']
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    barmode='group',
    font=dict(
        family="Arial",
        size=12
    ),
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showline=True,
        linewidth=1,
        linecolor='black',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='lightgray',
        ticksuffix='%',
        range=[0, 85],
        tickfont=dict(size=12)
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5
    ),
    plot_bgcolor='white',
    margin=dict(l=80, r=40, b=120, t=40, pad=4),
    annotations=[
        dict(
            showarrow=False,
            text=texts.get('note', ''),
            xref="paper",
            yref="paper",
            x=0,
            y=-0.35,
            xanchor='left',
            yanchor='bottom',
            font=dict(size=12)
        ),
        dict(
            showarrow=False,
            text=texts.get('source', ''),
            xref="paper",
            yref="paper",
            x=1,
            y=-0.35,
            xanchor='right',
            yanchor='bottom',
            font=dict(size=12)
        )
    ]
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)
print(f"Chart saved as {output_filename}")