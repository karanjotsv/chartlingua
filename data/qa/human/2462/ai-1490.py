import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load data from JSON file ---
# The script expects the JSON file path as the first command-line argument.
if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data and texts for convenience
chart_data = chart_info["chart_data"]
texts = chart_info["texts"]
colors = chart_info["colors"]
x_labels = texts["x_axis_labels"]

# --- 2. Create the Plotly figure ---
fig = go.Figure()

# Add a bar trace for each data series
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=x_labels,
        y=series["values"],
        name=series["name"],
        marker_color=colors[i],
        text=[f'<b>{v}%</b>' for v in series["values"]],
        textposition='inside',
        textfont=dict(color='white', size=14, family='Arial'),
        hoverinfo='none'
    ))

# --- 3. Configure the layout ---
fig.update_layout(
    barmode='stack',
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    xaxis=dict(
        title_text=texts["x_axis_title"],
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts["y_axis_title"],
        range=[0, 125],
        tickvals=[0, 25, 50, 75, 100, 125],
        ticksuffix='%',
        showgrid=True,
        gridcolor='#E5E5E5',
        gridwidth=1,
        zeroline=False,
        title_font=dict(size=14),
        tickfont=dict(size=12)
    ),
    legend=dict(
        orientation='h',
        yanchor='top',
        y=-0.2,
        xanchor='center',
        x=0.5,
        font=dict(size=12)
    ),
    margin=dict(l=80, r=40, t=40, b=150),
    annotations=[
        dict(
            text=texts["source"],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.3, # Positioned below the legend
            xanchor='right',
            yanchor='top',
            font=dict(size=11, color='#666666')
        )
    ]
)

# --- 4. Output the figure to a PNG file ---
# The output filename is derived from the input JSON filename.
output_filename = json_path.with_suffix(".png")
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")