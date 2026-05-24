import sys
import json
import os
import plotly.graph_objects as go

# --- 1. Load Data from JSON ---
# The script expects the JSON file path as the sole command-line argument.
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the file exists
if not os.path.exists(json_path):
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Read the JSON data
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for easy access
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# --- 2. Create Chart ---
fig = go.Figure()

# Add the donut chart trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    hole=0.6,
    marker=dict(colors=colors, line=dict(color='white', width=1)),
    pull=[0.03, 0.03],
    textinfo='percent',
    insidetextfont=dict(family='Arial', size=18, color='white'),
    hoverinfo='label+percent',
    sort=False,  # Preserve the order from the JSON file
    direction='clockwise'
))

# --- 3. Configure Layout ---
# Combine title and subtitle
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text = f"<b>{title_text}</b><br><sub>{texts['subtitle']}</sub>"
else:
    title_text = f"<b>{title_text}</b>"

fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.05,
        xanchor='left',
        yanchor='top'
    ),
    showlegend=True,
    legend=dict(
        orientation='v',
        yanchor="top",
        y=0.25,
        xanchor="left",
        x=0.25,
        traceorder='normal',
        font=dict(
            family="Arial",
            size=12
        ),
        bgcolor='rgba(0,0,0,0)'
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(l=40, r=40, t=120, b=40),
    annotations=[] # Placeholder for source/note if needed
)

# Add source/note at the bottom if present
# This chart has no source, but the logic is here for robustness.
source_note_text = []
if texts.get('source'):
    source_note_text.append(texts['source'])
if texts.get('note'):
    source_note_text.append(texts['note'])

if source_note_text:
    fig.add_annotation(
        text='<br>'.join(source_note_text),
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0,
        y=0,
        xanchor='left',
        yanchor='bottom',
        font=dict(size=10, color='#666666')
    )

# --- 4. Save Image ---
# Derive the output filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")