import sys
import json
import os
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read and parse the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data, texts, and colors from the JSON structure
chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

# Initialize the figure
fig = go.Figure()

# Add a bar trace for each series in the data, in the specified order
for i, series in enumerate(chart_data['series']):
    # Format bar labels to be bold with a space as the thousands separator
    bar_labels = [f"<b>{val:,}</b>".replace(',', ' ') for val in series['y_values']]

    fig.add_trace(go.Bar(
        x=chart_data['x_values'],
        y=series['y_values'],
        name=series['name'],
        marker_color=colors[i],
        text=bar_labels,
        textposition='outside',
        textfont=dict(family='Arial', size=12, color='black'),
        cliponaxis=False  # Allow text to be drawn outside the axis range
    ))

# Configure the layout of the chart
fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    barmode='group',
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 15500],  # Set range to give space for text above bars
        tickvals=[0, 2500, 5000, 7500, 10000, 12500, 15000],
        showgrid=True,
        gridcolor='#dddddd',
        griddash='dot',
        zeroline=False,
        showline=False
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5,
        traceorder='normal'
    ),
    margin=dict(l=80, r=40, b=150, t=50), # Increased bottom margin for source and legend
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.98,
            y=-0.4,
            xanchor='right',
            yanchor='bottom',
            align='right',
            font=dict(family='Arial', size=12)
        )
    ]
)

# Define the output filename based on the input JSON filename
base_filename = os.path.basename(json_path).rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to {output_filename}")