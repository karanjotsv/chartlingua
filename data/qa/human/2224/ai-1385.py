import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load Configuration from JSON ---
# The script expects the path to the JSON file as the first command-line argument.
if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

# Extract data and text from the configuration
chart_data = config.get('chart_data', {})
texts = config.get('texts', {})
colors = config.get('colors', [])
categories = chart_data.get('categories', [])
series_list = chart_data.get('series', [])

# --- 2. Create the Chart Figure ---
fig = go.Figure()

# Add a bar trace for each data series
for i, series in enumerate(series_list):
    fig.add_trace(go.Bar(
        x=categories,
        y=series.get('data', []),
        name=series.get('name', ''),
        marker_color=colors[i % len(colors)],
        text=series.get('data', []),
        textposition='outside',
        textfont=dict(family="Arial", size=12, color='black')
    ))

# --- 3. Configure Layout and Styling ---
fig.update_layout(
    barmode='group',
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    paper_bgcolor='#f8f9fa',
    margin=dict(l=80, r=40, b=120, t=40),
    title_text=texts.get('title'),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 105],
        tickvals=[0, 20, 40, 60, 80, 100],
        showgrid=True,
        gridcolor='lightgrey',
        griddash='dot',
        zeroline=False
    )
)

# Add vertical separator lines between category groups
if len(categories) > 1:
    for i in range(len(categories) - 1):
        fig.add_vline(x=i + 0.5, line_width=1, line_color="lightgrey")

# Add annotations for note and source
if texts.get('note'):
    fig.add_annotation(
        text=f"ⓘ {texts.get('note')}",
        align='left',
        showarrow=False,
        xref='paper', yref='paper',
        x=0, y=-0.4,
        font=dict(color=colors[0]) # Use the primary color for the note
    )

if texts.get('source'):
    fig.add_annotation(
        text=texts.get('source'),
        align='right',
        showarrow=False,
        xref='paper', yref='paper',
        x=1.0, y=-0.4,
        xanchor='right'
    )

# --- 4. Output the Chart to a PNG File ---
output_path = pathlib.Path(json_path).with_suffix('.png')
fig.write_image(str(output_path), scale=2)
print(f"Chart saved to {output_path}")