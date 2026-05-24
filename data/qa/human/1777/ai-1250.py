import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load Data from JSON ---
# The script expects the JSON file path as the sole command-line argument.
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Extract data, texts, and colors from the loaded JSON
chart_data = config.get("chart_data", [])
texts = config.get("texts", {})
colors = config.get("colors", [])

# Prepare data for Plotly traces
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# --- 2. Create the Chart ---
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors,
    text=values,
    textposition='outside',
    texttemplate='%{text:.1f}',
    textfont=dict(
        family="Arial",
        color=colors,
        size=14
    ),
    cliponaxis=False  # Prevents data labels at the top from being clipped
))

# --- 3. Configure Layout and Styling ---
# Combine title and subtitle using HTML for rich formatting
title_text = f"<b>{texts.get('title', '')}</b><br>{texts.get('subtitle', '')}"

# Use annotations for custom x-axis labels to control color and angle
annotations = []
for i, data_point in enumerate(chart_data):
    annotations.append(
        dict(
            x=data_point['category'],
            y=0,
            yref='y',
            yshift=-25, # Shift label below the axis line
            text=data_point['category'],
            showarrow=False,
            font=dict(
                family="Arial",
                color=colors[i],
                size=12
            ),
            textangle=-45
        )
    )

# Add source text annotation at the top right
if texts.get('source'):
    annotations.append(
        dict(
            xref="paper", yref="paper",
            x=0.99, y=1.06,
            showarrow=False,
            text=texts['source'],
            xanchor='right', yanchor='bottom',
            font=dict(family="Arial", size=12, color='#444444')
        )
    )

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.01,
        y=0.95,
        xanchor='left',
        yanchor='top',
        font=dict(family="Arial", size=24, color='#333333')
    ),
    xaxis=dict(
        showticklabels=False,  # Hide default labels; we use annotations
        showgrid=False,
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title') if texts.get('y_axis_title') else "",
        range=[0, 20],
        tickmode='array',
        tickvals=[i for i in range(0, 20, 2)],
        gridcolor='#FFFFFF',
        zeroline=False,
        showline=False,
        tickfont=dict(family="Arial", size=12)
    ),
    plot_bgcolor='#eaf1f5',
    paper_bgcolor='#eaf1f5',
    font=dict(family="Arial"),
    showlegend=False,
    margin=dict(l=60, r=40, t=130, b=100),
    annotations=annotations,
    # Add a decorative line below the title area
    shapes=[
        dict(
            type='line',
            xref='paper', yref='paper',
            x0=0, y0=0.86, x1=1, y1=0.86,
            line=dict(color='#0082ba', width=2)
        )
    ]
)

# --- 4. Output the Image ---
output_filename = json_path.with_suffix('.png')
fig.write_image(output_filename, scale=2, width=1000, height=600)

print(f"Chart successfully generated and saved to {output_filename}")