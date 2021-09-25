# This is a convenience function that can generate simple bar graph
# 'title' is the Title of the graph (Just for visuals)
# 'dataTitles' is a list of the titles of the individual data rows
# 'data' should be a List of Tuples
#   Each tuple should contain as element 0 the main axis (Timestamp usually)
#        All other elements should contain the values to graph
#  Result is a massive string returned that can be dumped to a file
def MakeChart(titles, dataTitles, data):

    color = ("blue", "red")

    chart = ""  
    chart += """<html>
    <head>
        <script src="https://cdn.jsdelivr.net/npm/chart.js@3.5.0"></script>
        <script src="https://cdn.jsdelivr.net/npm/hammerjs@2.0.8"></script>
        <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-zoom@1.1.1"></script>
        <title>%s</title>
    </head>
    <body>
        <canvas id="myChart"></canvas>
    <script>
    chartData = {
        datasets: [
    """ % titles
    dataSets = list()
    # Skip element 0 because that's the x-Axis
    for element in range(1, len(data[0])):
        d = """{ type: 'bar',
                  label: '%s', 
                  showLine: true,
                  cubicInterpolationMode: 'default',
                  tension: 0.2,
                  radius: 0,
                  data: [""" % dataTitles[element-1]

        dataElements = map(lambda x : "{x: '%s', y: %s}" % (x[0], x[element]), data)
        d += ','.join(dataElements)
        d += """],
                  borderColor: '%s',
                  backgroundColor: '%s'
                }""" % (color[element-1], color[element-1])
        dataSets.append(d)

    chart += ','.join(dataSets)

    chart += """ ] };
    const config = {
        type: "bar",
        data: chartData,
        options: {
            parsing: false,
            interaction: {
                    mode: 'x',
                    axis: 'x',
                    intersect: false
            },
        plugins: {
            zoom: {
                pan: {
                    enabled: true,
                    mode: 'xy'
                },
                zoom: {
                    wheel: {
                        enabled: true
                    }
                }
            }
        } 
    } };
    var myChart = new Chart(
        document.getElementById('myChart'),
        config
    );
    </script>
    </body>
    </html>"""

    return chart






