import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load Data from JSON ---
# The script requires the JSON file path as a command-line argument.
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors from the JSON structure.
data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# --- 2. Prepare Data for Plotting ---
# Plotly's horizontal bar charts are plotted from bottom to top.
# To match the visual order (top-down), the data lists must be reversed.
y_categories = [item['brand'] for item in reversed(data)]
x_values = [item['share'] for item in reversed(data)]
bar_labels = [f"{item['share']}%" for item in reversed(data)]

# --- 3. Create the Chart Figure ---
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    y=y_categories,
    x=x_values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=bar_labels,
    textposition='outside',
    textfont=dict(color='black', size=12),
    cliponaxis=False  # Prevents text labels at the edge from being clipped
))

# --- 4. Configure Layout and Styling ---
# Combine title and subtitle using HTML for rich text formatting.
title_text = ""
if texts.get('title'):
    title_text += f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Combine source and note for the annotation.
source_note_text = ""
if texts.get('source'):
    source_note_text += texts['source']
if texts.get('note'):
    source_note_text += f"<br>{texts['note']}"

annotations = []
if source_note_text:
    annotations.append(
        dict(
            text=source_note_text,
            showarrow=False,
            xref='paper', yref='paper',
            x=1.0, y=-0.12,
            xanchor='right', yanchor='top',
            align='right',
            font=dict(size=10)
        )
    )

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title=texts.get('x_axis_title', ''),
        ticksuffix='%',
        showgrid=True,
        gridcolor='#EAEAEA',
        gridwidth=1,
        zeroline=False,
        range=[0, max(x_values) * 1.18] # Set range to give space for labels
    ),
    yaxis=dict(
        title=texts.get('y_axis_title', ''),
        showgrid=False,
        zeroline=False,
        autorange=True
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12, color="black"),
    showlegend=False,
    margin=dict(l=100, r=50, t=40, b=80), # Margins for category labels and source note
    annotations=annotations
)

# --- 5. Save the Output ---
# The output filename is derived from the input JSON filename.
output_filename = json_path.with_suffix('.png')
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")