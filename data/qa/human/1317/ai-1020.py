import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

fig = go.Figure()

# Extract data for easier access
chart_data = config['chart_data']
colors = config['colors']
texts = config['texts']

# --- Trace 1: Hispanic eligible voters (split for dashed line) ---
series1 = chart_data[0]
color1 = colors[0]
text_values1 = [f'{y:.1f}' for y in series1['y']]

# Solid part of the line
fig.add_trace(go.Scatter(
    x=series1['x'][:8],
    y=series1['y'][:8],
    mode='lines+markers+text',
    text=text_values1[:8],
    textposition=series1['text_position'],
    textfont=dict(family="Arial", size=12, color=color1),
    line=dict(color=color1, width=3),
    marker=dict(color=color1, size=9, line=dict(color='white', width=2)),
    showlegend=False
))

# Dashed part of the line
fig.add_trace(go.Scatter(
    x=series1['x'][7:],
    y=series1['y'][7:],
    mode='lines+markers+text',
    text=['', text_values1[8]],
    textposition=series1['text_position'],
    textfont=dict(family="Arial", size=12, color=color1),
    line=dict(color=color1, width=3, dash='dash'),
    marker=dict(color=color1, size=9, line=dict(color='white', width=2)),
    showlegend=False
))

# --- Trace 2: Hispanic voters ---
series2 = chart_data[1]
color2 = colors[1]
text_values2 = [f'{y:.1f}' for y in series2['y']]

fig.add_trace(go.Scatter(
    x=series2['x'],
    y=series2['y'],
    mode='lines+markers+text',
    text=text_values2,
    textposition=series2['text_position'],
    textfont=dict(family="Arial", size=12, color=color2),
    line=dict(color=color2, width=3),
    marker=dict(color=color2, size=9, line=dict(color='white', width=2)),
    showlegend=False
))

# --- Layout and Styling ---
title_text = f"{texts['title']}<br><span style='font-size: 15px; color: #555555;'>{texts['subtitle']}</span>"

# Add annotations for series labels
fig_annotations = []
for ann in texts['annotations']:
    fig_annotations.append(go.layout.Annotation(
        text=ann['text'],
        x=ann['x'],
        y=ann['y'],
        showarrow=ann['showarrow'],
        font=dict(family="Arial", size=13),
        xanchor='left',
        align='left'
    ))

# Add annotation for source notes
fig_annotations.append(go.layout.Annotation(
    text=texts['source'],
    showarrow=False,
    xref='paper',
    yref='paper',
    x=0,
    y=-0.28,
    xanchor='left',
    yanchor='top',
    align='left',
    font=dict(family="Arial", size=11, color='#555555')
))

fig.update_layout(
    width=650,
    height=600,
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=20, r=20, t=110, b=180),
    font=dict(family="Arial"),
    title=dict(
        text=title_text,
        y=0.96,
        x=0.01,
        xanchor='left',
        yanchor='top',
        font=dict(family="Arial", size=19, color='black')
    ),
    xaxis=dict(
        tickvals=chart_data[0]['x'],
        showgrid=False,
        zeroline=False,
        linecolor='black',
        linewidth=1,
        ticks='outside',
        tickfont=dict(family="Arial", size=14, color='black')
    ),
    yaxis=dict(
        visible=False,
        range=[0, 33]
    ),
    annotations=fig_annotations
)

# --- Output ---
output_path = pathlib.Path(json_path).with_suffix('.png')
fig.write_image(str(output_path), scale=2)
print(f"Chart saved to {output_path}")