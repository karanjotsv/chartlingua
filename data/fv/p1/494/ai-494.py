import sys
import json
import os
import plotly.graph_objects as go

def main():
    """
    Main function to generate a pie chart from a JSON file.
    """
    if len(sys.argv) != 2:
        print("Usage: python <script_name>.py <json_file_path>")
        sys.exit(1)

    json_path = sys.argv[1]

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at '{json_path}'")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{json_path}'")
        sys.exit(1)

    chart_data = config.get('chart_data', [])
    colors = config.get('colors', [])
    background_color = config.get('background_color', '#FFFFFF')

    labels = [item['label'] for item in chart_data]
    values = [item['value'] for item in chart_data]

    # Create the pie chart trace
    pie_trace = go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors),
        textinfo='percent',
        textfont=dict(family='Arial', size=20, color='black'),
        hoverinfo='label+percent',
        sort=False,
        direction='clockwise',
        insidetextorientation='horizontal'
    )

    # Define the layout
    layout = go.Layout(
        showlegend=True,
        legend=dict(
            font=dict(family='Arial', size=12, color='white'),
            traceorder='normal',
            bgcolor='rgba(0,0,0,0)' # Transparent legend background
        ),
        plot_bgcolor=background_color,
        paper_bgcolor=background_color,
        font=dict(family='Arial'),
        margin=dict(l=40, r=40, t=40, b=40),
        autosize=True
    )

    # Create the figure
    fig = go.Figure(data=[pie_trace], layout=layout)

    # Determine output filename and save the image
    base_filename = os.path.splitext(os.path.basename(json_path))[0]
    output_filename = f"{base_filename}.png"

    try:
        fig.write_image(output_filename, scale=2)
        print(f"Chart saved to {output_filename}")
    except Exception as e:
        print(f"Error saving image: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()