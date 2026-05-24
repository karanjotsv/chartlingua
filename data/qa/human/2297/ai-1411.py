import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# --- 1. Load Data from JSON ---
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# --- 2. Extract Data and Texts ---
chart_data = chart_info.get("chart_data", {})
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])
categories = chart_data.get("categories", [])
series_list = chart_data.get("series", [])
data_suffix = texts.get("data_labels_suffix", "")

# --- 3. Create Figure ---
fig = go.Figure()

# --- 4. Add Bar Traces ---
for i, series in enumerate(series_list):
    # Prepare text labels for each bar
    bar_texts = [f"{val}{data_suffix}" for val in series.get("data", [])]
    
    # Position labels outside for positive values, inside for negative
    text_positions = ['outside' if val >= 0 else 'inside' for val in series.get("data", [])]
    
    fig.add_trace(go.Bar(
        x=categories,
        y=series.get("data", []),
        name=series.get("name", ""),
        marker_color=colors[i % len(colors)],
        text=bar_texts,
        textposition=text_positions,
        textfont=dict(family="Arial, bold", size=12, color='black'),
        hoverinfo='none' # Hiding hover to match static image
    ))

# --- 5. Configure Layout ---
# Combine title and subtitle if they exist
title_text = texts.get("title") or ""
if texts.get("subtitle"):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

fig.update_layout(
    barmode='group',
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12),
    title=dict(
        text=title_text if title_text else None,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts.get("x_axis_title"),
        showgrid=False,
        zeroline=False,
        linecolor='black'
    ),
    yaxis=dict(
        title_text=texts.get("y_axis_title"),
        showgrid=True,
        gridcolor='#E5E5E5',
        zeroline=True,
        zerolinecolor='black',
        zerolinewidth=1,
        tickvals=[-10, 0, 10, 20, 30, 40],
        ticktext=[f"{v}%" for v in [-10, 0, 10, 20, 30, 40]],
        range=[-15, 45] # Add padding to prevent label clipping
    ),
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.15,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=80, r=40, t=50, b=120),
    annotations=[
        dict(
            text=texts.get("source", ""),
            showarrow=False,
            xref="paper",
            yref="paper",
            x=1.0,
            y=-0.25,
            xanchor='right',
            yanchor='top',
            font=dict(size=10)
        )
    ]
)

# --- 6. Output Image ---
output_filename = json_path.with_suffix('.png')
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")