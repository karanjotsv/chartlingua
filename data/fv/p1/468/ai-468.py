import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

# Read data from JSON file
json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# --- Extract data from the JSON structure ---
main_pie_data = chart_info['main_pie_data']
secondary_pie_data = chart_info['secondary_pie_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Prepare data for Plotly traces
main_labels = [d['label'] for d in main_pie_data]
main_values = [d['value'] for d in main_pie_data]

secondary_labels = [d['label'] for d in secondary_pie_data]
secondary_values = [d['value'] for d in secondary_pie_data]

# --- Create the plot figure ---
fig = go.Figure()

# Add the first (main) pie chart trace
fig.add_trace(go.Pie(
    labels=main_labels,
    values=main_values,
    domain={'x': [0, 0.48], 'y': [0, 1]},
    marker={
        'colors': colors['main_pie'],
        'line': {'color': 'black', 'width': 2}
    },
    texttemplate='%{value}%',
    textposition='inside',
    insidetextfont={'family': 'Arial', 'size': 18, 'color': 'black'},
    hoverinfo='label+percent',
    sort=False,
    direction='clockwise',
    rotation=105
))

# Add the second (secondary) pie chart trace
fig.add_trace(go.Pie(
    labels=secondary_labels,
    values=secondary_values,
    domain={'x': [0.52, 1], 'y': [0, 1]},
    marker={
        'colors': colors['secondary_pie'],
        'line': {'color': 'black', 'width': 2}
    },
    texttemplate='%{value}%',
    textposition='inside',
    insidetextfont={'family': 'Arial', 'size': 18, 'color': 'black'},
    hoverinfo='label+percent',
    sort=False,
    direction='clockwise',
    rotation=135
))

# --- Update layout and styling ---
fig.update_layout(
    title_text=texts.get('title'),
    showlegend=True,
    legend=dict(
        font=dict(
            family='Arial',
            size=12,
            color='white'
        )
    ),
    paper_bgcolor='black',
    plot_bgcolor='black',
    font=dict(family='Arial', color='white'),
    width=1000,
    height=500,
    margin=dict(l=20, r=160, t=60, b=20) # Increased right margin for legend
)

# --- Generate and save the output image ---
output_filename = json_path.with_suffix('.png').name
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")