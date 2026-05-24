import sys
import json
import plotly.graph_objects as go

# --- 1. Argument and File Handling ---
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_filepath = sys.argv[1]

try:
    with open(json_filepath, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_filepath}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_filepath}")
    sys.exit(1)

# --- 2. Data Extraction from JSON ---
data = chart_data.get('chart_data', [])
texts = chart_data.get('texts', {})
colors = chart_data.get('colors', [])

labels = [d['label'] for d in data]
values = [d['value'] for d in data]

# --- 3. Chart Creation and Styling ---
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='#000000', width=1)
    ),
    textinfo='label',
    textposition='outside',
    sort=False,
    direction='clockwise',
    hole=0
))

# --- 4. Layout Configuration ---
title_parts = []
if texts.get('title'):
    title_parts.append(texts['title'])
if texts.get('subtitle'):
    title_parts.append(f"<span style='font-size: 14px;'>{texts['subtitle']}</span>")
full_title = "<br>".join(title_parts)

fig.update_layout(
    title_text=full_title,
    title_x=0.5,
    title_y=0.95,
    title_font_size=20,
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    showlegend=False,
    margin=dict(l=100, r=100, t=100, b=100),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

# --- 5. Output Generation ---
# Derive the output filename from the input JSON filename
if json_filepath.endswith('.json'):
    output_filename_base = json_filepath[:-5]
else:
    output_filename_base = json_filepath

output_image_path = f"{output_filename_base}.png"

fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")