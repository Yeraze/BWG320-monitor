# This is a convenience function that can generate simple bar graph
# 'title' is the Title of the graph (Just for visuals)
# 'dataTitles' is a list of the titles of the individual data rows
# 'data' should be a List of Tuples
#   Each tuple should contain as element 0 the main axis (Timestamp usually)
#        All other elements should contain the values to graph
#  Result is a massive string returned that can be dumped to a file
def MakeChart(name, titles, dataTitles, data):
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
        <canvas id="%s"></canvas>
    <script>
    %s_chartData = {
        datasets: [
    """  % (name, name)
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
    const %s_config = {
        type: "bar",
        data: %s_chartData,
        options: {
            parsing: false,
            interaction: {
                    mode: 'x',
                    axis: 'x',
                    intersect: false
            }
    } };
    var %s = new Chart(
        document.getElementById('%s'),
        %s_config
    );
    </script>""" % (name, name, name, name, name)
#    chart += """
#    </body>
#    </html>"""

    return chart

def MakeBWChart(name, titles, dataTitles, data):
    color = ("rgba(0,0,255,0.5)" , "purple","rgba(255,0,0,0.5)", "orange")
    chart = ""  
    chart += """
    <script src="https://cdn.jsdelivr.net/npm/chart.js@3.5.0"></script>
        <script src="https://cdn.jsdelivr.net/npm/hammerjs@2.0.8"></script>
        <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-zoom@1.1.1"></script>
        <canvas id="%s"></canvas>
    <script>
    %s_chartData = {
        labels: [""" % (name, name)

    dataElements = map(lambda x : "'%s'" % x[0], data)
    chart += ','.join(dataElements)

    chart += """
        ],
        datasets: [
    """ 
    dataSets = list()
    for N in range(0, int((len(data[0]) - 1) / 3)):
        element = (N *3) +1
        
        # Skip element 0 because that's the x-Axis
        d = """{ type: 'bar',
                  yAxisID: 'SLOPE',
                  label: '%s', 
                  data: [""" % dataTitles[2*N]

        dataElements = map(lambda x : "[%s, %s]" % (round(x[element],3), round(x[element+1],3)), data)
        d += ','.join(dataElements)
        d += """],
                  borderColor: '%s',
                  backgroundColor: '%s'
                }""" % (color[2*N], color[2*N])
        dataSets.append(d)
 
        d = """ 
                { type: 'line',
                  yAxisID: 'SLOPE',
                  label: '%s',
                  data:[""" %dataTitles[2*N +1]
        dataElements = map(lambda x : "%s" % (round(x[element +2],3)), data)
        d += ','.join(dataElements)
        d += """],
                  borderColor: '%s',
                  backgroundColor: '%s'
                }""" % (color[2*N+1], color[2*N+1])
        dataSets.append(d)

    chart += ','.join(dataSets)

    chart += """ ] };
    const %s_config = {
        type: "bar",
        data: %s_chartData,
        options: {
            scales: {
                'SLOPE': {
                    position: 'left',
                    beginAtZero: false
                }
            }
        }
    };
    var %s_myChart = new Chart(
        document.getElementById('%s'),
        %s_config
    );
    </script>""" % (name, name, name, name, name)
#    chart += """
#    </body>
#    </html>"""

    return chart


