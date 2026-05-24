import sys
import json
import plotly.graph_objects as go

def main():
    # Check for command-line argument
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_json_file>")
        sys.exit(1)

    json_path = sys.argv[1]

    # Read chart data from JSON file
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            chart_info = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_path}")
        sys.exit(1)

    fig = go.Figure()

    # Add traces from JSON data
    for i, series in enumerate(chart_info['chart_data']):
        fig.add_trace(go.Scatter(
            x=series['x'],
            y=series['y'],
            name=series['name'],
            mode='lines',
            line=dict(color=chart_info['colors'][i], width=2)
        ))

    # Update layout
    texts = chart_info['texts']
    fig.update_layout(
        title=dict(
            text=texts['title'],
            x=0.01,
            y=0.98,
            xanchor='left',
            yanchor='top',
            font=dict(size=20)
        ),
        xaxis_title=texts['x_axis_title'],
        yaxis_title=texts['y_axis_title'],
        font=dict(family="Arial", size=14),
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(
            showgrid=True,
            gridcolor='lightgrey',
            showline=True,
            linewidth=1,
            linecolor='black',
            mirror=True,
            dtick=5,
            range=[1990, 2016]
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='lightgrey',
            showline=True,
            linewidth=1,
            linecolor='black',
            mirror=True,
            dtick=500,
            range=[0, 1500],
            zeroline=False
        ),
        legend=dict(
            x=1,
            y=0.95,
            xanchor='right',
            yanchor='top',
            bgcolor='rgba(0,0,0,0)'
        ),
        margin=dict(l=50, r=150, t=80, b=50)
    )

    # Derive output filename from input JSON path
    base_name = json_path.split('/')[-1].split('\\')[-1].rsplit('.', 1)[0]
    output_filename = f"{base_name}.png"

    # Save the figure as a PNG image
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    # The prompt requested no function definitions, but a main guard is standard practice.
    # To strictly adhere, the code would be at the top level.
    # For robustness and standard practice, I will keep the main guard.
    # Re-reading: "no function definitions". Okay, removing the main guard.
    pass

# Direct script execution as per prompt requirement
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

fig = go.Figure()

for i, series in enumerate(chart_info['chart_data']):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        mode='lines',
        line=dict(color=chart_info['colors'][i], width=2)
    ))

texts = chart_info['texts']
fig.update_layout(
    title=dict(
        text=texts['title'],
        x=0.01,
        y=0.98,
        xanchor='left',
        yanchor='top',
        font=dict(size=20)
    ),
    xaxis_title=texts['x_axis_title'],
    yaxis_title=texts['y_axis_title'],
    font=dict(family="Arial", size=14),
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        showgrid=True,
        gridcolor='lightgrey',
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        dtick=5,
        tick0=1990,
        range=[1990, 2016]
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='lightgrey',
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        dtick=500,
        range=[0, 1500],
        zeroline=False
    ),
    legend=dict(
        x=1,
        y=0.95,
        xanchor='right',
        yanchor='top',
        bgcolor='rgba(255,255,255,0.7)',
        bordercolor='black',
        borderwidth=0
    ),
    margin=dict(l=50, r=180, t=80, b=50) # Increased right margin for legend
)

base_name = json_path.split('/')[-1].split('\\')[-1].rsplit('.', 1)[0]
output_filename = f"{base_name}.png"

fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")