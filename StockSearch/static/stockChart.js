var dataPoints1 = [],
    dataPoints2 = [];
var stockChart;

window.onload = function () {

    stockChart = new CanvasJS.Chart("chartContainer", {
        animationEnabled: true,

        exportEnabled: true,
        exportFileName: "Compare result", //Change it to "Stock Chart"
        // theme: "light2",

        title: {
            text: "比對結果",
            fontSize: 28,
            fontWeight: "bold",
        },
        axisX: {
            interval: 1
        },
        axisY2: {
            interlacedColor: "rgba(1,77,101,.1)",
            gridColor: "rgba(1,77,101,.1)",
            title: "相似度 %"
        },
        data: [{
            type: "bar",
            name: "website",
            // showInLegend: true, 
            axisYType: "secondary",
            
            color: "#52E99E",
            dataPoints: [
            ]
        }]
    });
    stockChart.render();
    $("#loader").css("display", "block");
}

// window.onload = function () {

//     stockChart = new CanvasJS.StockChart("chartContainer", {
//         // animationEnabled: true,
//         exportEnabled: true,
//         exportFileName: "StockChart", //Change it to "Stock Chart"
//         theme: "light2",
//         title: {
//             text: "股票走勢圖",
//             fontSize: 28,
//             fontWeight: "bold",
//         },

//         // rangeChanged: rangeChanged,
//         rangeSelector: {
//             enabled: false, //change it to true
//         },
//         charts: [{
//             axisX: {
//                 margin: 20,
//                 // valueFormatString: "YYYY-MM-DD",
//                 // crosshair: {
//                 //     enabled: true,
//                 //     snapToDataPoint: true
//                 // }
//             },
//             axisX2: {
//                 margin: 25,
//                 valueFormatString: "YYYY-MM-DD",
//                 crosshair: {
//                     enabled: true,
//                     snapToDataPoint: true
//                 }
//             },
//             axisY: {
//                 title: "Price (NT$)",
//                 prefix: "$"
//             },
//             toolTip: {
//                 shared: true
//             },
//             data: [{
//                 name: "Price (NT$)",
//                 type: "candlestick",
//                 xValueFormatString: "YYYY MMM DD",
//                 yValueFormatString: "$#,###.##",
//                 // axisYType: "secondary",
//                 axisXType: "secondary",
//                 risingColor: "green",
//                 fallingColor: "red",
//                 dataPoints: dataPoints1
//             }]
//         }],
//         navigator: {
//             // dynamicUpdate: false,
//             // animationEnabled: true,
//             axisX: {
//                 valueFormatString: "YYYY MMM DD"
//               },
//             data: [{
//                 // valueFormatString:  "YYYY MMM DD",
//                 dataPoints: dataPoints2
//             }],
//             // slider: {
//             //     minimum: new Date(now_year, now_month-3, now_date),
//             //     maximum: new Date(now_year, now_month+1, now_date)
//             // }
//         }
//     });
//     stockChart.render();
//     $("#loader").css("display", "block");

// }