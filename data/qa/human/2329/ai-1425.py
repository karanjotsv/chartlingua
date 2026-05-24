import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load data from JSON file provided as a command-line argument ---
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# --- 2. Extract data and text from the loaded configuration ---
data = chart_config['chart_data']
texts = chart_config['texts']
colors = chart_config['colors']
categories = data['categories']
series_list = data['series']

# --- 3. Create the Plotly figure ---
fig = go.Figure()

# --- 4. Add a bar trace for each data series ---
for i, series in enumerate(series_list):
    fig.add_trace(go.Bar(
        x=categories,
        y=series['data'],
        name=series['name'],
        marker_color=colors[i],
        text=series['data'],
        textposition='outside',
        textfont=dict(family="Arial", size=12, color='black'),
        cliponaxis=False  # Prevents text labels for high values from being clipped
    ))

# --- 5. Configure the layout, axes, and annotations ---

# Combine title and subtitle
title_parts = []
if texts.get('title'):
    title_parts.append(texts['title'])
if texts.get('subtitle'):
    # Use HTML for subtitle styling to make it smaller and grey
    title_parts.append(f"<br><span style='font-size:0.8em;color:grey;'>{texts['subtitle']}</span>")
final_title = "".join(title_parts)

fig.update_layout(
    barmode='group',
    font=dict(family="Arial"),
    title=dict(text=final_title, x=0.05, xanchor='left'),
    xaxis_title=texts['x_axis_title'],
    yaxis_title=texts['y_axis_title'],
    plot_bgcolor='white',
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=80, r=40, b=130, t=50, pad=4),
    xaxis=dict(
        showline=True,
        linewidth=1,
        linecolor='black',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        range=[0, 600],
        showgrid=True,
        gridcolor='#E5E5E5',
        zeroline=False,
        tickfont=dict(size=12)
    ),
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.4,
            xanchor='right',
            yanchor='bottom',
            align='right',
            font=dict(family="Arial", size=10, color='grey')
        )
    ]
)

# --- 6. Generate and save the output image ---
input_path = pathlib.Path(json_path)
output_filename = input_path.with_suffix(".png")
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")