import React, { Component } from 'react';
import { Link, Route, Switch } from 'react-router-dom';
// import $ from 'jquery';
import Chart from 'chart.js';

import { GetJSON } from '../utils/ajax';

import Config from './config';
import { options, getData } from './chart';


class Index extends Component {
  constructor(props) {
    super(props)
    this.canvasMap = {};
    this.state = { camList: null, totalMap: null }
  }

  componentDidMount() {
    const {} = this.state;
    this.setState({ camList: null }, () => {
      GetJSON('/cctv/webcam-list', null, camList => {
        this.setState({ camList }, () => {

          var totalMap = {};

          camList.map((o, i) => {
            GetJSON('/cctv/track-list', { id: o.id }, data => {

              var chartData = getData(data);

              // new Chart(this.canvasMap[o.id].getContext('2d')).Line(chartData, {
              //   responsive: true,
              //   showTooltips: true,
              //   multiTooltipTemplate: "<%= datasetLabel %> - <%= value %>"
              // });

              var ctx = this.canvasMap[o.id].getContext('2d');
              var myChart = new Chart(ctx, chartData);
              var totalLeft = 0, totalRight = 0, totalTop = 0, totalBottom = 0;
              data.map((trace,i) => { 
                totalLeft += trace.left;
                totalRight += trace.right;
                totalTop += trace.top;
                totalBottom += trace.bottom;
              });
              
              totalMap = Object.assign({}, totalMap);
              totalMap[o.id] = {totalLeft, totalRight, totalTop, totalBottom};
              this.setState({totalMap});
            })
          })

        });
      });
    });


  }


  render() {
    const { camList,totalMap } = this.state;
    return <div>
      {camList && camList.map((o, i) => <div className="chart" key={i}>
        <h4>{o.name} {totalMap && totalMap[o.id] && 
          <span style={{float: 'right'}}>
            Total left: {totalMap[o.id].totalLeft}, 
            right: {totalMap[o.id].totalRight},
            top: {totalMap[o.id].totalTop},
            bottom: {totalMap[o.id].totalBottom}</span>}</h4>
        <canvas
          ref={el => this.canvasMap[o.id] = el}
          style={{ height: 250 }}></canvas>

        <hr />
      </div>)}
    </div>
  }
}

class CCTV extends Component {

  render() {
    const { match } = this.props;
    return <div className="container-fluid">
      <div className="row">
        <div className="col-xs-12">
          <Switch>
            {/* <Route path={`${match.url}/`} exact component={() => "index"} /> */}
            <Route path={`${match.url}/`} exact component={Index} />
            <Route path={`${match.url}/config/`} exact component={Config} />
          </Switch>
        </div>
      </div>

    </div>
  }
}


export default CCTV;