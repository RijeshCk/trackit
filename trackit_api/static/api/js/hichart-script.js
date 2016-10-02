// function Test(id){
// $(function () {                 var chart;
// 								var processed_json = new Array();   
// 														var k=new Array(),d;
// 														var j =new Array();
// 														id=$(id).attr("data")

// 							 aana();		
//                              chart.showLoading();	
// 								$.getJSON('http://127.0.0.1:8000/history/id='+id+'?format=json', function(data) {
// 										// Populate series
// 										$.each(data,function(key,val)
// 												{   

// 													var month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
// 													d = new Date(val.date).getDate()+' '+month[new Date(val.date).getMonth()]


// 														f=d
// 														if(val.price=='')
// 															{
// 																k.push(null)
// 															}
// 															else{ 
// 														k.push(parseInt(val.price));
// 														}
// 														j.push(f);
// 														processed_json.push(k);
// 														k=[]
// 												});
	 
// 						}).success(function() { 
// 						// draw chart
// 										$('#container').highcharts({
// 										chart: {
// 												type: "line"
// 										},
// 										chart: {
// 								zoomType: 'x'
// 						},
								
// 										title: {
// 												text: "Price history"
// 										},
// 										xAxis: {
// 											tickInterval: 5,
// 												// gridLineWidth: .1,
// 												// crosshair:true,
// 												categories:j,
// 												allowDecimals: true,
// 												title: {
// 															text: "date"
// 														},
// 												plotLines: [{
// 														value: 0,
// 														width: 1,
// 													}]
						
				
// 										},
// 										yAxis: {
// 												allowDecimals: true,
// 												title: {
// 														text: "Price"
// 												},
// 												tickInterval: 10,
// 										plotLines: [{
// 														value: 0,
// 														width: 1,
// 													}]
// 										},credits: {
// 												enabled: false
// 												 },

										 

// 										 tooltip: {crosshairs: [{
//             width: 1.5,
//             dashStyle: 'solid',
//             color: 'gray'
//         }, false]
// 				},
// 										series: [{
// 												name: 'Price',
// 												data: processed_json,
// 										}]
// 								}); })




// .error(function() {  
// 	$('#container').highcharts().destroy();
// 	$('#container').html('no data');
// 	});
						
// 				});
// }
// /**
//  * Grid-light theme for Highcharts JS
//  * @author Torstein Honsi
//  */

// // Load the fonts
// Highcharts.createElement('link', {
//    href: '//fonts.googleapis.com/css?family=Dosis:400,600',
//    rel: 'stylesheet',
//    type: 'text/css'
// }, null, document.getElementsByTagName('head')[0]);

// Highcharts.theme = {
//    colors: ["#000000"],
//    // colors: ['7cb5ec','#0066FF', '#00CCFF'],
//    chart: {
//       backgroundColor: null,
//       style: {
//          fontFamily: "Dosis, sans-serif"
//       }
//    },
//    title: {
//       style: {
//          fontSize: '16px',
//          fontWeight: 'bold',
//          textTransform: 'uppercase'
//       }
//    },
//    tooltip: {
//       borderWidth: 0,
//       backgroundColor: 'rgba(219,219,216,0.8)',
//       shadow: false
//    },
//    legend: {
//       itemStyle: {
//          fontWeight: 'bold',
//          fontSize: '13px'
//       }
//    },
//    xAxis: {
//       gridLineWidth: 1,
//       labels: {
//          style: {
//             fontSize: '12px'
//          }
//       }
//    },
//    yAxis: {
//       minorTickInterval: 'auto',
//       title: {
//          style: {
//             textTransform: 'uppercase'
//          }
//       },
//       labels: {
//          style: {
//             fontSize: '12px'
//          }
//       }
//    },
//    plotOptions: {
//       candlestick: {
//          lineColor: '#404048'
//       }
//    },


//    // General
//    background2: '#c0c0c0'

// };

// // Apply the theme
// Highcharts.setOptions(Highcharts.theme);
// function aana (){$(function aana () {
//     // the button handler
//     var isLoading = false,
//         $button = $('#button'),
//         chart;
//         alert('ssss');

    
//         if (!isLoading) {
//             chart.showLoading();
//             $button.html('Hide loading');
//         } else {
//             chart.hideLoading();
//             $button.html('Show loading');
//         }
//         isLoading = !isLoading;
//     });}
function Test(id){
$(function () {

    // Get the CSV and create the chart
    $.getJSON('https://www.highcharts.com/samples/data/jsonp.php?filename=analytics.csv&callback=?', function (csv) {
        console.log(csv);
        $('#container').highcharts({

            title: {
                text: 'Daily visits at www.highcharts.com'
            },

            subtitle: {
                text: 'Source: Google Analytics'
            },

            xAxis: {
                tickInterval: 7 * 24 * 3600 * 1000, // one week
                tickWidth: 0,
                gridLineWidth: 1,
                labels: {
                    align: 'left',
                    x: 3,
                    y: -3
                }
            },

            yAxis: [{ // left y axis
                title: {
                    text: null
                },
                labels: {
                    align: 'left',
                    x: 3,
                    y: 16,
                    format: '{value:.,0f}'
                },
                showFirstLabel: false
            }, { // right y axis
                linkedTo: 0,
                gridLineWidth: 0,
                opposite: true,
                title: {
                    text: null
                },
                labels: {
                    align: 'right',
                    x: -3,
                    y: 16,
                    format: '{value:.,0f}'
                },
                showFirstLabel: false
            }],

            legend: {
                align: 'left',
                verticalAlign: 'top',
                y: 20,
                floating: true,
                borderWidth: 0
            },

            tooltip: {
                shared: true,
                crosshairs: true
            },

            // plotOptions: {
            //     series: {
            //         cursor: 'pointer',
            //         point: {
            //             events: {
            //                 click: function (e) {
            //                     hs.htmlExpand(null, {
            //                         pageOrigin: {
            //                             x: e.pageX || e.clientX,
            //                             y: e.pageY || e.clientY
            //                         },
            //                         headingText: this.series.name,
            //                         maincontentText: Highcharts.dateFormat('%A, %b %e, %Y', this.x) + ':<br/> ' +
            //                             this.y + ' visits',
            //                         width: 200
            //                     });
            //                 }
            //             }
            //         },
            //         marker: {
            //             lineWidth: 1
            //         }
            //     }
            // },
            series:[{name:'aaaa',data:[1,2,3,4,5,6,6,3]}]

            // series: [{
            //     name: 'All visits',
            //     data:csv,
            //     lineWidth: 4,
            //     marker: {
            //         radius: 4
            //     }
            // }, {
            //     name: 'New visitors'
            // }]
        });
    });

});}