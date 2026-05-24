import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load Data from JSON ---
# The script requires the path to the JSON file as a command-line argument.
if len(sys.argv) != 2:
    print(f"Usage: python {pathlib.Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# --- 2. Prepare Data for Plotting ---
data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])
text_colors = chart_info.get('text_colors', [])

labels = [item.get('label', '') for item in data]
values = [item.get('value', 0) for item in data]
text_labels = [f"{item.get('label', '')}<br>{item.get('value', 0)}%" for item in data]

# --- 3. Create the Chart Figure ---
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    hole=0.4,
    marker=dict(colors=colors),
    text=text_labels,
    textinfo='text',
    textposition='inside',
    textfont=dict(
        family="Arial",
        size=24,
        color=text_colors if text_colors else 'black'
    ),
    hoverinfo='none',
    sort=False,
    direction='clockwise',
    rotation=90
))

# --- 4. Configure Layout and Styling ---
# Combine title and subtitle using HTML for rich formatting
title_parts = []
if texts.get('title'):
    title_parts.append(f"<span style='font-size: 24px;'><b>{texts['title']}</b></span>")
if texts.get('subtitle'):
    title_parts.append(f"<span style='font-size: 18px;'>{texts['subtitle']}</span>")
full_title_text = '<br>'.join(title_parts)

fig.update_layout(
    showlegend=False,
    plot_bgcolor='black',
    paper_bgcolor='black',
    font=dict(family="Arial", color="white"),
    margin=dict(l=20, r=20, t=60 if full_title_text else 20, b=20),
    title_text=full_title_text if full_title_text else None,
    title_x=0.5,
    title_y=0.95,
    title_xanchor='center',
    title_yanchor='top'
)

# Combine source and note for an annotation at the bottom
annotation_parts = []
if texts.get('source'):
    annotation_parts.append(texts['source'])
if texts.get('note'):
    annotation_parts.append(texts['note'])
full_annotation_text = '<br>'.join(annotation_parts)

if full_annotation_text:
    fig.add_annotation(
        text=full_annotation_text,
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0,
        y=-0.05,
        xanchor='left',
        yanchor='top',
        font=dict(size=12)
    )

# --- 5. Save the Output Image ---
output_filename = json_path.stem + ".png"
fig.write_image(output_filename, scale=2, width=600, height=600)
print(f"Chart saved to {output_filename}")