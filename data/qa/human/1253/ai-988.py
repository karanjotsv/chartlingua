import sys
import json
import plotly.graph_objects as go

# Check for command-line argument for the JSON file path
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts for plotting
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

categories = [d['category'] for d in chart_data]
values = [d['value'] for d in chart_data]
max_value = max(values) if values else 0

# Create the figure object
fig = go.Figure()

# Add the horizontal bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors),
    text=values,
    texttemplate='%{text:.2f}%',
    textposition='outside',
    cliponaxis=False,
    textfont=dict(family='Arial', size=12, color='black'),
    hoverinfo='none'
))

# Update the layout for a clean, professional appearance
fig.update_layout(
    title=dict(
        text=f"<b>{texts['title']}</b>",
        font=dict(family='Arial', size=24, color='#333333'),
        x=0.01,
        y=0.95,
        xanchor='left',
        yanchor='top'
    ),
    xaxis=dict(
        showgrid=True,
        gridcolor='#E0E0E0',
        gridwidth=1,
        griddash='dash',
        zeroline=False,
        showline=False,
        ticks='outside',
        tickfont=dict(family='Arial', size=14, color='#333333'),
        ticksuffix='%',
        range=[0, max_value * 1.15]
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        ticks='',
        tickfont=dict(family='Arial', size=14, color='#333333'),
        autorange='reversed'
    ),
    font=dict(family="Arial"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=100, r=60, b=80, t=100)
)

# Add annotations for the source note and credits at the bottom
if texts.get('source_note'):
    fig.add_annotation(
        text=texts['source_note'],
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0,
        y=-0.15,
        xanchor='left',
        yanchor='top',
        font=dict(family='Arial', size=12, color='#666666')
    )

if texts.get('owid_credit'):
    fig.add_annotation(
        text=texts['owid_credit'],
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1,
        y=-0.15,
        xanchor='right',
        yanchor='top',
        font=dict(family='Arial', size=12, color='#666666')
    )

# Derive output filename from input JSON path and save the image
base_path = sys.argv[1]
filename_with_ext = base_path.split('/')[-1].split('\\')[-1]
base_filename = filename_with_ext.rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")