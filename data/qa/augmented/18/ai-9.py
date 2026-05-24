import sys
import json
import os
import plotly.graph_objects as go

# --- 1. Load Data from JSON ---
# The script expects the JSON file path as a command-line argument.
if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_file_path}'")
    sys.exit(1)

# Extract data and texts from the loaded JSON
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])
legend_labels = texts.get('legend_labels', [])

# --- 2. Prepare Data for Plotting ---
categories = [item['category'] for item in chart_data]
series_data = []
for i in range(len(legend_labels)):
    series_data.append([item['values'][i] for item in chart_data])

# --- 3. Create the Chart ---
fig = go.Figure()

# Add a bar trace for each data series
for i, label in enumerate(legend_labels):
    fig.add_trace(go.Bar(
        name=label,
        x=categories,
        y=series_data[i],
        marker_color=colors[i],
        text=series_data[i],
        textposition='outside',
        textfont=dict(family="Arial", size=12, color='black'),
        cliponaxis=False
    ))

# --- 4. Configure Layout and Styling ---
fig.update_layout(
    barmode='group',
    plot_bgcolor='white',
    font=dict(family="Arial", size=12, color='black'),
    margin=dict(l=80, r=40, t=50, b=150),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=[0, 850],
        tickvals=[0, 200, 400, 600, 800],
        gridcolor='#e9e9e9',
        showgrid=True,
        zeroline=False
    ),
    xaxis=dict(
        tickfont=dict(size=11),
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    legend=dict(
        orientation='h',
        yanchor='top',
        y=-0.25,
        xanchor='center',
        x=0.5,
        traceorder='normal',
        font=dict(size=12)
    )
)

# Add source annotation at the bottom right
fig.add_annotation(
    text=texts.get('source'),
    align='right',
    showarrow=False,
    xref='paper',
    yref='paper',
    x=1.0,
    y=-0.4,
    xanchor='right',
    yanchor='bottom',
    font=dict(size=11)
)

# --- 5. Output the Chart ---
# Derive the output filename from the input JSON file path
base_name = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_name}.png"

# Save the figure to a high-resolution PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")