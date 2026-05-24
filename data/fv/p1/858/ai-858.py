import sys
import json
import os
import plotly.graph_objects as go

def main():
    # Check for command-line argument
    if len(sys.argv) != 2:
        print("Usage: python generate_chart.py <json_file_path>")
        sys.exit(1)

    json_path = sys.argv[1]

    # Verify JSON file exists
    if not os.path.exists(json_path):
        print(f"Error: JSON file not found at '{json_path}'")
        sys.exit(1)

    # Read data from JSON file
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)

    # Initialize figure
    fig = go.Figure()

    # Add traces from JSON data
    data_series = chart_data['chart_data']['series']
    categories = chart_data['chart_data']['categories']
    colors = chart_data['colors']

    for i, series in enumerate(data_series):
        fig.add_trace(go.Bar(
            name=series['name'],
            x=categories,
            y=series['y'],
            marker_color=colors[i],
            text=[f"{val}%" for val in series['y']],
            textposition='outside',
            cliponaxis=False
        ))

    # Update layout
    texts = chart_data['texts']
    fig.update_layout(
        barmode='group',
        title=dict(
            text=texts['title'],
            x=0.5,
            font=dict(size=20)
        ),
        xaxis=dict(
            title_text=texts['x_axis_title'],
            showline=True,
            linewidth=1,
            linecolor='black',
            mirror=True,
        ),
        yaxis=dict(
            title_text=texts['y_axis_title'],
            range=[0, 105],
            dtick=10,
            ticksuffix='%',
            showline=True,
            linewidth=1,
            linecolor='black',
            mirror=True,
            gridcolor='lightgray'
        ),
        legend=dict(
            x=0.99,
            y=0.99,
            xanchor='right',
            yanchor='top',
            borderwidth=0
        ),
        font=dict(
            family="Arial",
            size=12,
            color="black"
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=100, r=40, t=100, b=120)
    )

    # Set text font for data labels specifically
    fig.update_traces(textfont_size=12)

    # Generate output image path
    base_filename = os.path.splitext(os.path.basename(json_path))[0]
    output_image_path = f"{base_filename}.png"

    # Save image and print confirmation
    fig.write_image(output_image_path, scale=2)
    print(f"Chart saved to {output_image_path}")

if __name__ == "__main__":
    main()