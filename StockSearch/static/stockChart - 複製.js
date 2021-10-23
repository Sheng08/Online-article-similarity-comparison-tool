window.onload = function () {
  var dataPoints1 = [],
    dataPoints2 = [];
  var stockChart = new CanvasJS.StockChart("chartContainer", {
    // title: {
    //   text: "開盤走勢圖"
    // },
    rangeChanged: rangeChanged,
    charts: [{
      axisY2: {
        prefix: "$"
      },
      data: [{
        type: "candlestick",
        yValueFormatString: "$#,###.##",
        axisYType: "secondary",
        dataPoints: dataPoints1
      }]
    }],
    navigator: {
      dynamicUpdate: false,
      data: [{
        dataPoints: dataPoints2
      }],
      slider: {
        minimum: new Date(2015, 05, 01),
        maximum: new Date(2019, 05, 01)
      }
    }
  });

  function addData(data) {
    stockChart.options.charts[0].data[0].dataPoints = [];
    for (var i = 0; i < data.length; i++) {
      stockChart.options.charts[0].data[0].dataPoints.push({
        x: new Date(data[i].dateTime * 1000),
        y: [Number(data[i].open), Number(data[i].high), Number(data[i].low), Number(data[i].close)]
      });
    }
    stockChart.render();
  }

  function rangeChanged(e) {
    var minimum = parseInt(e.minimum / 1000);
    var maximum = parseInt(e.maximum / 1000);
    var url = "https://canvasjs.com/services/data/datapoints-bitcoinusd.php?minimum=" + minimum + "&maximum=" +
      maximum;
    $("#loader").css("display", "block");
    $.getJSON(url, function (data) {
      addData(data);
      $("#loader").css("display", "none");
    });
  }
  
  $("#loader").css("display", "block");
  $.getJSON("https://canvasjs.com/services/data/datapoints-bitcoinusd.php", function (data) {
    for (var i = 0; i < data.length; i++) {
      dataPoints1.push({
        x: new Date(data[i].dateTime * 1000),
        y: [Number(data[i].open), Number(data[i].high), Number(data[i].low), Number(data[i].close)]
      });
      dataPoints2.push({
        x: new Date(data[i].dateTime * 1000),
        y: Number(data[i].close)
      });
    }
    $("#loader").css("display", "none");
    stockChart.render();
  });
}