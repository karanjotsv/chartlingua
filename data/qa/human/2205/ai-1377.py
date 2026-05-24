import sys
import json
import plotly.graph_objects as go
import pathlib

# --- 1. Load Data from JSON ---
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path_str = sys.argv[1]
json_path = pathlib.Path(json_path_str)

if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path_str}'")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_config = json.load(f)

# --- 2. Extract and Prepare Data ---
chart_data = chart_config['chart_data']
texts = chart_config['texts']
colors = chart_config['colors']

categories = [item['category'] for item in chart_data]
num_series = len(texts['legend_labels'])
series_values = [[] for _ in range(num_series)]

for item in chart_data:
    for i in range(num_series):
        series_values[i].append(item['values'][i])

# --- 3. Create the Chart ---
fig = go.Figure()

for i in range(num_series):
    fig.add_trace(go.Bar(
        x=categories,
        y=series_values[i],
        name=texts['legend_labels'][i],
        marker_color=colors[i],
        text=[f"{val}{texts.get('data_labels_suffix', '')}" for val in series_values[i]],
        textposition='outside',
        cliponaxis=False  # Prevents text labels on tall bars from being clipped
    ))

# --- 4. Configure Layout ---
# Combine title and subtitle if they exist
title_text = texts.get('title')
subtitle_text = texts.get('subtitle')
full_title = ""
if title_text:
    full_title += f"<b>{title_text}</b>"
if subtitle_text:
    if full_title:
        full_title += "<br>"
    full_title += subtitle_text

fig.update_layout(
    barmode='group',
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12),
    title_text=full_title if full_title else None,
    title_x=0.05,
    title_y=0.95,
    title_xanchor='left',
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=[0, 105], # Extra space for top data labels
        tickvals=[0, 20, 40, 60, 80, 100],
        ticksuffix=texts.get('data_labels_suffix', ''),
        gridcolor='#E5E5E5',
        zeroline=False,
        showline=False
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=False,
        showline=True,
        linecolor='black'
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5,
        traceorder='normal'
    ),
    margin=dict(t=60, b=120, l=80, r=40),
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.98,
            y=-0.3,
            xanchor='right',
            yanchor='bottom',
            align='right',
            font=dict(size=12)
        )
    ]
)

# --- 5. Output the Image ---
output_filename = json_path.stem + ".png"
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")