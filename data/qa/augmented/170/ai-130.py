import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# --- 1. Argument and File Handling ---
if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]
json_path = Path(json_file_path)

if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# --- 2. Data Loading ---
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in '{json_file_path}'")
    sys.exit(1)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# --- 3. Data Preparation ---
# Reverse data for Plotly's top-to-bottom rendering in horizontal bars
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
categories.reverse()
values.reverse()

# --- 4. Chart Creation ---
fig = go.Figure()

# Add bar trace
fig.add_trace(go.Bar(
    x=values,
    y=categories,
    orientation='h',
    marker=dict(color=colors[0]),
    text=[f'{v:.2f}' for v in values],
    textposition='outside',
    cliponaxis=False, # Prevent text from being clipped at the chart edge
    hoverinfo='none'
))

# --- 5. Layout and Styling ---
# Combine title and subtitle using HTML for rich formatting
title_text = ""
if texts.get("title"):
    title_text += f"<b>{texts['title']}</b>"
if texts.get("subtitle"):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#E5E5E5',
        gridwidth=1,
        griddash='dash',
        zeroline=False,
        showline=False,
        ticks='outside',
        automargin=True
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        showgrid=False,
        showline=False,
        ticks='',
        automargin=True
    ),
    margin=dict(l=120, r=60, t=50, b=100),
    showlegend=False
)

# Add annotations for source and note at the bottom
annotations = []
if texts.get("note"):
    annotations.append(
        dict(
            xref='paper', yref='paper',
            x=0, y=-0.18,
            xanchor='left', yanchor='top',
            text=f"<i>{texts['note']}</i>",
            showarrow=False,
            font=dict(size=11, color='#555555')
        )
    )
if texts.get("source"):
    annotations.append(
        dict(
            xref='paper', yref='paper',
            x=1, y=-0.18,
            xanchor='right', yanchor='top',
            text=texts['source'],
            showarrow=False,
            font=dict(size=11, color='#555555')
        )
    )

fig.update_layout(annotations=annotations)

# --- 6. Output ---
output_filename = json_path.stem + '.png'
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to '{output_filename}'")