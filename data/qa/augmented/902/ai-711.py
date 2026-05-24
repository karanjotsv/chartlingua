import sys
import json
import plotly.graph_objects as go
import os

def main():
    # Check if a command-line argument is provided
    if len(sys.argv) != 2:
        print("Usage: python create_chart.py <path_to_json_file>")
        sys.exit(1)

    json_path = sys.argv[1]

    # Check if the file exists
    if not os.path.exists(json_path):
        print(f"Error: File not found at {json_path}")
        sys.exit(1)

    # Load data from the specified JSON file
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            chart_config = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {json_path}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)

    # Extract data, texts, and colors from the JSON structure
    chart_data = chart_config.get('chart_data', [])
    texts = chart_config.get('texts', {})
    colors = chart_config.get('colors', [])

    # Prepare data for Plotly
    categories = [item['category'] for item in chart_data]
    values = [item['value'] for item in chart_data]

    # Create the figure
    fig = go.Figure()

    # Add the bar trace
    fig.add_trace(go.Bar(
        x=categories,
        y=values,
        marker_color=colors[0] if colors else '#2672C7',
        text=[f'{v}%' for v in values],
        textposition='outside',
        textfont=dict(
            family="Arial",
            size=12,
            color='black'
        ),
        cliponaxis=False # Prevent text from being clipped at the top
    ))

    # Update layout
    fig.update_layout(
        font=dict(
            family="Arial",
            size=12,
            color="black"
        ),
        title_text=texts.get('title'),
        yaxis_title=texts.get('y_axis_title'),
        xaxis_title=texts.get('x_axis_title'),
        plot_bgcolor='white',
        showlegend=False,
        margin=dict(l=60, r=40, t=40, b=100),
        xaxis=dict(
            showline=True,
            linewidth=1,
            linecolor='black',
            tickfont=dict(size=12)
        ),
        yaxis=dict(
            range=[0, max(values) * 1.3],
            showgrid=True,
            gridcolor='#e9e9e9',
            ticksuffix='%',
            zeroline=False,
            tickfont=dict(size=12)
        ),
        annotations=[
            dict(
                text=texts.get('source_left'),
                align='left',
                showarrow=False,
                xref='paper',
                yref='paper',
                x=0,
                y=-0.15,
                xanchor='left',
                yanchor='top'
            ),
            dict(
                text=texts.get('source_right'),
                align='right',
                showarrow=False,
                xref='paper',
                yref='paper',
                x=1,
                y=-0.15,
                xanchor='right',
                yanchor='top'
            )
        ]
    )

    # Generate output filename from the input JSON path
    base_filename = os.path.splitext(os.path.basename(json_path))[0]
    output_filename = f"{base_filename}.png"

    # Save the figure as a PNG image
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved as {output_filename}")

if __name__ == "__main__":
    main()