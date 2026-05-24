import sys
import json
from pathlib import Path
import plotly.graph_objects as go

# --- 1. Load Data from JSON ---
# The script requires the path to the JSON file as a command-line argument.
if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# --- 2. Extract Data and Texts ---
chart_data = config['chart_data']
categories = config['categories']
texts = config['texts']
colors = config['colors']

# --- 3. Create the Plot ---
fig = go.Figure()

# Add a trace for each data series
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        y=categories,
        x=series['x'],
        name=series['name'],
        orientation='h',
        marker=dict(color=colors[i], line_width=0),
        text=series['text'],
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(color='white', size=14, family='Arial')
    ))

# --- 4. Configure Layout and Styling ---
fig.update_layout(
    barmode='stack',
    paper_bgcolor='white',
    plot_bgcolor='white',
    showlegend=False,
    font=dict(family="Arial"),
    margin=dict(l=150, r=40, t=180, b=120),
    title=dict(
        text=f"<b>{texts['title']}</b><br><span style='font-size:16px; color:#555555;'>{texts['subtitle']}</span>",
        y=0.98,
        x=0.01,
        xanchor='left',
        yanchor='top',
        font=dict(size=22, family='Arial', color='black')
    ),
    xaxis=dict(
        visible=False,
        range=[0, sum(chart_data[i]['x'][0] for i in range(len(chart_data))) + 5] # Ensure space for labels
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        ticks='',
        autorange='reversed',  # Display categories from top to bottom as they appear in the JSON
        tickfont=dict(size=16)
    )
)

# --- 5. Add Annotations ---
annotations = []

# Add series labels above the first bar
first_bar_values = [series['x'][0] for series in chart_data]
label_x_positions = [first_bar_values[0] / 2, first_bar_values[0] + (first_bar_values[1] / 2)]

for i, label in enumerate(texts['series_labels']):
    annotations.append(dict(
        xref='x', yref='y',
        x=label_x_positions[i],
        y=categories[0],  # Position relative to the first category
        yshift=50,        # Shift upwards in pixels
        text=f"<b>{label}</b>",
        showarrow=False,
        font=dict(size=14, family='Arial', color='black'),
        align='center'
    ))

# Add source and footer note at the bottom
annotations.append(dict(
    xref='paper', yref='paper',
    x=0, y=-0.22,  # Position below the chart area
    xanchor='left', yanchor='top',
    align='left',
    text=f"<span style='color:#555555;font-size:12px;'>{texts['source']}</span><br><b>{texts['footer']}</b>",
    showarrow=False,
    font=dict(family='Arial')
))

fig.update_layout(annotations=annotations)

# --- 6. Export the Image ---
output_filename = json_path.stem + ".png"
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")