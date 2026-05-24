import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load data from JSON file provided as a command-line argument ---
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# --- 2. Extract data and texts from the loaded JSON ---
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# --- 3. Create the Plotly figure ---
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else '#1f77b4',
    text=values,
    textposition='auto',
    textfont=dict(family="Arial", size=12, color='black'),
    hoverinfo='none'
))

# --- 4. Configure layout and styling ---
# Combine title and subtitle if they exist
title_text = ""
if texts.get("title"):
    title_text += texts["title"]
if texts.get("subtitle"):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Create a list for annotations (source and note)
annotations = []
if texts.get("note"):
    annotations.append(dict(
        xref='paper', yref='paper',
        x=0, y=-0.15,
        xanchor='left', yanchor='top',
        text=texts["note"],
        showarrow=False,
        align='left',
        font=dict(family="Arial", size=12, color="#555555")
    ))
if texts.get("source"):
    annotations.append(dict(
        xref='paper', yref='paper',
        x=1, y=-0.15,
        xanchor='right', yanchor='top',
        text=texts["source"],
        showarrow=False,
        align='right',
        font=dict(family="Arial", size=12, color="#555555")
    ))

fig.update_layout(
    title=dict(
        text=title_text if title_text else None,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickfont=dict(family="Arial"),
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 350],
        tickmode='linear',
        tick0=0,
        dtick=50,
        gridcolor='#EAEAEA',
        tickfont=dict(family="Arial")
    ),
    font=dict(
        family="Arial",
        size=14
    ),
    showlegend=False,
    plot_bgcolor='white',
    paper_bgcolor='#F8F9FA',
    margin=dict(l=80, r=40, t=50, b=100),
    annotations=annotations
)

# --- 5. Output the chart as a PNG file ---
output_filename = f"{json_path.stem}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")