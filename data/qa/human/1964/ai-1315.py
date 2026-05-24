import sys
import json
import os
import plotly.graph_objects as go

# --- 1. Load data from JSON file ---
# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

# --- 2. Extract data and configuration from the loaded JSON ---
labels = [item['label'] for item in chart_data['chart_data']]
values = [item['value'] for item in chart_data['chart_data']]
colors = chart_data['colors']
texts = chart_data['texts']

# --- 3. Create the Plotly figure ---
fig = go.Figure()

# Add the pie trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='white', width=1)),
    hoverinfo='label+percent',
    textinfo='none',  # Custom text template will be used instead
    texttemplate='%{label} %{value}',
    textposition='outside',
    sort=False,  # Preserve the order from the JSON file
    direction='clockwise',
    rotation=90  # Start the first slice at the 12 o'clock position
))

# --- 4. Configure the layout ---
annotations = []
# Add source text annotation if it exists
if texts.get('source'):
    annotations.append(
        go.layout.Annotation(
            text=texts['source'],
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.99,
            y=0.01,
            xanchor='right',
            yanchor='bottom',
            font=dict(
                family="Arial",
                size=12,
                color="#888888"
            )
        )
    )

fig.update_layout(
    title_text=None,  # No title
    showlegend=False,
    font=dict(
        family="Arial",
        size=14,
        color="black"
    ),
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(l=80, r=80, t=50, b=80), # Add margins to prevent clipping
    annotations=annotations
)

# --- 5. Output the chart as a PNG file ---
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")