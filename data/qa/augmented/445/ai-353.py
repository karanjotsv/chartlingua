import sys
import json
import plotly.graph_objects as go
import os

# --- 1. Load Data from JSON ---
# The script expects the JSON file path as the sole command-line argument.
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
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

chart_data = chart_config['chart_data']
texts = chart_config['texts']
colors = chart_config['colors']

# --- 2. Create the Figure ---
fig = go.Figure()

# --- 3. Add Traces (Bars) ---
# Iterate through each data series in the JSON file
for i, series in enumerate(chart_data):
    # Format the text labels to match the original (space as thousands separator)
    text_labels = [f'{val:,}'.replace(',', ' ') for val in series['y']]
    
    fig.add_trace(go.Bar(
        x=series['x'],
        y=series['y'],
        name=series.get('name', ''),
        marker_color=colors[i % len(colors)],
        text=text_labels,
        textposition='outside',
        textfont=dict(
            family="Arial",
            size=12,
            color='black'
        ),
        cliponaxis=False # Allows text to render outside the plot area
    ))

# --- 4. Configure Layout ---
# Combine title and subtitle if they exist
title_text = ""
if texts.get("title"):
    title_text += texts["title"]
if texts.get("subtitle"):
    title_text += f'<br><sub>{texts["subtitle"]}</sub>'

fig.update_layout(
    title_text=title_text,
    yaxis_title_text=texts.get('y_axis_title'),
    xaxis_title_text=texts.get('x_axis_title'),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='#f8f9fa',
    showlegend=False,
    margin=dict(l=60, r=40, t=50, b=100), # Increased bottom margin for source/note
    xaxis=dict(
        showgrid=False,
        tickvals=chart_data[0]['x'],
        tickangle=0,
        linecolor='black',
        linewidth=1,
        ticks='outside'
    ),
    yaxis=dict(
        range=[0, 3000],
        tickvals=[0, 500, 1000, 1500, 2000, 2500, 3000],
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        zeroline=False,
        title_standoff=10
    )
)

# --- 5. Add Annotations for Source and Note ---
annotations = []
if texts.get("note"):
    annotations.append(dict(
        xref='paper', yref='paper',
        x=0, y=-0.2,
        xanchor='left', yanchor='top',
        text=texts['note'],
        showarrow=False,
        font=dict(family="Arial", size=12, color='#007bff') # Assuming blue for link-like text
    ))
if texts.get("source"):
    annotations.append(dict(
        xref='paper', yref='paper',
        x=1, y=-0.2,
        xanchor='right', yanchor='top',
        text=texts['source'],
        showarrow=False,
        font=dict(family="Arial", size=12, color='grey')
    ))

fig.update_layout(annotations=annotations)


# --- 6. Output the Image ---
# Derive the output filename from the input JSON filename
base_name = os.path.basename(json_path).rsplit('.', 1)[0]
output_filename = f"{base_name}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to '{output_filename}'")