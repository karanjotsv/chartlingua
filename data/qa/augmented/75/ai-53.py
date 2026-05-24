import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

x_values = [d['x'] for d in chart_data]
y_values = [d['y'] for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=x_values,
    y=y_values,
    mode='lines+markers+text',
    line=dict(color=colors[0], width=2.5),
    marker=dict(color=colors[0], size=8),
    text=[f'{y:.2f}' if y != 125.8 else '125.8' for y in y_values], # Handle formatting for single decimal point case
    textposition='top center',
    textfont=dict(family="Arial", size=12, color='#333333'),
    hoverinfo='none',
    showlegend=False
))

# Combine title and subtitle if they exist
title_text = ""
if texts.get("title"):
    title_text += texts["title"]
if texts.get("subtitle"):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    title=dict(text=title_text, x=0.05, xanchor='left'),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=False,
        zeroline=False,
        tickfont=dict(color='#666666'),
        fixedrange=True
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='#E5E5E5',
        gridwidth=1,
        showline=False,
        zeroline=False,
        tickfont=dict(color='#666666'),
        range=[116, 128.5],
        tickmode='linear',
        tick0=116,
        dtick=2,
        fixedrange=True
    ),
    margin=dict(l=90, r=40, t=50, b=80),
    annotations=[
        dict(
            text=texts.get('source', ''),
            xref="paper", yref="paper",
            x=0.99, y=-0.15,
            xanchor='right', yanchor='top',
            showarrow=False,
            font=dict(size=12, color="#666666")
        )
    ]
)

output_filename = json_path.with_suffix('.png')
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")