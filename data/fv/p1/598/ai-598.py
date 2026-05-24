import sys
import json
import plotly.graph_objects as go
import os

def main():
    # Check for command-line argument
    if len(sys.argv) != 2:
        print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
        sys.exit(1)

    json_path = sys.argv[1]

    # Ensure the JSON file exists
    if not os.path.exists(json_path):
        print(f"Error: JSON file not found at '{json_path}'")
        sys.exit(1)

    # Read data from JSON file
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            chart_data = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{json_path}'")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)

    # Extract data and texts from the loaded JSON
    data = chart_data.get('chart_data', [])
    texts = chart_data.get('texts', {})
    colors = chart_data.get('colors', [])
    
    labels = [item['label'] for item in data]
    values = [item['value'] for item in data]

    # Create the pie chart trace
    pie_trace = go.Pie(
        labels=labels,
        values=values,
        marker=dict(
            colors=colors,
            line=dict(color='#000000', width=1)
        ),
        sort=False,
        direction='clockwise',
        rotation=90,
        textinfo='none',
        hoverinfo='label+percent'
    )

    # Create the figure
    fig = go.Figure(data=[pie_trace])

    # Update the layout
    fig.update_layout(
        font=dict(family="Arial", size=12),
        plot_bgcolor='#D3D3D3',
        paper_bgcolor='#FFFFFF',
        showlegend=True,
        legend=dict(
            x=1.02,
            y=1,
            xanchor='left',
            yanchor='top',
            bgcolor='rgba(255,255,255,0.5)'
        ),
        margin=dict(l=20, r=400, t=40, b=150),
        annotations=[
            dict(
                text=texts.get('source', ''),
                showarrow=False,
                xref="paper",
                yref="paper",
                x=0,
                y=-0.1,
                xanchor='left',
                yanchor='top',
                align='left',
                font=dict(size=10)
            )
        ]
    )

    # Derive output filename from the input JSON filename
    base_filename, _ = os.path.splitext(os.path.basename(json_path))
    output_filename = f"{base_filename}.png"

    # Save the figure as a PNG image
    try:
        fig.write_image(output_filename, scale=2)
        print(f"Chart saved as {output_filename}")
    except Exception as e:
        print(f"Error saving image: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()