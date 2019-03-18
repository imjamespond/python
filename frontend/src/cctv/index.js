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
    this.state = { data: null, camlist: null }
  }

  componentDidMount() {
    this.setState({ camlist: null }, () => {
      GetJSON('/cctv/webcam-list', null, camlist => {
        this.setState({ camlist }, () => {

          camlist.map((o, i) => {
            GetJSON('/cctv/track-list', { id: o.id }, data => {

              var chartData = getData(data);

              // new Chart(this.canvasMap[o.id].getContext('2d')).Line(chartData, {
              //   responsive: true,
              //   showTooltips: true,
              //   multiTooltipTemplate: "<%= datasetLabel %> - <%= value %>"
              // });

              var ctx = this.canvasMap[o.id].getContext('2d');
              var myChart = new Chart(ctx, chartData);

            })
          })

        });
      });
    });


  }

  render() {
    const { camlist } = this.state;
    return <div>
      {camlist && camlist.map((o, i) => <div className="chart">
        <h4>{o.name}</h4>
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