import sys
import json
import plotly.graph_objects as go
import os

if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# Prepare data for Plotly
chart_data = chart_config['chart_data']
texts = chart_config['texts']
colors = chart_config['colors']

y_categories = [item['category'] for item in chart_data]
traces = []

for i, series_name in enumerate(texts['legend_items']):
    x_values = [item['values'][i] for item in chart_data]
    traces.append(go.Bar(
        name=series_name,
        y=y_categories,
        x=x_values,
        orientation='h',
        marker=dict(color=colors[i], line=dict(width=0)),
        text=x_values,
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(color='white', size=14, family='Arial'),
        hovertemplate='%{y}: %{x}%<extra></extra>'
    ))

# Create layout
title_text = f"<b>{texts['title']}</b><br><span style='font-style: italic; font-size: 14px;'>{texts['subtitle']}</span>"
footer_text = f"<span style='font-style: italic;'>{texts['note']}</span><br>{texts['source']}<br><b>{texts['footer']}</b>"

layout = go.Layout(
    barmode='stack',
    title=dict(
        text=title_text,
        x=0.01,
        xanchor='left',
        y=0.95,
        yanchor='top',
        font=dict(size=20, family='Arial')
    ),
    xaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=False,
        zeroline=False,
        range=[0, 100.5]
    ),
    yaxis=dict(
        showgrid=False,
        showline=False,
        autorange='reversed',
        tickfont=dict(size=14, family='Arial')
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.01,
        xanchor='left',
        x=0.22,
        traceorder='normal',
        font=dict(size=14, family='Arial'),
        bgcolor='rgba(0,0,0,0)'
    ),
    font=dict(family='Arial'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=220, r=20, t=160, b=120),
    annotations=[
        dict(
            text=footer_text,
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.20,
            xanchor='left',
            yanchor='top',
            align='left',
            font=dict(size=12, color='#555555')
        )
    ]
)

fig = go.Figure(data=traces, layout=layout)

# Generate output filename from JSON path
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")