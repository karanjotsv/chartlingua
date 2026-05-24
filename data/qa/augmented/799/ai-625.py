import sys
import json
import os
import plotly.graph_objects as go

# --- 1. Load data from JSON file provided as a command-line argument ---
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_file_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Failed to decode JSON from the file '{json_file_path}'.")
    sys.exit(1)

# --- 2. Extract data and text from the loaded JSON ---
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# --- 3. Create the Plotly figure ---
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=values,
    textposition='outside',
    marker_color=colors[0] if colors else None,
    cliponaxis=False  # Allow text to be drawn outside the plot area
))

# --- 4. Configure the layout ---
annotations = []
if texts.get("source_left"):
    annotations.append(
        dict(
            text=texts["source_left"],
            showarrow=False,
            xref="paper", yref="paper",
            x=0, y=-0.15,
            xanchor="left", yanchor="bottom",
            align="left"
        )
    )
if texts.get("source_right"):
    annotations.append(
        dict(
            text=texts["source_right"],
            showarrow=False,
            xref="paper", yref="paper",
            x=1, y=-0.15,
            xanchor="right", yanchor="bottom",
            align="right"
        )
    )

fig.update_layout(
    title_text=texts.get('title'),
    title_x=0.5,
    yaxis_title=texts.get('y_axis_title'),
    xaxis_title=texts.get('x_axis_title'),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        showgrid=True,
        gridcolor='#f0f0f0',
        linecolor='black',
        zeroline=False,
        tickmode='array',
        tickvals=categories,
        ticktext=categories
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='#e9e9e9',
        gridwidth=1,
        zeroline=False,
        linecolor='black',
        range=[0, 4100],
        tickvals=[0, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000]
    ),
    margin=dict(l=80, r=40, t=80, b=100),
    annotations=annotations
)

# --- 5. Output the chart as a PNG file ---
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")