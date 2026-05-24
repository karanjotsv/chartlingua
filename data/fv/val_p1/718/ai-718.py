import sys
import json
import plotly.graph_objects as go

# --- 1. Load Data from JSON ---
# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read the JSON data file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from the file '{json_path}'.")
    sys.exit(1)

# Extract data, texts, and colors from the loaded JSON
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for Plotly
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# --- 2. Create the Plotly Figure ---
fig = go.Figure()

# Add the pie chart trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='#FFFFFF', width=2)
    ),
    textinfo='percent',
    textfont=dict(
        family="Arial",
        size=16,
        color='black'
    ),
    insidetextorientation='horizontal',
    sort=False,  # This is crucial to preserve the original data order
    direction='clockwise',
    domain=dict(x=[0.35, 1.0]) # Reserve left 35% of the space for the legend
))

# --- 3. Configure Layout and Styling ---
# Combine title and subtitle if they exist
title_text = ""
if texts.get("title"):
    title_text += texts["title"]
if texts.get("subtitle"):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    title_text=title_text,
    font_family="Arial",
    showlegend=True,
    legend=dict(
        x=0,
        y=1,
        xanchor='left',
        yanchor='top',
        traceorder='normal',
        font=dict(
            family="Arial",
            size=12
        ),
        bgcolor='rgba(0,0,0,0)' # Transparent background
    ),
    margin=dict(l=20, r=20, t=50, b=50),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

# Add source/note as an annotation if it exists
if texts.get("source"):
    fig.add_annotation(
        showarrow=False,
        text=texts["source"],
        xref="paper",
        yref="paper",
        x=0,
        y=-0.08,
        xanchor="left",
        yanchor="top",
        font=dict(family="Arial", size=10)
    )

# --- 4. Output the Image ---
# Derive the output filename from the input JSON path
# e.g., 'path/to/my_chart.json' -> 'my_chart.png'
base_name = json_path.split('/')[-1].split('\\')[-1]
if '.' in base_name:
    base_name = base_name.rsplit('.', 1)[0]
output_filename = f"{base_name}.png"

# Save the figure to a PNG file with a high resolution
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")