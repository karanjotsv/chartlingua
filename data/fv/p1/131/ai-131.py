import sys
import json
import plotly.graph_objects as go

def main():
    """
    Main function to generate a chart from a JSON file.
    """
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <path_to_json_file>")
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

    chart_data = chart_info.get('chart_data', [])
    texts = chart_info.get('texts', {})
    colors = chart_info.get('colors', [])

    fig = go.Figure()

    for i, series in enumerate(chart_data):
        fig.add_trace(go.Scatter(
            x=series.get('x'),
            y=series.get('y'),
            mode='lines',
            name=series.get('name', ''),
            line=dict(color=colors[i % len(colors)])
        ))

    fig.update_layout(
        font=dict(family="Arial"),
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False,
        width=320,
        height=240,
        margin=dict(l=45, r=10, t=10, b=35),
        xaxis=dict(
            title_text=texts.get('x_axis_title'),
            tickvals=[-6, -4, -2, 0, 2, 4, 6],
            showline=True,
            linewidth=1,
            linecolor='black',
            mirror=True,
            ticks='outside',
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray',
            zeroline=False
        ),
        yaxis=dict(
            title_text=texts.get('y_axis_title'),
            range=[-0.01, 0.26],
            tickvals=[0, 0.05, 0.1, 0.15, 0.2, 0.25],
            showline=True,
            linewidth=1,
            linecolor='black',
            mirror=True,
            ticks='outside',
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray',
            zeroline=False
        )
    )
    
    if '.' in json_path:
        base_name = json_path.rsplit('.', 1)[0]
    else:
        base_name = json_path
    output_filename = f"{base_name}.png"
    
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    # Removed the main function wrapper to comply with the "no function definitions" rule.
    # The logic is now at the top level of the script.

    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <path_to_json_file>")
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

    chart_data = chart_info.get('chart_data', [])
    texts = chart_info.get('texts', {})
    colors = chart_info.get('colors', [])

    fig = go.Figure()

    for i, series in enumerate(chart_data):
        fig.add_trace(go.Scatter(
            x=series.get('x'),
            y=series.get('y'),
            mode='lines',
            name=series.get('name', ''),
            line=dict(color=colors[i % len(colors)])
        ))

    fig.update_layout(
        font=dict(family="Arial"),
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False,
        width=320,
        height=240,
        margin=dict(l=45, r=10, t=10, b=35),
        xaxis=dict(
            title_text=texts.get('x_axis_title'),
            tickvals=[-6, -4, -2, 0, 2, 4, 6],
            showline=True,
            linewidth=1,
            linecolor='black',
            mirror=True,
            ticks='outside',
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray',
            zeroline=False
        ),
        yaxis=dict(
            title_text=texts.get('y_axis_title'),
            range=[-0.01, 0.26],
            tickvals=[0, 0.05, 0.1, 0.15, 0.2, 0.25],
            showline=True,
            linewidth=1,
            linecolor='black',
            mirror=True,
            ticks='outside',
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray',
            zeroline=False
        )
    )
    
    if '.' in json_path:
        base_name = json_path.rsplit('.', 1)[0]
    else:
        base_name = json_path
    output_filename = f"{base_name}.png"
    
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")