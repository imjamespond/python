import React, { Component } from 'react';
import $ from 'jquery';
import 'flot';

import { GetJSON } from '../utils/ajax';

class CCTV extends Component {

  componentDidMount() {
    GetJSON('/cctv/frame-list', null, data => {
      console.log(data)
    });

    var areaData = [[2, 88.0], [3, 93.3], [4, 102.0], [5, 108.5], [6, 115.7], [7, 115.6],
    [8, 124.6], [9, 130.3], [10, 134.3], [11, 141.4], [12, 146.5], [13, 151.7], [14, 159.9],
    [15, 165.4], [16, 167.8], [17, 168.7], [18, 169.5], [19, 168.0]]
    $.plot('#area-chart', [{ data: areaData, label: "person count" },], {
      grid: {
        borderWidth: 0,
        hoverable: true,
        clickable: true
      },
      series: {
        lines: {
          show: true
        },
        points: {
          show: true
        },
        shadowSize: 0, // Drawing is faster without shadows
        color: '#00c0ef'
      },
      lines: {
        fill: true, //Converts the line chart to area chart
      },
      yaxis: {
        show: true
      },
      xaxis: {
        show: true
      },
    });

    $('#area-chart').bind("plothover", (event, pos, item) => {
      // if ($("#enablePosition:checked").length > 0) {
      //   var str = "(" + pos.x.toFixed(2) + ", " + pos.y.toFixed(2) + ")";
      //   $("#hoverdata").text(str);
      // }

      // if ($("#enableTooltip:checked").length > 0) {
      if (item) {
        console.log(item.pageX, item.pageY)
        var x = item.datapoint[0].toFixed(2),
          y = item.datapoint[1].toFixed(2);

        $(this.tooltipEl).html(item.series.label + " of " + x + " = " + y);
        $(this.tooltipEl).css({ top: item.pageY + 5, left: item.pageX + 5 }).fadeIn(200);
      } else {
        $(this.tooltipEl).hide();
      }
      // }
    });

  }

  // tooltip() {

  // }

  render() {
    return <div className="container">
      <div className="row">
        <div className="col-xs-12">
          {/* <!-- Area chart --> */}
          <div className="box box-primary">
            <div className="box-header with-border">
              <i className="fa fa-bar-chart-o"></i>

              <h3 className="box-title">Full Width Area Chart</h3>

              <div className="box-tools pull-right">
                <button type="button" className="btn btn-box-tool" data-widget="collapse"><i className="fa fa-minus"></i>
                </button>
                <button type="button" className="btn btn-box-tool" data-widget="remove"><i className="fa fa-times"></i></button>
              </div>
            </div>
            <div className="box-body">
              <div id="area-chart"
                style={{ height: 338 }} className="full-width-chart"></div>
            </div>
            {/* <!-- /.box-body--> */}
          </div>

        </div>
      </div>

      <div id='tooltip'
        ref={el => this.tooltipEl = el}
        style={{ position: 'absolute', display: 'none' }}>tooltip</div>
    </div>
  }
}

export default CCTV;