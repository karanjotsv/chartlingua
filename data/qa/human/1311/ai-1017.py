import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load data from JSON file ---
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]
with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# --- 2. Extract data and texts ---
data_series = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']
json_annotations = chart_data['annotations']

# --- 3. Create the figure ---
fig = go.Figure()

# --- 4. Add data traces ---
for i, series in enumerate(data_series):
    color = colors[i]
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        mode='lines+markers+text',
        name=series['name'],
        line=dict(color=color, width=2.5),
        marker=dict(
            color='white',
            size=9,
            line=dict(color=color, width=2)
        ),
        text=series['text'],
        textposition=series['textposition'],
        textfont=dict(
            family="Arial",
            size=12,
            color="#3D3D3D"
        ),
        hoverinfo='none',
        showlegend=False
    ))

# --- 5. Configure layout, axes, and titles ---
title_text = f"{texts['title']}<br><span style='font-size: 14px; color:#555555; font-weight:normal;'>{texts['subtitle']}</span>"

source_text = f"{texts['source_and_note']}<br>{texts['logo']}"

# --- 6. Prepare annotations ---
layout_annotations = []

# Add series label annotations from JSON
for i, ann in enumerate(json_annotations):
    layout_annotations.append(
        go.layout.Annotation(
            text=ann['text'],
            x=ann['x'],
            y=ann['y'],
            xref="x",
            yref="y",
            showarrow=False,
            font=dict(
                family="Arial",
                size=14,
                color=colors[i]
            ),
            align=ann['align']
        )
    )

# Add source annotation
layout_annotations.append(
    go.layout.Annotation(
        text=source_text,
        xref="paper", yref="paper",
        x=0, y=-0.15,
        xanchor="left", yanchor="top",
        align="left",
        showarrow=False,
        font=dict(family="Arial", size=11, color="#555555")
    )
)

# --- 7. Update layout ---
fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    font=dict(family="Arial", color="#333333"),
    title=dict(
        text=title_text,
        x=0.01,
        y=0.98,
        xanchor='left',
        yanchor='top',
        font=dict(size=20)
    ),
    xaxis=dict(
        range=[2011.5, 2018.5],
        tickvals=[2012, 2014, 2016, 2018],
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        ticks='outside',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        range=[-5, 85],
        tickvals=[0, 80],
        ticktext=['0', '80 %'],
        showgrid=False,
        showline=False,
        zeroline=True,
        zerolinecolor='black',
        zerolinewidth=1,
        tickfont=dict(size=12)
    ),
    margin=dict(l=40, r=40, t=120, b=100),
    annotations=layout_annotations
)

# --- 8. Save the chart as a PNG image ---
base_filename = pathlib.Path(json_path).stem
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2, width=450, height=450)

print(f"Chart saved to {output_filename}")