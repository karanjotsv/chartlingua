import sys
import json
import plotly.graph_objects as go

# --- 1. Load Data from JSON ---
# The script requires the path to the JSON file as a command-line argument.
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
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

chart_data = chart_config['chart_data']
texts = chart_config['texts']
colors = chart_config['colors']

# --- 2. Create the Chart ---
fig = go.Figure()

# Add traces for each data series
for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        mode='lines',
        name='',  # Legend is disabled, direct labels are used
        line=dict(color=colors[i], width=2),
        hoverinfo='none'
    ))

# --- 3. Configure Layout and Styling ---
annotations = []
# Create annotations for line labels
for series in chart_data:
    annotations.append(
        dict(
            x=series['label_x'],
            y=series['label_y'],
            text=series['name'],
            showarrow=False,
            xanchor='left',
            yanchor='middle',
            font=dict(family="Arial", size=14, color="black")
        )
    )

# Create annotation for the source text
if texts.get('source'):
    annotations.append(
        dict(
            xref="paper",
            yref="paper",
            x=0,
            y=-0.15,
            text=texts['source'],
            showarrow=False,
            xanchor="left",
            yanchor="top",
            align="left",
            font=dict(family="Arial", size=10, color="grey")
        )
    )

fig.update_layout(
    title=dict(
        text=texts['title'],
        x=0.01,
        y=0.95,
        xanchor='left',
        yanchor='top',
        font=dict(family="Arial", size=20, color='black')
    ),
    yaxis=dict(
        title=texts['y_axis_title'],
        range=[0, 161],
        tickmode='array',
        tickvals=[0, 20, 40, 60, 80, 100, 120, 140, 160],
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        zeroline=False
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        range=[1989.5, 2021.5],
        tickmode='array',
        tickvals=[1990, 1995, 2000, 2005, 2010, 2015, 2020],
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=14, color="black"),
    showlegend=False,
    margin=dict(l=80, r=120, t=80, b=80),
    annotations=annotations
)


# --- 4. Output the Image ---
# Derive the output filename from the input JSON filename
if '.' in json_path:
    base_name = json_path.rsplit('.', 1)[0]
else:
    base_name = json_path

output_filename = f"{base_name}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")