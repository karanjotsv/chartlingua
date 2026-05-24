import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_file_path = pathlib.Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)

with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_data_json = json.load(f)

chart_data = chart_data_json['chart_data']
texts = chart_data_json['texts']
colors = chart_data_json['colors']

fig = go.Figure()

# Add traces and annotations for each data series
all_annotations = []
for i, series in enumerate(chart_data):
    color = colors[i]
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        mode='lines',
        line=dict(color=color, width=3),
        showlegend=False
    ))

    # Add series label annotation
    all_annotations.append(go.layout.Annotation(
        x=series['label']['x'],
        y=series['label']['y'],
        text=series['label']['text'],
        showarrow=False,
        font=dict(color=color, size=14, family="Arial"),
        align='center'
    ))

    # Add data point annotations
    for ann in series['annotations']:
        all_annotations.append(go.layout.Annotation(
            x=ann['x'],
            y=ann['y'],
            text=ann['text'],
            showarrow=False,
            yshift=ann['y_offset'],
            font=dict(color=color, size=11, family="Arial")
        ))

# Combine title and subtitle
title_text = f"<b>{texts['title']}</b><br><i style='color:#555555'>{texts['subtitle']}</i>"

# Add source text as a separate annotation
source_annotation = go.layout.Annotation(
    text=texts['source'],
    align='left',
    showarrow=False,
    xref='paper',
    yref='paper',
    x=0,
    y=-0.22,
    xanchor='left',
    yanchor='top',
    font=dict(size=11, color="#555555", family="Arial")
)
all_annotations.append(source_annotation)

fig.update_layout(
    annotations=all_annotations,
    title=dict(
        text=title_text,
        x=0.01,
        y=0.98,
        xanchor='left',
        yanchor='top',
        font=dict(size=20, family="Arial")
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=20, r=20, t=100, b=140),
    xaxis=dict(
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=False,
        showgrid=False,
        tickmode='array',
        tickvals=[1969, 1974, 1979, 1984, 1989, 1994, 1999, 2004, 2009, 2014],
        range=[1968, 2016],
        tickfont=dict(family="Arial", size=12)
    ),
    yaxis=dict(
        showticklabels=False,
        showgrid=False,
        showline=False,
        zeroline=False,
        range=[0, 95]
    ),
    font=dict(family="Arial")
)

# Output the image
base_filename = json_file_path.stem
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")