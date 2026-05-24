import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

fig = go.Figure()

for i, series in enumerate(chart_data["chart_data"]):
    color = chart_data["colors"][i]
    fig.add_trace(go.Scatter(
        x=series["x"],
        y=series["y"],
        name=series["name"],
        mode='lines+markers',
        line=dict(color=color, width=2),
        marker=dict(color=color, size=5, symbol='circle'),
        showlegend=False
    ))

# Combine title and subtitle
title_text = f'<b>{chart_data["texts"]["title"]}</b>  <span style="color:grey;">{chart_data["texts"]["subtitle"]}</span>'

fig.update_layout(
    plot_bgcolor='#E6F2F8',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12, color="black"),
    title=dict(
        text=title_text,
        y=0.97,
        x=0.01,
        xanchor='left',
        yanchor='top'
    ),
    margin=dict(l=40, r=40, b=40, t=100),
    xaxis=dict(
        range=[1972, 2007],
        tickvals=[1975, 1980, 1985, 1990, 1995, 2000, 2005],
        showgrid=False,
        zeroline=False,
        linecolor='black',
        linewidth=1
    ),
    yaxis=dict(
        range=[12, 47],
        tickvals=[15, 20, 25, 30, 35, 40, 45],
        gridcolor='white',
        gridwidth=1.5,
        zeroline=False
    ),
    showlegend=False
)

# Add source annotation
fig.add_annotation(
    text=chart_data["texts"]["source"],
    align='right',
    showarrow=False,
    xref='paper',
    yref='paper',
    x=0.99,
    y=0.99,
    xanchor='right',
    yanchor='bottom'
)

# Add data series annotations (labels)
annotations_from_json = chart_data.get("annotations", [])
for ann in annotations_from_json:
    fig.add_annotation(
        x=ann["x"],
        y=ann["y"],
        xref="x",
        yref="y",
        text=ann["text"],
        showarrow=True,
        arrowhead=6,
        arrowwidth=1.0,
        arrowcolor='#636363',
        ax=ann["ax"],
        ay=ann["ay"],
        font=dict(
            family="Arial",
            size=11
        ),
        bgcolor="white",
        bordercolor="#cccccc",
        borderwidth=1,
        borderpad=4
    )

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")