import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load Data from JSON ---
# The script requires the JSON file path as a command-line argument.
if len(sys.argv) < 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data from the loaded JSON
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# --- 2. Prepare Data for Plotting ---
y_values = [d['emissions_per_person'] for d in chart_data]
widths = [d['population_billions'] for d in chart_data]

# Calculate x-axis center points for each bar
x_centers = []
current_x = 0
for w in widths:
    x_centers.append(current_x + w / 2.0)
    current_x += w

# --- 3. Create the Chart ---
fig = go.Figure()

# Add the variwide bar trace
fig.add_trace(go.Bar(
    x=x_centers,
    y=y_values,
    width=widths,
    marker=dict(
        color=colors,
        line=dict(color='#808080', width=2)
    ),
    showlegend=False
))

# --- 4. Add Annotations ---
# Add category labels rotated above each bar
for i, d in enumerate(chart_data):
    fig.add_annotation(
        x=x_centers[i],
        y=y_values[i],
        text=d['category'],
        showarrow=False,
        textangle=-55,
        xanchor='left',
        yanchor='bottom',
        yshift=5,
        font=dict(family="Arial", size=14)
    )

# Add subtitle annotations
fig.add_annotation(
    x=3.0, y=18.5,
    text=texts['subtitle_1'],
    showarrow=False,
    xref='x', yref='y',
    xanchor='left',
    font=dict(family="Arial", size=14)
)

fig.add_annotation(
    x=3.0, y=15,
    text=texts['subtitle_2'],
    showarrow=False,
    xref='x', yref='y',
    xanchor='left',
    align='left',
    font=dict(family="Arial", size=20)
)


# --- 5. Configure Layout and Styling ---
fig.update_layout(
    title=dict(
        text=texts['title'],
        x=0.5,
        font=dict(size=28)
    ),
    xaxis=dict(
        title=texts['x_axis_title'],
        range=[0, 8],
        tickmode='array',
        tickvals=[1, 2, 3, 4, 5, 6, 7, 8],
        ticktext=['1B', '2B', '3B', '4B', '5B', '6B', '7B', '8B'],
        showgrid=False,
        zeroline=True,
        showline=True,
        linecolor='black',
        ticks='outside',
        mirror=True
    ),
    yaxis=dict(
        title=texts['y_axis_title'],
        range=[0, 22],
        showgrid=True,
        gridcolor='lightgrey',
        zeroline=True,
        showline=True,
        linecolor='black',
        ticks='outside',
        mirror=True
    ),
    font=dict(
        family="Arial",
        size=16
    ),
    xaxis_title_font_size=20,
    yaxis_title_font_size=20,
    plot_bgcolor='white',
    paper_bgcolor='#f0f0f0',
    margin=dict(l=100, r=40, t=100, b=80)
)

# --- 6. Output the Image ---
output_filename = json_path.stem + ".png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")