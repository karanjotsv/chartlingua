import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load Data ---
# The script requires the path to the JSON file as a command-line argument.
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

# Extract data and texts from the loaded JSON
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# --- 2. Create Figure ---
fig = go.Figure()

# --- 3. Add Traces (Bars) ---
# Iterate through the data series from the JSON to create a bar for each
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        marker_color=colors[i],
        text=[f'{val}%' for val in series['y']],
        textposition='outside',
        cliponaxis=False,  # Prevents text on top of bars from being clipped
        textfont=dict(family="Arial", size=12)
    ))

# --- 4. Configure Layout ---
fig.update_layout(
    barmode='group',
    plot_bgcolor='white',
    font=dict(family="Arial", size=12),
    margin=dict(l=80, r=40, t=50, b=120),  # Adjust margins for titles and legend
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=True,
        linecolor='black',
        tickfont=dict(size=12),
        type='category' # Ensures discrete, evenly spaced categories
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 52],  # Set range to give space above highest bar
        dtick=10,
        ticksuffix='%',
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        zeroline=False
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.3,
        xanchor='center',
        x=0.5
    ),
    # Add source annotation at the bottom right
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.32,
            xanchor='right',
            yanchor='bottom',
            align='right',
            font=dict(size=10)
        )
    ]
)
# Ensure data labels have the correct font
fig.update_traces(textfont_family="Arial")

# --- 5. Output Image ---
# Derive the output filename from the input JSON filename
base_filename = pathlib.Path(json_path).stem
output_filename = f"{base_filename}.png"

# Save the figure to a PNG file with a high resolution
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to '{output_filename}'")