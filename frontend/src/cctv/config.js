import React, { Component } from 'react';
// import { Link, Route, Switch } from 'react-router-dom';

import { GetJSON, Get, Post } from '../utils/ajax'; 
import Modal from '../utils/Modal';
import { Store } from '../utils/commons';

import DetectionArea from './detectionArea';

class Config extends Component {
  constructor(){
    super()
    this.state = { formdata: {}, camlist: null, cam: null, timestamp: 0};
  }

  componentDidMount() {
    Store.app.setState({ pageHeader: 'Web camera list'});
    this.getWebCamList();
  }

  getWebCamList() {
    this.setState({ camlist: null }, () => {
      GetJSON('/cctv/webcam-list', null, camlist => {
        this.setState({ camlist });
      });
    });
  }
  addWebCam() {
    const { formdata } = this.state;
    Get('/cctv/csrf-token', null, csrfmiddlewaretoken =>
      Post('/cctv/webcam-add', { csrfmiddlewaretoken, ...formdata }, rs => {
        alert("添加成功");
        this.getWebCamList();
      }))
  }
  removeWebCam(pk){
    Get('/cctv/csrf-token', null, csrfmiddlewaretoken =>
      Post('/cctv/webcam-del', { csrfmiddlewaretoken, pk }, rs => {
        alert("删除成功");
        this.getWebCamList();
      }))
  }
  configDetectionArea(){
    const { cam } = this.state;
    const pos = this.detectionArea.getPosition();
    console.log(cam, pos);
    Get('/cctv/csrf-token', null, csrfmiddlewaretoken =>
      Post('/cctv/webcam-update', { csrfmiddlewaretoken, pk: cam.pk, ...cam.fields, ...pos }, 
        rs => {
          if (rs) {
            alert("配置成功");
            this.getWebCamList();
          }
        }))
  }

  render() {
    // console.log(this.props.location);

    const { formdata, camlist, cam} = this.state;
    return <div style={{backgroundColor: 'white'}}>
      <div className="row" style={{padding: 10}}>
        <h4 className="col-md-6">webcam list</h4>
        <div className="col-md-6 text-right"> 
          <button className="btn btn-sm btn-default"
            onClick={e => this.modal_add.show()}>add</button>
        </div>
      </div>

      <table className="table  table-striped">
        <thead>
          <tr>
          <th>id</th>
          <th>name</th>
          <th>url</th>
          <th>config</th>
          </tr>
        </thead>
        <tbody>
          {camlist && camlist.map((cam, i) => <tr key={i}>
            <td>{cam.pk}</td>
            <td>{cam.fields.name}</td>
            <td>{cam.fields.address}</td>
            <td>
              <a className=" glyphicon glyphicon-cog" href="javascript:;"
                onClick={() => {
                  this.setState({ cam: null }, () =>
                    this.setState({ cam, timestamp: new Date().getTime() }));
                  this.modal.show();
                }} />
              <a className=" glyphicon glyphicon-remove" href="javascript:;"
                onClick={this.removeWebCam.bind(this, cam.pk)} />
            </td>
            </tr>
          )}

        </tbody>
      </table>

      <Modal ref={ref => this.modal = ref} 
        onConfirm={this.configDetectionArea.bind(this)}
        lg={true}
        title={'Configure detection area - ' + (cam ? cam.fields.name : '')}
        body={<div>
          {cam && <DetectionArea ref={ref => this.detectionArea = ref} cam={cam} />}
        </div>
        }/>
      <Modal ref={ref => this.modal_add = ref}
        onConfirm={this.addWebCam.bind(this)}
        title="add"
        body={
          <div className="form-horizontal">
            <div className="form-group">
              <label className="col-sm-3 control-label">name</label>
              <div className="col-sm-9">
                <input type="text" className="form-control" placeholder="name" 
                  value={formdata.name ? formdata.name: ''}
                  onChange={e => {
                    const _formdata = Object.assign({}, formdata, { 'name': e.target.value });
                    this.setState({ formdata: _formdata });
                  }} />
              </div>
            </div>
            <div className="form-group">
              <label className="col-sm-3 control-label">ip address</label>
              <div className="col-sm-9">
                <input type="text" className="form-control" placeholder="ip address" 
                  value={formdata.addr ? formdata.addr : ''}
                  onChange={e => {
                    const _formdata = Object.assign({}, formdata, {'addr': e.target.value });
                    this.setState({ formdata: _formdata});
                  }} />
              </div>
            </div>
          </div>
        } />
    </div>
  }
}

export default Config;