import sys
import json
import pathlib
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

# Get file path from command-line argument
json_file_path = pathlib.Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Load data from JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# --- Chart Generation ---

# Extract data for convenience
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

# Create subplots figure: 2 rows, 2 columns.
# Bottom-left cell is empty to make space for the legend.
fig = make_subplots(
    rows=2,
    cols=2,
    specs=[[{'type': 'pie'}, {'type': 'pie'}],
           [{}, {'type': 'pie'}]],
    subplot_titles=texts['subplot_titles']
)

# Define subplot positions
positions = [(1, 1), (1, 2), (2, 2)]

# Add a pie chart for each year
for i, entry in enumerate(data):
    row, col = positions[i]
    fig.add_trace(go.Pie(
        labels=texts['legend_labels'],
        values=entry['values'],
        name=entry['year'],
        marker=dict(
            colors=colors,
            line=dict(color='#000000', width=2)
        ),
        hoverinfo='label+percent',
        textinfo='value',
        texttemplate='<b>%{value}%</b>',
        textfont=dict(color='white', size=18, family="Arial"),
        sort=False,  # Preserve original data order
        direction='clockwise'
    ), row=row, col=col)

# --- Layout and Styling ---

fig.update_layout(
    # Main title
    title_text=f"<b>{texts['title']}</b>",
    title_x=0.5,
    title_font=dict(family="Arial", size=24),

    # Global font
    font=dict(family="Arial", size=14),

    # Legend
    showlegend=True,
    legend_title_text=f"<b>{texts['legend_title']}</b>",
    legend=dict(
        x=0.23,
        y=0.45,
        xanchor='center',
        yanchor='top',
        bgcolor='rgba(255,255,255,1)',
        bordercolor='black',
        borderwidth=1.5,
        font=dict(size=16)
    ),

    # Subplot titles
    annotations=[
        dict(
            text=a.text,
            x=a.x,
            y=a.y,
            font=dict(family="Arial", size=20, color='black'),
            showarrow=False
        ) for a in fig.layout.annotations
    ],
    
    # Margins
    margin=dict(l=20, r=20, t=100, b=20),
    width=800,
    height=700
)

# --- Output ---

# Derive output filename from JSON path
output_filename = json_file_path.with_suffix('.png').name

# Save image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")