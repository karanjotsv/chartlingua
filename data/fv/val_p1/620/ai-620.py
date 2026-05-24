import sys
import json
import pathlib
import plotly.graph_objects as go

# Check if a file path is provided
if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = pathlib.Path(sys.argv[1])

# Check if the JSON file exists
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read the JSON data
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_data_json = json.load(f)

# Extract data from the JSON object
chart_data = chart_data_json['chart_data']
texts = chart_data_json['texts']
colors = chart_data_json['colors']

# Initialize the figure
fig = go.Figure()

# Add a bar trace for each category
for i, item in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=[item['category']],
        y=[item['value']],
        name=item['category'],
        marker_color=colors[i],
        error_y=dict(
            type='data',
            array=[item['error']],
            visible=True,
            color='dimgray',
            thickness=1.5
        ),
        text=[item['value']],
        textposition='inside',
        textfont=dict(
            family="Arial",
            size=16,
            color='white' if item['value'] > 0 else 'black'
        ),
        insidetextanchor='middle',
        width=0.6
    ))

# Update layout for a clean and accurate representation
fig.update_layout(
    font=dict(family="Arial", size=12, color="dimgray"),
    plot_bgcolor='white',
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5,
        traceorder='normal',
        itemsizing='constant',
        font=dict(size=14, color='black')
    ),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        title_font=dict(size=14, color='black'),
        showticklabels=False,
        zeroline=False,
        showline=False,
        title_standoff=15
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        title_font=dict(size=14, color='black'),
        range=[-250, 650],
        tickmode='array',
        tickvals=[-200, 0, 200, 400, 600],
        gridcolor='#e0e0e0',
        zeroline=True,
        zerolinecolor='black',
        zerolinewidth=1,
        title_standoff=10
    ),
    margin=dict(l=60, r=20, t=80, b=80),
    barmode='group'
)

# Define the output filename based on the input JSON filename
output_filename = json_file_path.with_suffix('.png')

# Save the figure as a high-resolution PNG image
fig.write_image(str(output_filename), scale=2)

print(f"Chart saved to {output_filename}")