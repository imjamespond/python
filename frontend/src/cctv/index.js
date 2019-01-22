import React, { Component } from 'react';
// import $ from 'jquery';
import Chart from 'chart.js';

import { GetJSON } from '../utils/ajax';
import { GetRandomColor } from '../utils/commons'

class CCTV extends Component {

  componentDidMount() {
    GetJSON('/cctv/frame-count', null, data => {
      // console.log(data) 
      var dateMap = {}, dateList = [], countMap = {};
      data.map(frame => {
        if (!dateMap[frame.frame_date]) {
          dateList.push(frame.frame_date);
          dateMap[frame.frame_date] = {};
        }

        dateMap[frame.frame_date][frame.object_type] = frame.count;
      });
      dateList.map(date => {
        const objs = dateMap[date];

        for (var k in objs) {
          var countList = countMap[k] || [];
          countList.push(objs[k] ? objs[k] : 0);
          countMap[k] = countList;
        }

      });
      var chartData = getData(dateList, countMap);
      new Chart(this.canvas.getContext('2d'), { data: chartData, type: 'line', options })
    });


  }

  render() {
    return <div className="container-fluid">
      <div className="row">
        <div className="col-xs-12">
          <div className="box box-info">
            <div className="box-header with-border">
              <h3 className="box-title">Line Chart</h3>

              <div className="box-tools pull-right">
                <button type="button" className="btn btn-box-tool" data-widget="collapse"><i className="fa fa-minus"></i>
                </button>
                <button type="button" className="btn btn-box-tool" data-widget="remove"><i className="fa fa-times"></i></button>
              </div>
            </div>
            <div className="box-body">
              <div className="chart">
                <canvas id="lineChart"
                  ref={el => this.canvas = el}
                  style={{ height: 250 }}></canvas>
              </div>
            </div>
          </div>

        </div>
      </div>

    </div>
  }
}

function getData(labels, objs, getData) {
  var datasets = [];
  for (var k in objs) {
    const data = getData ? getData(objs[k]) : objs[k];
    const color = GetRandomColor();
    var dataset = {
      label: k,
      backgroundColor: color + '88',
      borderColor: color,
      data
    }
    datasets.push(dataset);
  }
  return {
    labels,
    datasets
  }
}

// var chartData = {
//   labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
//   datasets: [
//     {
//       label: 'Electronics',
//       backgroundColor: 'rgba(210, 214, 222, .5)',
//       borderColor: 'rgba(210, 214, 222, 1)',
//       // pointColor: 'rgba(210, 214, 222, 1)',
//       // pointStrokeColor: '#c1c7d1',
//       // pointHighlightFill: '#fff',
//       // pointHighlightStroke: 'rgba(220,220,220,1)',
//       data: [65, 59, 80, 81, 56, 55, 40]
//     },
//     {
//       label: 'Digital Goods',
//       backgroundColor: 'rgba(60,141,188, 0.5)',
//       borderColor: 'rgba(60,141,188,0.8)',
//       // pointColor: '#3b8bba',
//       // pointStrokeColor: 'rgba(60,141,188,1)',
//       // pointHighlightFill: '#fff',
//       // pointHighlightStroke: 'rgba(60,141,188,1)',
//       data: [28, 48, 40, 19, 86, 27, 90]
//     }
//   ]
// }


var options = {
  responsive: true,
  title: {
    display: true,
    text: 'Chart.js Line Chart'
  },
  tooltips: {
    mode: 'index',
    intersect: false,
  },
  hover: {
    mode: 'nearest',
    intersect: true
  },
  scales: {
    xAxes: [{
      display: true,
      scaleLabel: {
        display: true,
        labelString: 'Frame date'
      }
    }],
    yAxes: [{
      display: true,
      scaleLabel: {
        display: true,
        labelString: 'Object count'
      },
      ticks: {
        beginAtZero: true
      }
    }]
  },

  datasetFill: false,
}

export default CCTV;