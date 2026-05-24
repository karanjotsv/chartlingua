import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])
background_color = config.get('background_color', '#FFFFFF')

labels = [item.get('label') for item in chart_data]
values = [item.get('value') for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=1)),
    textinfo='percent',
    textposition='outside',
    hoverinfo='label+percent',
    sort=False,
    direction='clockwise',
    textfont_family="Arial"
))

title_parts = [texts.get('title'), texts.get('subtitle')]
full_title = "<br>".join(filter(None, title_parts))

source_parts = [texts.get('source'), texts.get('note')]
full_source_text = "<br>".join(filter(None, source_parts))

fig.update_layout(
    title=dict(
        text=full_title,
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(family="Arial", size=24)
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.15,
        xanchor="center",
        x=0.5,
        font=dict(family="Arial")
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    margin=dict(l=40, r=40, t=120, b=100),
    paper_bgcolor=background_color,
    plot_bgcolor=background_color
)

if full_source_text:
    fig.add_annotation(
        text=full_source_text,
        showarrow=False,
        xref="paper",
        yref="paper",
        x=0,
        y=-0.25,
        xanchor='left',
        yanchor='bottom',
        align='left',
        font=dict(family="Arial")
    )

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2, width=700, height=600)

print(f"Chart successfully generated and saved to {output_filename}")