import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(sys.argv[0])} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

fig = go.Figure()

x_values = [d['year'] for d in chart_data]
y_values = [d['concentration'] for d in chart_data]

fig.add_trace(go.Scatter(
    x=x_values,
    y=y_values,
    mode='lines+markers',
    name=texts['series_name'],
    line=dict(color=colors[0], width=2),
    marker=dict(color=colors[0], size=5),
    showlegend=False
))

title_text = f"<b>{texts['title']}</b><br><span style='font-size: 14px; color: #555555;'>{texts['subtitle']}</span>"

fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.01,
        xanchor='left',
        yanchor='top',
        font=dict(size=22)
    ),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        tickvals=[1840, 1860, 1880, 1900, 1920, 1940, 1960, 1975],
        showgrid=False,
        showline=True,
        linecolor='lightgrey',
        linewidth=1,
        ticks='outside',
        tickcolor='lightgrey'
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        tickvals=[250, 260, 270, 280, 290],
        ticksuffix=' ppb',
        showgrid=True,
        gridcolor='#e5e5e5',
        gridwidth=1,
        griddash='dash',
        showline=False,
        zeroline=False,
        range=[248, 298]
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(
        family="Arial",
        size=12,
        color="#333333"
    ),
    margin=dict(l=70, r=40, t=120, b=100),
    annotations=[
        dict(
            x=x_values[-1],
            y=y_values[-1],
            text=texts['series_name'],
            showarrow=False,
            xanchor='left',
            yanchor='middle',
            xshift=8,
            font=dict(
                size=12,
                color=colors[0]
            )
        ),
        dict(
            x=0,
            y=-0.2,
            xref='paper',
            yref='paper',
            text=texts['source'],
            showarrow=False,
            align='left',
            xanchor='left',
            yanchor='top',
            font=dict(
                size=10,
                color='#7f7f7f'
            )
        )
    ]
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")