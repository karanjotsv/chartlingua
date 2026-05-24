import sys
import json
import os
import plotly.graph_objects as go

# --- 1. Load Data ---
# The script must be called with the JSON file path as the single argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Read the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_spec = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in '{json_path}'")
    sys.exit(1)

# Extract data from the JSON structure
chart_data = chart_spec.get('chart_data', [])
texts = chart_spec.get('texts', {})
colors = chart_spec.get('colors', [])
legend_annotations_spec = chart_spec.get('legend_annotations', [])

# --- 2. Create Chart ---
fig = go.Figure()

# Add data traces
for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        name=series.get('name'),
        mode='lines',
        line=dict(
            color=colors[i] if i < len(colors) else None,
            dash=series.get('line_style')
        ),
        legendgroup=series.get('legend_group')
    ))

# --- 3. Configure Layout ---
# Prepare annotations for legend groups
annotations = []
for anno in legend_annotations_spec:
    annotations.append(
        go.layout.Annotation(
            text=anno['text'],
            align='left',
            showarrow=False,
            xref='paper',
            yref=anno.get('y_ref', 'paper'),
            x=0.25,
            y=anno['y'],
            xanchor='left',
            yanchor=anno.get('y_anchor', 'middle'),
            font=dict(family="Arial", size=12)
        )
    )

# Update layout
fig.update_layout(
    title=dict(
        text=f"<b>{texts.get('title', '')}</b>",
        x=0.5,
        xanchor='center',
        yanchor='top',
        y=0.95
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        range=[-90, 90],
        tickvals=[-90, -70, -50, -30, -10, 10, 30, 50, 70, 90],
        showgrid=True,
        gridcolor='lightgrey',
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        type='log',
        range=[-3, 0], # Corresponds to 10^-3 to 10^0, i.e., 0.001 to 1.0
        tickvals=[0.001, 0.01, 0.1, 1.0],
        showgrid=True,
        gridcolor='lightgrey',
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True
    ),
    legend=dict(
        x=0.05,
        y=0.95,
        xanchor='left',
        yanchor='top',
        bgcolor='rgba(255, 255, 255, 0.8)',
        bordercolor='black',
        borderwidth=1
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='#f0f0f0',
    margin=dict(l=80, r=40, t=80, b=80),
    annotations=annotations
)

# --- 4. Output Image ---
# Derive the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Write the image file
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to '{output_filename}'")
except ValueError as e:
    if "requires the kaleido" in str(e) or "requires the orca" in str(e):
        print("\n---")
        print("Plotly image export requires the 'kaleido' package.")
        print("Please install it using: pip install kaleido")
        print("---\n")
    sys.exit(1)