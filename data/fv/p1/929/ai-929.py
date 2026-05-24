import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(sys.argv[0])} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

if not os.path.exists(json_file_path):
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

x_values = [d['x'] for d in chart_data]
y_values = [d['y'] for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker=dict(
        color=colors['bar_colors'],
        line=dict(
            color=colors['bar_border_color'],
            width=1.5
        )
    ),
    hoverinfo='none'
))

annotations = []
if texts.get('note'):
    annotations.append(
        go.layout.Annotation(
            text=texts['note'],
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.38,
            xanchor='left',
            yanchor='top'
        )
    )

fig.update_layout(
    title=dict(
        text=texts['title'],
        x=0.5,
        y=0.95,
        xanchor='center',
        yanchor='top'
    ),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        tickangle=-45,
        showgrid=False,
        showline=True,
        linecolor='black'
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        tickformat='.1%',
        range=[0, 0.08],
        dtick=0.01,
        gridcolor=colors['grid_color'],
        showline=True,
        linecolor='black'
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor=colors['plot_bgcolor'],
    paper_bgcolor=colors['paper_bgcolor'],
    showlegend=False,
    margin=dict(l=120, r=20, t=100, b=180),
    annotations=annotations
)

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")