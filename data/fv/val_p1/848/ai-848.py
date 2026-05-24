import sys
import json
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_filepath = sys.argv[1]

# Load data from the specified JSON file
try:
    with open(json_filepath, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_filepath}")
    sys.exit(1)

# Extract data for plotting
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Prepare data specifically for the Pie chart
# The legend text is formatted using HTML to match the original's style
labels = [f"{item['category']}<br><u>{item['value']}%</u>" for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart trace
pie_trace = go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=1)),
    hoverinfo='label+percent',
    textinfo='none',
    sort=False,
    direction='clockwise'
)

# Create the figure
fig = go.Figure(data=[pie_trace])

# Update layout for a clean and accurate look
fig.update_layout(
    title_text=texts['title'],
    font=dict(family="Arial", size=12),
    showlegend=True,
    legend=dict(
        x=0.98,
        y=0.8,
        xanchor='left',
        yanchor='top'
    ),
    margin=dict(l=20, r=150, t=50, b=20),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

# Determine the output filename from the input JSON path
if json_filepath.endswith('.json'):
    output_filename = json_filepath[:-5] + '.png'
else:
    output_filename = json_filepath + '.png'

# Save the figure to a high-resolution PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to {output_filename}")