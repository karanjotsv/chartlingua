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
    print(f"Error: Invalid JSON format in {json_path}")
    sys.exit(1)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', ['#000000'])

fig = go.Figure()

if chart_data:
    x_values = [d['x'] for d in chart_data]
    y_values = [d['y'] for d in chart_data]
    text_labels = [f"{y:.1f}%" for y in y_values]

    fig.add_trace(go.Scatter(
        x=x_values,
        y=y_values,
        mode='lines+markers+text',
        line=dict(color=colors[0], width=2.5),
        marker=dict(color=colors[0], size=7),
        text=text_labels,
        textposition='top center',
        textfont=dict(
            family="Arial",
            size=11,
            color='black'
        )
    ))

title_text = texts.get('title') or ''
if texts.get('subtitle'):
    title_text = f"<b>{title_text}</b><br><sub>{texts.get('subtitle')}</sub>"

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickmode='array',
        tickvals=x_values,
        ticktext=[str(x) for x in x_values],
        tickangle=0,
        showgrid=False,
        zeroline=False,
        linecolor='lightgrey'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[7.5, 13.5],
        tickvals=[8, 9, 10, 11, 12, 13],
        ticktext=[f"{i}%" for i in [8, 9, 10, 11, 12, 13]],
        showgrid=True,
        gridcolor='#EAEAEA',
        zeroline=False,
        linecolor='lightgrey'
    ),
    font=dict(
        family="Arial",
        size=12,
        color="#333333"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=60, b=80),
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.99,
            y=-0.18,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(
                size=10
            )
        )
    ]
)

base_filename, _ = os.path.splitext(json_path)
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")