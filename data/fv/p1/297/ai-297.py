import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load Data ---
# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} <path_to_json_file>")
    sys.exit(1)

json_file_path = pathlib.Path(sys.argv[1])

# Read the JSON data file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data and text elements from the JSON structure
data_series = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']
output_filename_base = json_file_path.stem

# --- 2. Create Figure ---
fig = go.Figure()

# --- 3. Add Traces ---
# Iterate through the data series to create a bar trace for each
for i, series in enumerate(data_series):
    fig.add_trace(go.Bar(
        name=series['name'],
        x=[series['name']],  # Treat each bar as a distinct category
        y=[series['value']],
        marker_color=colors[i],
        error_y=dict(
            type='data',
            array=[series['error']],
            visible=True,
            color='dimgrey',
            thickness=1.5
        ),
        text=[str(series['value'])],
        textposition='inside',
        textfont=dict(
            family="Arial",
            color=series['text_color'],
            size=14
        ),
        insidetextanchor='middle'
    ))

# --- 4. Update Layout ---
fig.update_layout(
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showticklabels=False,  # Hide tick labels as categories are in legend
        showline=False,
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        showgrid=True,
        gridcolor='lightgray',
        zeroline=True,
        zerolinecolor='black',
        zerolinewidth=1,
        range=[-250, 650],
        dtick=200
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5,
        traceorder="normal"
    ),
    plot_bgcolor='white',
    barmode='group',
    bargap=0.5, # Adjust gap between bars of different categories (though only one here)
    margin=dict(l=60, r=20, t=80, b=80),
    width=700,
    height=550
)

# --- 5. Output ---
output_image_path = f"{output_filename_base}.png"
fig.write_image(output_image_path, scale=2)
print(f"Chart saved to {output_image_path}")