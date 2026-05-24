import sys
import json
import plotly.graph_objects as go

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Load data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: The file {json_path} was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file {json_path} is not a valid JSON.")
    sys.exit(1)


# Extract data and texts from the loaded JSON
chart_data = chart_config['chart_data']
texts = chart_config['texts']
colors = chart_config['colors']

# Prepare data for Plotly (Plotly plots horizontal bars from bottom to top)
# We reverse the lists to match the visual order of the original image (top to bottom)
y_data = [item['category'] for item in chart_data][::-1]
x_data = [item['value'] for item in chart_data][::-1]
colors_reversed = colors[::-1]

# Prepare text labels for bars, with special formatting for the top bar
text_labels = []
for item in chart_data:
    if item['value'] == 1310000:
        text_labels.append("1.31 million")
    else:
        text_labels.append(f"{item['value']:,}")
text_labels_reversed = text_labels[::-1]


# Create the figure
fig = go.Figure()

# Add the horizontal bar trace
fig.add_trace(go.Bar(
    y=y_data,
    x=x_data,
    orientation='h',
    marker=dict(color=colors_reversed),
    text=text_labels_reversed,
    textposition='outside',
    textfont=dict(family='Arial', size=12, color='#444444'),
    cliponaxis=False  # Prevents text labels from being clipped
))

# Update layout
fig.update_layout(
    title=dict(
        text=f"<b>{texts['title']}</b><br><span style='font-size: 15px; color: #555555;'>{texts['subtitle']}</span>",
        x=0.01,
        y=0.98,
        xanchor='left',
        yanchor='top',
        font=dict(size=22)
    ),
    font=dict(family="Arial"),
    xaxis=dict(
        showgrid=True,
        gridcolor='#e0e0e0',
        griddash='dot',
        zeroline=False,
        showline=False,
        showticklabels=True,
        side='bottom',
        tickvals=[0, 200000, 400000, 600000, 800000, 1000000, 1200000],
        ticktext=['0', '200,000', '400,000', '600,000', '800,000', '1 million', '1.2 million'],
        range=[0, max(x_data) * 1.25] # Ensure space for text labels
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        autorange='reversed' # Corrects order without manual data reversal
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=260, r=80, t=120, b=80),
    annotations=[
        dict(
            text=texts['source'],
            xref="paper", yref="paper",
            x=0.0, y=-0.12,
            xanchor='left', yanchor='top',
            showarrow=False,
            font=dict(size=12, color='#666666')
        ),
        dict(
            text=texts['note'],
            xref="paper", yref="paper",
            x=1.0, y=-0.12,
            xanchor='right', yanchor='top',
            showarrow=False,
            font=dict(size=12, color='#666666')
        )
    ]
)
# Using autorange='reversed' on yaxis is a more direct way to handle order
fig.update_yaxes(categoryorder='array', categoryarray=[item['category'] for item in chart_data])

# Determine output filename from the input JSON path
base_filename = json_path.split('/')[-1].rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")