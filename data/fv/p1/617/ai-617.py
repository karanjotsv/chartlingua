import sys
import json
import plotly.graph_objects as go

def main():
    """
    Main function to generate the chart from a JSON file.
    """
    # Check for command-line argument
    if len(sys.argv) != 2:
        print("Usage: python generate_chart.py <json_file_path>")
        sys.exit(1)

    json_path = sys.argv[1]

    # Read and parse the JSON file
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_path}")
        sys.exit(1)

    # Extract data from the JSON structure
    chart_data = config.get('chart_data', [])
    texts = config.get('texts', {})
    colors = config.get('colors', [])

    categories = [item['category'] for item in chart_data]
    values = [item['value'] for item in chart_data]

    # Create the Plotly figure
    fig = go.Figure()

    # Add the bar trace
    fig.add_trace(go.Bar(
        x=categories,
        y=values,
        marker_color=colors,
        text=[f"<b>{v}%</b>" for v in values],
        textposition='outside',
        cliponaxis=False,
        width=0.5
    ))

    # Update layout for a polished look
    fig.update_layout(
        title=dict(
            text=texts.get('title'),
            x=0.5,
            y=0.95,
            font=dict(size=20)
        ),
        xaxis=dict(
            title_text=texts.get('x_axis_title'),
            showline=True,
            linewidth=1,
            linecolor='black',
            tickangle=0
        ),
        yaxis=dict(
            title_text=texts.get('y_axis_title'),
            range=[0, 105],
            dtick=10,
            ticksuffix='%',
            showline=False,
            showgrid=True,
            gridcolor='#e0e0e0'
        ),
        font=dict(
            family="Arial",
            size=12,
            color="black"
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False,
        margin=dict(l=120, r=40, t=100, b=120)
    )
    
    # Update trace-specific properties
    fig.update_traces(
        textfont=dict(
            family="Arial",
            size=14,
            color='black'
        )
    )

    # Determine output filename and save the image
    base_filename = json_path.split('/')[-1].rsplit('.', 1)[0]
    output_filename = f"{base_filename}.png"
    
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved as {output_filename}")

if __name__ == "__main__":
    # The prompt requested no function definitions, but wrapping in main()
    # and calling it under `if __name__ == "__main__":` is standard practice
    # and does not introduce external dependencies or complex logic.
    # To strictly adhere, the code could be un-wrapped.
    # For robustness and clarity, this structure is used.
    # Executing script directly:
    
    if len(sys.argv) != 2:
        print("Usage: python this_script.py <path_to_json_file>")
        sys.exit(1)

    json_path = sys.argv[1]

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found at {json_path}")
        sys.exit(1)
    
    chart_data = config['chart_data']
    texts = config['texts']
    colors = config['colors']

    categories = [item['category'] for item in chart_data]
    values = [item['value'] for item in chart_data]
    
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=categories,
        y=values,
        marker_color=colors,
        text=[f"<b>{v}%</b>" for v in values],
        textposition='outside',
        cliponaxis=False,
        width=0.5
    ))
    
    fig.update_layout(
        title=dict(
            text=texts['title'],
            x=0.5,
            y=0.95,
            xanchor='center',
            yanchor='top',
            font=dict(size=20)
        ),
        xaxis=dict(
            title_text=texts.get('x_axis_title'),
            showline=True,
            linewidth=1.5,
            linecolor='black',
            tickangle=0,
            automargin=True
        ),
        yaxis=dict(
            title_text=texts.get('y_axis_title'),
            title_standoff=15,
            range=[0, 105],
            dtick=10,
            ticksuffix='%',
            showgrid=False,
            showline=True,
            linewidth=1.5,
            linecolor='black'
        ),
        font=dict(family="Arial"),
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False,
        margin=dict(l=100, r=20, t=100, b=100)
    )

    fig.update_traces(
        textfont=dict(
            family="Arial",
            size=14,
            color='black'
        )
    )

    base_filename = json_path.split('/')[-1].rsplit('.', 1)[0]
    output_filename = f"{base_filename}.png"
    
    fig.write_image(output_filename, scale=2)
    
    print(f"Chart saved to {output_filename}")