import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load data from JSON file ---
if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# --- 2. Extract data and configuration ---
data = chart_data.get('chart_data', [])
texts = chart_data.get('texts', {})
colors = chart_data.get('colors', {})
shapes = chart_data.get('shapes', [])
title_text = texts.get('title')

# --- 3. Prepare data for plotting ---
years = [d['year'] for d in data]
values = [d['value'] for d in data]

pos_years = [years[i] for i, v in enumerate(values) if v >= 0]
pos_values = [v for v in values if v >= 0]

neg_years = [years[i] for i, v in enumerate(values) if v < 0]
neg_values = [v for v in values if v < 0]

# --- 4. Create the figure ---
fig = go.Figure()

# Add trace for positive values
fig.add_trace(go.Bar(
    x=pos_years,
    y=pos_values,
    marker_color=colors.get('positive_bar', 'blue'),
    name='Positive Rate'
))

# Add trace for negative values
fig.add_trace(go.Bar(
    x=neg_years,
    y=neg_values,
    marker_color=colors.get('negative_bar', 'red'),
    name='Negative Rate'
))

# --- 5. Apply layout and styling ---
fig.update_layout(
    title_text=title_text,
    title_x=0.5,
    title_font_size=18,
    font_family="Arial",
    plot_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickmode='linear',
        tick0=1930,
        dtick=5,
        showgrid=True,
        gridcolor=colors.get('grid_color', '#D3D3D3'),
        gridwidth=1,
        zeroline=False,
        range=[1928, 2008]
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[-5, 30],
        tickmode='linear',
        tick0=-5,
        dtick=5,
        showgrid=True,
        gridcolor=colors.get('grid_color', '#D3D3D3'),
        gridwidth=1,
        zeroline=True,
        zerolinecolor='black',
        zerolinewidth=1
    ),
    margin=dict(t=80, b=50, l=50, r=50),
    barmode='relative'
)

# Add shapes from JSON
if shapes:
    for shape in shapes:
        fig.add_shape(**shape)

# Add annotations from JSON
annotations = texts.get('annotations', [])
if annotations:
    for anno in annotations:
        fig.add_annotation(
            text=anno.get('text', ''),
            x=anno.get('x'),
            y=anno.get('y'),
            xref="x",
            yref="y",
            showarrow=anno.get('showarrow', False),
            align=anno.get('align', 'center'),
            font=dict(family="Arial", size=12)
        )
# Workaround for the title box in the original image
fig.add_shape(
    type="rect",
    xref="paper", yref="paper",
    x0=0.35, y0=0.92, x1=0.65, y1=1.0,
    line=dict(color="black", width=1),
    fillcolor="white"
)
fig.update_layout(title_y=0.96)


# --- 6. Output the image ---
output_filename = pathlib.Path(json_path).stem + ".png"
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")