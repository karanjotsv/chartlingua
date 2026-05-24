import sys
import json
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Load data from JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

categories = [item['category'] for item in data]
values = [item['value'] for item in data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors,
    marker_line_color='black',
    marker_line_width=1.5,
    cliponaxis=False
))

# Add annotations for bar values
for i, item in enumerate(data):
    fig.add_annotation(
        x=item['category'],
        y=item['value'],
        text=f"<b>{item['value']:,}</b>",
        showarrow=False,
        yshift=15,
        font=dict(family="Arial", size=20, color="black")
    )

# Update layout
fig.update_layout(
    title=dict(
        text=f"<b>{texts['title']}</b>",
        x=0.5,
        y=0.95,
        xanchor='center',
        yanchor='top',
        font=dict(family="Arial", size=24, color="black")
    ),
    xaxis=dict(
        tickfont=dict(family="Arial", size=18),
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 6000],
        dtick=1000,
        tickfont=dict(family="Arial", size=18),
        showgrid=True,
        gridcolor='LightGray',
        gridwidth=1,
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    font=dict(family="Arial"),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(t=120, b=120, l=80, r=40)
)

# Add source annotation
fig.add_annotation(
    text=texts['source'],
    xref="paper",
    yref="paper",
    x=0.5,
    y=-0.25,
    showarrow=False,
    xanchor='center',
    yanchor='top',
    font=dict(family="Arial", size=22, color="black")
)

# Generate output filename and save the image
output_filename = json_path.rsplit('.', 1)[0] + '.png'
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")