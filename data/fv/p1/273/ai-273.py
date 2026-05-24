import sys
import json
import plotly.graph_objects as go
import pathlib

# --- 1. Load data from JSON file ---
if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# --- 2. Extract data and text ---
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])
title_text = texts.get('title', '')
footer_notes = texts.get('footer_notes', '')

# --- 3. Prepare data for Plotly ---
labels = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Generate display text for pie slices (value + asterisks if applicable)
display_texts = []
for item in chart_data:
    text = f"{item['value']}"
    if '**' in item['category']:
        text += '**'
    elif '*' in item['category']:
        text += '*'
    display_texts.append(text)

# Explode the first (largest) slice
pull_values = [0.2] + [0] * (len(chart_data) - 1)

# --- 4. Create the chart ---
# Note: Plotly does not support 3D pie charts. A 2D pie chart is created
# as the closest possible representation.
fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#000000', width=1)),
    pull=pull_values,
    text=display_texts,
    textinfo='text',
    textposition='outside',
    sort=False,  # Preserve the original data order
    direction='clockwise'
)])

# --- 5. Configure layout and styling ---
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        font=dict(size=20, weight='bold')
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    legend=dict(
        traceorder='normal', # Match data order
        x=1,
        y=0.95,
        xanchor='left',
        yanchor='top'
    ),
    margin=dict(l=50, r=350, t=100, b=100), # Ample right margin for legend
    paper_bgcolor='white',
    plot_bgcolor='white',
    showlegend=True
)

# Add footer notes using an annotation
if footer_notes:
    fig.add_annotation(
        text=footer_notes,
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1,
        y=0.05,
        xanchor='right',
        yanchor='bottom'
    )

# --- 6. Save the output image ---
output_image_path = json_path.with_suffix('.png')
fig.write_image(output_image_path, scale=2, width=800, height=600)

print(f"Chart saved to {output_image_path}")