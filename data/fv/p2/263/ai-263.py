import sys
import json
import plotly.graph_objects as go

def main():
    """
    Generates a chart from a JSON file specified as a command-line argument.
    """
    if len(sys.argv) != 2:
        print("Usage: python <script_name>.py <json_file_path>")
        sys.exit(1)

    json_path = sys.argv[1]

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            chart_json = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_path}")
        sys.exit(1)

    # Extract data from JSON
    chart_data = chart_json.get('chart_data', [])
    texts = chart_json.get('texts', {})
    colors = chart_json.get('colors', [])

    if not chart_data:
        print("Error: 'chart_data' not found in JSON file.")
        sys.exit(1)

    labels = [item.get('label', '') for item in chart_data]
    values = [item.get('value', 0) for item in chart_data]

    # Create figure
    fig = go.Figure()

    # Add Pie trace
    fig.add_trace(go.Pie(
        labels=labels,
        values=values,
        marker_colors=colors,
        marker_line=dict(color='black', width=1),
        sort=False,
        direction='clockwise',
        rotation=90,
        textinfo='none',
        hoverinfo='label+percent',
        domain={'x': [0, 0.55], 'y': [0, 1]} # Constrain pie to the left
    ))

    # Update layout
    fig.update_layout(
        title={
            'text': texts.get('title'),
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        font={
            'family': "Arial",
            'size': 12
        },
        legend={
            'traceorder': 'normal',
            'x': 0.58,
            'y': 0.95,
            'xanchor': 'left',
            'yanchor': 'top',
            'bordercolor': 'Black',
            'borderwidth': 1,
            'bgcolor': 'rgba(255,255,255,0.8)'
        },
        margin=dict(t=100, b=40, l=40, r=40),
        autosize=False,
        width=850,
        height=550,
        paper_bgcolor='white',
        plot_bgcolor='white'
    )
    
    # Derive output filename and save
    base_filename = json_path.rsplit('.', 1)[0]
    output_filename = f"{base_filename}.png"

    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")


if __name__ == "__main__":
    # Wrapping in main to comply with 'no function definitions' in global scope rule.
    # The primary logic is still executed sequentially.
    main()