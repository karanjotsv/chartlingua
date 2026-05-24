import sys
import json
import os
import plotly.graph_objects as go

# --- 1. Load data from JSON file ---
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
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

# --- 2. Extract data and texts ---
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

# Plotly displays horizontal bars from bottom to top, so we reverse the data
data.reverse()

categories = [item['category'] for item in data]
values = [item['value'] for item in data]
bar_text = [str(item['value']) for item in data]

# --- 3. Create the chart figure ---
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=bar_text,
    textposition='inside',
    insidetextanchor='end',
    textfont=dict(
        family='Arial',
        size=14,
        color='white'
    ),
    hoverinfo='none' # Disable hover to match static image
))

# --- 4. Configure layout, title, and annotations ---
# Combine title and subtitle
title_text = f"<b>{texts['title']}</b><br><span style='font-size: 14px;'><i>{texts['subtitle']}</i></span>"

# Combine note and source for annotation
note_source_text = f"{texts['note']}<br>{texts['source']}"

fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.01,
        xanchor='left',
        yanchor='top',
        font=dict(size=18)
    ),
    xaxis=dict(
        visible=False,
        showgrid=False,
        zeroline=False
    ),
    yaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=True,
        domain=[0, 0.82] # Leave space at the bottom for annotations
    ),
    margin=dict(l=320, r=20, t=120, b=120),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=14),
    showlegend=False,
    annotations=[
        dict(
            xref="paper",
            yref="paper",
            x=0.01,
            y=-0.15,
            xanchor="left",
            yanchor="top",
            text=note_source_text,
            showarrow=False,
            align="left",
            font=dict(size=12)
        ),
        dict(
            xref="paper",
            yref="paper",
            x=0.01,
            y=-0.25,
            xanchor="left",
            yanchor="top",
            text=f"<b>{texts['logo']}</b>",
            showarrow=False,
            align="left",
            font=dict(size=12, color="black")
        )
    ]
)

# --- 5. Output the image ---
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")