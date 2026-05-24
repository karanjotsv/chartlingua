import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
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

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

text_labels = []
for val in values:
    if val == 0:
        label = f"{int(val)} MW"
    elif isinstance(val, int):
        label = f"{val:,} MW"
    else:
        label = f"{val:,.1f} MW"
    text_labels.append(label)

text_positions = ['outside' if v > 0 else 'inside' for v in values]

# Reverse data for top-to-bottom display in Plotly
categories.reverse()
values.reverse()
colors.reverse()
text_labels.reverse()
text_positions.reverse()

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors),
    text=text_labels,
    textposition=text_positions,
    textfont=dict(family="Arial", size=14, color='#333333'),
    insidetextanchor='start',
    hoverinfo='none'
))

title_text = f"<b>{texts['title']}</b><br><span style='font-size: 16px; color:#555555;'>{texts['subtitle']}</span>"
source_note_text = f"{texts['source']}<br>{texts['note']}"

fig.update_layout(
    title=dict(
        text=title_text,
        y=0.96,
        x=0.01,
        xanchor='left',
        yanchor='top',
        font=dict(size=22)
    ),
    font=dict(family="Arial", size=14, color='#333333'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        showgrid=True,
        gridcolor='#dddddd',
        zeroline=False,
        showline=False,
        ticksuffix=" MW",
        range=[0, max(values) * 1.15],
        dtick=500,
        tickfont=dict(size=14)
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        ticks='',
        tickfont=dict(size=14)
    ),
    margin=dict(l=120, r=40, t=110, b=80),
    annotations=[
        dict(
            text=source_note_text,
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.15,
            xanchor='left',
            yanchor='top',
            align='left',
            font=dict(size=12, color='#666666')
        )
    ]
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")