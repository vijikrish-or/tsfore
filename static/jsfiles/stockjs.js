document.getElementById("debug").innerHTML="js";
showdata(closelist);


function showdata(closelist){
    var viz_tag=document.getElementById("vdata")
    var viz_data=viz_tag.getAttribute("viz_data")
    /*c3.generate({
        bindto:"#schart",
        size:{height:480},
        data: {
            //x: 'x',
    //        xFormat: '%Y%m%d', // 'xFormat' can be used as custom format of 'x'
            columns: viz_data["columns"],
            type:"spline"
            //[
              // ['x', '2013-01-01', '2013-01-02', '2013-01-03', '2013-01-04', '2013-01-05', '2013-01-06'],
    //            ['x', '20130101', '20130102', '20130103', '20130104', '20130105', '20130106'],
               // ['data1', 30, 200, 100, 400, 150, 250],
                //['data2', 130, 340, 200, 500, 250, 350]
                
            //]
        },
        axis: {
            x: {
                type: "category",
                categories: viz_data["categories"]
               // tick: {
                 //   format: '%Y-%m-%d'
               // }
            }
        },
        grid:{
            x:{show:true},
            y:{show:true}
        }
    });

    c3.generate({
        bindto:"#sschart",
        data: {
            columns: [
                //['X', stockdt.iloc[0].Date, stockdt.iloc[1].Date,stockdt.iloc[2].Date, stockdt.iloc[3].Date ],
                //['x','2020-09-25','2020-09-28','2020-09-29','2020-09-30'],
                ['data1', 30, 200, 100, 400, 150, 250],
                ['data2', 50, 20, 10, 40]
                //['Close', stockdt.iloc[0].Close, stockdt.iloc[1].Close, stockdt.iloc[2].Close, stockdt.iloc[3].Close ]
            ]
        }
    });*/

    /*var ctx = document.getElementById('myChart').getContext('2d');
    var chart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'line',

    // The data for our dataset
    data: {
        labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
        datasets: [{
            label: 'My First dataset',
            backgroundColor: 'rgb(255, 99, 132)',
            borderColor: 'rgb(255, 99, 132)',
            data: [0, 10, 5, 2, 20, 30, 45]
        }]
    },

    // Configuration options go here
    options: {}
    });*/

    
    var ctx = document.getElementById('myChart').getContext('2d');
            var chart = new Chart(ctx, {
            // The type of chart we want to create
            type: 'line',

            // The data for our dataset
            data: {
                labels: ['2020-09-25','2020-09-28','2020-09-29','2020-09-30'],
                datasets: [{
                label: 'stock data',
                backgroundColor: 'rgb(255, 99, 132)',
                borderColor: 'rgb(255, 99, 132)',
                data: closelist
                 }]
            },

            // Configuration options go here
            options: {}
            });


}
