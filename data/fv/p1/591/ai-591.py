import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='#FFFFFF', width=1)
    ),
    hovertemplate='%{label}: %{value}%<extra></extra>',
    texttemplate='%{value}%',
    insidetextfont=dict(
        family="Arial",
        size=16,
        color="white"
    ),
    textposition='inside',
    sort=False,
    direction='clockwise',
    showlegend=True
))

title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(
            family="Arial",
            size=24,
            color="black"
        )
    ),
    legend=dict(
        orientation="v",
        yanchor="top",
        y=0.85,
        xanchor="left",
        x=0.8,
        font=dict(
            family="Arial",
            size=12
        ),
        bgcolor='rgba(0,0,0,0)'
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    paper_bgcolor='#E8E8E8',
    plot_bgcolor='#E8E8E8',
    margin=dict(l=40, r=200, t=100, b=40),
    width=800,
    height=550
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")