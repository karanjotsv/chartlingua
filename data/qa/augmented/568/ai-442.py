import sys
import json
import os
import plotly.graph_objects as go

# --- 1. Load Data from JSON ---
# The script expects the JSON file path as the first command-line argument.
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts from the loaded JSON
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# --- 2. Create Figure ---
fig = go.Figure()

# --- 3. Add Traces ---
# Iterate through each data series in the JSON and add it to the figure
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=series.get('values'),
        y=series.get('categories'),
        orientation='h',
        marker=dict(color=colors[i % len(colors)]),
        text=series.get('values'),
        texttemplate='%{text:,}',
        textposition='outside',
        cliponaxis=False  # Prevents text labels from being clipped
    ))

# --- 4. Configure Layout ---
fig.update_layout(
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    showlegend=False,
    # Set y-axis to reversed to show the highest value at the top, matching the JSON order
    yaxis=dict(
        autorange="reversed",
        showgrid=False,
        zeroline=False,
        ticks='outside',
        ticklen=5,
        tickcolor='lightgrey'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#E5E5E5',
        griddash='dot',
        zeroline=False,
        range=[0, 8500], # Set range to give space for outside text labels
        tickvals=[0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000],
        ticktext=['0', '1 000', '2 000', '3 000', '4 000', '5 000', '6 000', '7 000', '8 000']
    ),
    # Adjust margins to prevent labels from being cut off
    margin=dict(l=100, r=80, t=40, b=80),
)

# Add source annotation at the bottom right
if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        xref="paper", yref="paper",
        x=0.98, y=-0.12,
        showarrow=False,
        xanchor='right',
        yanchor='top',
        align='right',
        font=dict(size=12, color="grey")
    )

# --- 5. Export Figure ---
# Derive output filename from the input JSON filename
base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")