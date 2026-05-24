import sys
import json
import plotly.graph_objects as go

# --- 1. Load data from JSON file ---
# The script requires the path to the JSON file as a command-line argument.
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{json_path}' is not a valid JSON file.")
    sys.exit(1)

# Extract data and configuration from the loaded JSON
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', {})
series_colors = colors.get('series', [])
text_colors = colors.get('text', [])

# --- 2. Create the chart figure ---
fig = go.Figure()

# Add a bar trace for each data series, iterating in order
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        y=series['y'],
        x=series['x'],
        name=series['name'],
        orientation='h',
        marker=dict(
            color=series_colors[i],
            line=dict(width=0) # Remove border around bar segments
        ),
        # Format text to be bold with a percentage sign
        text=[f'<b>{val}%</b>' for val in series['x']],
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(
            family='Arial',
            size=14,
            color=text_colors[i]
        ),
        hoverinfo='skip'
    ))

# --- 3. Configure the layout ---
fig.update_layout(
    barmode='stack',
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=50, r=20, t=40, b=100),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        range=[0, 100],
        ticksuffix='%',
        showgrid=False,
        zeroline=False,
        title_font=dict(size=14),
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='#EAEAEA',
        gridwidth=1,
        zeroline=False,
        tickfont=dict(size=14)
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5,
        traceorder='normal',
        font=dict(size=12)
    ),
    annotations=[
        dict(
            xref='paper', yref='paper',
            x=0.99, y=-0.3,
            text=texts.get('source'),
            showarrow=False,
            xanchor='right', yanchor='bottom',
            font=dict(size=12, color='#666666')
        )
    ],
    height=500,
    width=800
)

# --- 4. Save the chart as a PNG image ---
# Derive the output filename from the input JSON filename
output_filename_base = json_path.rsplit('.', 1)[0]
output_filename_png = f"{output_filename_base}.png"

fig.write_image(output_filename_png, scale=2)

print(f"Chart saved successfully to '{output_filename_png}'")