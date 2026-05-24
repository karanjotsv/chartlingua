import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
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

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Reverse data for Plotly's bottom-to-top plotting order
categories.reverse()
values.reverse()

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=values,
    textposition='outside',
    texttemplate='%{text}',
    cliponaxis=False,
    hoverinfo='none'
))

fig.update_layout(
    xaxis_title=texts['x_axis_title'],
    yaxis_title=texts['y_axis_title'],
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=160, r=40, t=30, b=80),
    xaxis=dict(
        showgrid=True,
        gridcolor='#EAEAEA',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        showline=False,
        ticks='outside',
        tickcolor='#B0B0B0',
        tickfont=dict(size=11),
        title_font=dict(size=12),
        range=[0, max(values) * 1.18]
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        ticks='',
        tickfont=dict(size=12)
    ),
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.98,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=10, color='#888888')
        )
    ]
)

fig.update_traces(textfont_size=12, textfont_color='black')

base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")