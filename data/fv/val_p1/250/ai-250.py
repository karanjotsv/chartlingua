import sys
import json
import plotly.graph_objects as go

# Load data from the JSON file provided as a command-line argument
json_path = sys.argv[1]
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extract data elements from the JSON structure
chart_data = data['chart_data']
texts = data['texts']
colors = data['colors']

# Prepare data for Plotly trace
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure object
fig = go.Figure()

# Add the donut chart trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    hole=0.6,
    marker=dict(
        colors=colors,
        line=dict(color='white', width=4)
    ),
    texttemplate='%{value}%',
    textposition='inside',
    insidetextfont=dict(family="Arial", size=16, color='white'),
    hoverinfo='label+percent',
    sort=False,
    direction='clockwise'
))

# Configure the layout of the chart
fig.update_layout(
    title_text=texts['title'],
    title_x=0.5,
    title_font=dict(family="Arial", size=18, color='black'),
    showlegend=True,
    legend=dict(
        x=0.5,
        y=0.15,
        xanchor='center',
        yanchor='top',
        bgcolor='rgba(0,0,0,0)',
        font=dict(family="Arial", size=12)
    ),
    paper_bgcolor='white',
    plot_bgcolor='white',
    font=dict(family="Arial", size=12, color='black'),
    margin=dict(l=20, r=20, t=100, b=140)
)

# Derive the output filename from the input JSON path
output_filename = json_path.rsplit('.', 1)[0] + '.png'

# Save the figure to a high-resolution PNG file
fig.write_image(output_filename, scale=2, width=500, height=650)