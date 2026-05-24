import sys
import json
import os
import plotly.graph_objects as go

# --- 1. Load data from JSON file ---
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]
with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# --- 2. Extract data for plotting ---
data = chart_data['chart_data']
colors = chart_data['colors']
texts = chart_data['texts']

pie_labels = [d['pie_label'] for d in data]
legend_labels = [d['legend_label'] for d in data]
values = [d['value'] for d in data]

# --- 3. Create the Plotly figure ---
fig = go.Figure()

# --- 4. Add the Pie chart trace ---
fig.add_trace(go.Pie(
    labels=pie_labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#666666', width=1)),
    textinfo='label',
    textfont=dict(family="Arial", size=12, color='black'),
    hoverinfo='label+percent',
    sort=False,
    direction='counterclockwise',
    rotation=270,
    domain={'x': [0.3, 1.0], 'y': [0.0, 1.0]},
    showlegend=False,
    insidetextorientation='horizontal'
))

# --- 5. Create a custom legend using shapes and annotations ---
legend_shapes = []
legend_annotations = []

# Define legend area coordinates (paper reference)
legend_box = {'x0': 0.02, 'x1': 0.38, 'y0': 0.25, 'y1': 0.85}
num_items = len(data)
item_y_span = (legend_box['y1'] - legend_box['y0']) / num_items

# Add a border for the legend
legend_shapes.append(go.layout.Shape(
    type="rect",
    xref="paper", yref="paper",
    x0=legend_box['x0'], y0=legend_box['y0'],
    x1=legend_box['x1'], y1=legend_box['y1'],
    line=dict(color="grey", width=1)
))

# Add items to the legend
for i, item in enumerate(data):
    y_center = legend_box['y1'] - (i + 0.5) * item_y_span
    
    # Color swatch
    legend_shapes.append(go.layout.Shape(
        type="rect",
        xref="paper", yref="paper",
        x0=legend_box['x0'] + 0.02, 
        y0=y_center - 0.015,
        x1=legend_box['x0'] + 0.06, 
        y1=y_center + 0.015,
        fillcolor=colors[i],
        line_width=0
    ))
    
    # Category label
    legend_annotations.append(go.layout.Annotation(
        xref="paper", yref="paper",
        x=legend_box['x0'] + 0.08,
        y=y_center,
        text=item['legend_label'],
        showarrow=False,
        xanchor='left',
        yanchor='middle',
        font=dict(family="Arial", size=12, color='black')
    ))
    
    # Percentage value
    legend_annotations.append(go.layout.Annotation(
        xref="paper", yref="paper",
        x=legend_box['x1'] - 0.02,
        y=y_center,
        text=f"{item['value']}%",
        showarrow=False,
        xanchor='right',
        yanchor='middle',
        font=dict(family="Arial", size=12, color='black')
    ))

# --- 6. Update layout and styling ---
fig.update_layout(
    title_text=None,  # No title in the original image
    font=dict(family="Arial"),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=20, r=20, t=20, b=20),
    autosize=False,
    width=800,
    height=550,
    shapes=legend_shapes,
    annotations=legend_annotations
)

# --- 7. Output the image ---
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)
print(f"Chart saved as {output_filename}")