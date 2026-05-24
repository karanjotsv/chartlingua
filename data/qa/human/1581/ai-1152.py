import sys
import json
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Load data from the specified JSON file
json_path = sys.argv[1]
with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Extract data, texts, and colors from the loaded configuration
chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

# Prepare data for plotting (categories and values)
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Initialize a Plotly Figure
fig = go.Figure()

# Add the horizontal bar trace to the figure
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors['bars']),
    text=[f"{v} kg" for v in values],
    textposition='outside',
    cliponaxis=False,
    textfont=dict(family="Arial", size=14, color='#333333')
))

# Construct the list of annotations for source, note, and logo
annotations = [
    dict(
        xref='paper', yref='paper',
        x=0.0, y=-0.12,
        xanchor='left', yanchor='top',
        text=texts['source'],
        showarrow=False,
        font=dict(family="Arial", size=12, color='#666666')
    ),
    dict(
        xref='paper', yref='paper',
        x=1.0, y=-0.12,
        xanchor='right', yanchor='top',
        text=texts['note'],
        showarrow=False,
        font=dict(family="Arial", size=12, color='#666666')
    )
]
if texts.get('logo_text'):
    annotations.append(dict(
        xref='paper', yref='paper',
        x=0.99, y=1.07,
        xanchor='right', yanchor='bottom',
        text=f"<b>{texts['logo_text']}</b>",
        showarrow=False,
        font=dict(family="Arial", size=10, color='white'),
        bgcolor=colors['logo_background'],
        borderpad=4,
        align='center'
    ))

# Update the figure layout for a clean, professional appearance
fig.update_layout(
    title=dict(
        text=f"<b>{texts['title']}</b>",
        y=0.97,
        x=0.01,
        xanchor='left',
        yanchor='top',
        font=dict(family="Arial", size=22, color='#333333')
    ),
    xaxis=dict(
        showgrid=True,
        gridcolor='#d9d9d9',
        gridwidth=1,
        griddash='dot',
        showline=False,
        zeroline=False,
        ticksuffix=' kg',
        showticklabels=True,
        automargin=True,
        range=[0, max(values) * 1.18]  # Ensure space for text labels
    ),
    yaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=True,
        autorange='reversed',  # Display categories from top to bottom
        ticks='outside',
        tickcolor='white',
        ticklen=10,
        automargin=True
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    font=dict(family="Arial", size=14, color='black'),
    margin=dict(t=100, b=80),
    annotations=annotations,
    height=500
)

# Generate the output filename and save the chart as a PNG image
output_filename = json_path.rsplit('.', 1)[0] + '.png'
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")