import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    sys.exit(1)

json_path = sys.argv[1]
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

fig = go.Figure()

for i, series in enumerate(chart_info['chart_data']):
    color = chart_info['colors'][i]
    
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        mode=series['mode'],
        marker=dict(
            symbol=series.get('marker_symbol'),
            color=color,
            size=8,
            line=dict(color=color, width=1.5)
        ),
        line=dict(
            color=color,
            dash=series.get('line_style'),
            width=1.5
        )
    ))

plot_annotations = []
if chart_info['texts'].get('annotations'):
    for ann in chart_info['texts']['annotations']:
        plot_annotations.append(go.layout.Annotation(
            x=ann['x'],
            y=ann['y'],
            text=ann['text'],
            showarrow=False,
            font=dict(family="Arial", size=12),
            xanchor=ann.get('xanchor', 'left'),
            yanchor=ann.get('yanchor', 'middle'),
            xshift=ann.get('xshift', 0),
            yshift=ann.get('yshift', 0)
        ))

fig.update_layout(
    font=dict(family="Arial"),
    xaxis=dict(
        title=chart_info['texts']['x_axis_title'],
        range=[0, 200],
        tickmode='linear',
        dtick=50,
        showgrid=True,
        gridcolor='lightgrey',
        griddash='dot',
        showline=True,
        linewidth=1,
        linecolor='black',
        ticks='inside',
        mirror=True
    ),
    yaxis=dict(
        title=chart_info['texts']['y_axis_title'],
        range=[0, 300],
        tickmode='linear',
        dtick=50,
        showgrid=True,
        gridcolor='lightgrey',
        griddash='dot',
        showline=True,
        linewidth=1,
        linecolor='black',
        ticks='inside',
        mirror=True
    ),
    plot_bgcolor='white',
    legend=dict(
        x=0.08,
        y=0.92,
        xanchor='left',
        yanchor='top',
        bordercolor='black',
        borderwidth=1
    ),
    annotations=plot_annotations,
    margin=dict(l=70, r=30, t=30, b=60)
)

filename_base = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{filename_base}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")