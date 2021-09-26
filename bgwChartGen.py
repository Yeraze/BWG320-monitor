# This is a convenience function that can generate simple bar graph
# 'title' is the Title of the graph (Just for visuals)
# 'dataTitles' is a list of the titles of the individual data rows
# 'data' should be a List of Tuples
#   Each tuple should contain as element 0 the main axis (Timestamp usually)
#        All other elements should contain the values to graph
#  Result is a massive string returned that can be dumped to a file
def MakeChart(titles, dataTitles, data):
    color = ("red", "blue", "purple")

    chart = ""  
#    chart += """<html>
#    <head>
#        <script src="https://cdn.jsdelivr.net/npm/chart.js@3.5.0"></script>
#        <script src="https://cdn.jsdelivr.net/npm/hammerjs@2.0.8"></script>
#        <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-zoom@1.1.1"></script>
#        <title>%s</title>
#    </head>
#    <body>"""
    chart += """
    <script src="https://cdn.jsdelivr.net/npm/chart.js@3.5.0"></script>
        <script src="https://cdn.jsdelivr.net/npm/hammerjs@2.0.8"></script>
        <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-zoom@1.1.1"></script>
        <canvas id="myChart"></canvas>
    <script>
    chartData = {
        datasets: [
    """ 
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
            }
    } };
    var myChart = new Chart(
        document.getElementById('myChart'),
        config
    );
    </script>"""
#    chart += """
#    </body>
#    </html>"""

    return chart

def MakeBWChart(titles, dataTitles, data):
    chart = ""  
    chart += """
    <script src="https://cdn.jsdelivr.net/npm/chart.js@3.5.0"></script>
        <script src="https://cdn.jsdelivr.net/npm/hammerjs@2.0.8"></script>
        <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-zoom@1.1.1"></script>
        <canvas id="myChart"></canvas>
    <script>
    chartData = {
        labels: ["""

    dataElements = map(lambda x : "'%s'" % x[0], data)
    chart += ','.join(dataElements)

    chart += """
        ],
        datasets: [
    """ 
    dataSets = list()
    # Skip element 0 because that's the x-Axis
    d = """{ type: 'bar',
              yAxisID: 'SLOPE',
              label: '%s', 
              data: [""" % dataTitles[0]

    dataElements = map(lambda x : "[%s, %s]" % (int(x[1]), int(x[2])), data)
    d += ','.join(dataElements)
    d += "]}"
    dataSets.append(d)

    d = """ 
            { type: 'line',
              yAxisID: 'SLOPE',
              label: '%s',
              data:[""" %dataTitles[1]
    dataElements = map(lambda x : "%s" % int(x[3]), data)
    d += ','.join(dataElements)
    d += "]}"
    dataSets.append(d)

    chart += ','.join(dataSets)

    chart += """ ] };
    const config = {
        type: "bar",
        data: chartData,
        options: {
        scales: {
            'SLOPE': {
                position: 'left',
                beginAtZero: false
            }
        }
    } };
    var myChart = new Chart(
        document.getElementById('myChart'),
        config
    );
    </script>"""
#    chart += """
#    </body>
#    </html>"""

    return chart


