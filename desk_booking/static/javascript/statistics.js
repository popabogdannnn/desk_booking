const SVG_WIDTH = 500;
const SVG_HEIGHT = 300;
const BAR_PADDING = 5;
var statistics

function draw_chart(dataset, id) {
    let svg = d3.select(id)
    let bar_width = SVG_WIDTH / 4;

    let x_vals = Object.keys(dataset);
    let y_vals = [];
    x_vals.forEach(element => {
        y_vals.push(dataset[element]);
    });

    max_y = Math.max(...y_vals);
    console.log(max_y);
    for(let i = 0; i < y_vals.length; i++) {
        y_vals[i] *= SVG_HEIGHT / max_y;
        
    }

    let bar_chart = svg.selectAll('rect')
    .data(y_vals)
    .enter()
    .append('rect')
    .attr('y', function(d) {
        return SVG_HEIGHT - d;
    })
    .attr('height', function(d) {
        return d;
    })
    .attr('width', bar_width - BAR_PADDING)
    .attr('transform', function(d, i) {
        var translate = [bar_width * i, 0];
        return 'translate(' + translate + ')';
    });
   
    console.log(x_vals);
    var text = svg.selectAll("text")
    .data(x_vals)
    .enter()
    .append("text")
    .text(function(d) {
        return d;
    })
    .attr("y", function(d, i) {
        return SVG_HEIGHT - 4;
    })
    .attr("x", function(d, i) {
        return bar_width * i;
    })
    .attr("fill", "#A64C38");

} 


window.onload = function init(e) {
    var svg = d3.selectAll('svg')
    .attr('width', SVG_WIDTH)
    .attr('height', SVG_HEIGHT);
    
    let xhr = new XMLHttpRequest();
    let url = window.location.href;
    xhr.open("FETCH", url, true);

    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.setRequestHeader("X-CSRFToken", csrf_token);
    
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            statistics = JSON.parse(JSON.parse(xhr.responseText));
            keys = Object.keys(statistics);
            console.log(statistics);
            draw_chart(statistics.location_distribution, "#first_chart");
            draw_chart(statistics.floor_distribution, "#second_chart");
            let x = document.createElement("p")
            x.innerText = "Percentage of employees that booked in the last 7 days: " + statistics.percentage_last_week * 100 + "%";
            document.getElementById("centered").appendChild(x);

        }
    };
    
    var data = JSON.stringify({});
    
    xhr.send(data);
    
    
    
}