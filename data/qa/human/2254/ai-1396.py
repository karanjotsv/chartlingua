import sys
import json
import plotly.graph_objects as go

# --- 1. Load Data from JSON ---
# The script expects the JSON file path as a command-line argument.
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

chart_data = chart_config.get("chart_data", [])
texts = chart_config.get("texts", {})
colors = chart_config.get("colors", [])
data_labels_suffix = texts.get("data_labels_suffix", "")

# --- 2. Create the Plotly Figure ---
fig = go.Figure()

# --- 3. Add Traces (Bars) ---
# Iterate through the data series from the JSON to create a bar for each.
# This preserves the original order.
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=series.get("x"),
        y=series.get("y"),
        name=series.get("name"),
        marker_color=colors[i % len(colors)],
        text=[f"{y:g}{data_labels_suffix}" for y in series.get("y", [])],
        textposition='outside',
        textfont=dict(family="Arial", size=12, color='black'),
        cliponaxis=False
    ))

# --- 4. Configure Layout ---
# Combine title and subtitle
title_parts = []
if texts.get("title"):
    title_parts.append(f'<b>{texts["title"]}</b>')
if texts.get("subtitle"):
    title_parts.append(f'<i>{texts["subtitle"]}</i>')
full_title = "<br>".join(title_parts)

fig.update_layout(
    barmode='group',
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12),
    title=dict(text=full_title, x=0.5),
    xaxis=dict(
        title_text=texts.get("x_axis_title"),
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        mirror=True,
        ticks='outside'
    ),
    yaxis=dict(
        title_text=texts.get("y_axis_title"),
        showgrid=True,
        gridcolor='#e0e0e0',
        showline=True,
        linecolor='black',
        linewidth=1,
        mirror=True,
        range=[0, 1.55],
        dtick=0.25,
        ticksuffix='$'
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5,
        title_text=texts.get("legend_title")
    ),
    margin=dict(l=80, r=40, b=120, t=40, pad=4)
)

# --- 5. Add Source/Note Annotation ---
# Combine source and note for a single annotation box.
source_parts = []
if texts.get("source"):
    source_parts.append(texts["source"])
if texts.get("note"):
    source_parts.append(texts["note"])
source_text = "<br>".join(source_parts)

if source_text:
    fig.add_annotation(
        text=source_text,
        xref="paper",
        yref="paper",
        x=1.0,
        y=-0.32,
        showarrow=False,
        xanchor='right',
        yanchor='bottom',
        align='right',
        font=dict(size=10, color="#555555")
    )

# --- 6. Output the Image ---
# Derive the output filename from the input JSON path.
if json_path.endswith('.json'):
    output_filename = json_path[:-5] + '.png'
else:
    output_filename = json_path + '.png'

fig.write_image(output_filename, scale=2)
print(f"Chart saved to '{output_filename}'")