import sys
import json
import plotly.graph_objects as go
import os

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

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(
        color=colors,
        line=dict(color='black', width=2)
    ),
    text=values,
    textposition='inside',
    insidetextanchor='end',
    textfont=dict(
        family='Arial',
        size=16,
        color='black'
    ),
    hoverinfo='none'
))

title_text = f"<b>{texts.get('title', '')}</b>" if texts.get('title') else ''

fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(
            family='Arial',
            size=22,
            color='white'
        )
    ),
    xaxis=dict(
        visible=False,
        range=[0, max(values) * 1.05]
    ),
    yaxis=dict(
        autorange='reversed',
        showline=False,
        showgrid=False,
        showticklabels=True,
        tickfont=dict(
            family='Arial',
            size=18,
            color='white'
        )
    ),
    paper_bgcolor='#0D3D28',
    plot_bgcolor='#0D3D28',
    margin=dict(l=150, r=20, t=80, b=20),
    showlegend=False,
    font=dict(family="Arial")
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")