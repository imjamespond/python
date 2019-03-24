import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import { fabric } from 'fabric';
import { Get } from '../utils/ajax'; 

class DetectionArea extends Component {
  constructor() {
    super()
    this.state = { preview: null };
  }

  componentDidMount(){
    const { cam } = this.props;
    this.previewWebCam(cam.id);
  }

  previewWebCam(pk) { 
      Get('/cctv/webcam-capture', { pk }, preview => { 
        this.setState({preview});

        // var _this = this;
        // var img = document.createElement('img');
        // img.src = 'data:image/png;base64, ' + preview;
        // img.style.width = '100%';
        // img.style.height = 'auto';
        // img.onload = function(){
        //   console.log(this.width, this.height);
        //   // _this.onPreviewLoad(this.width, this.height);
        // } 

        // this.preview.innerHTML = "";
        // this.preview.appendChild(img);
        
      }); 
  }

  onPreviewLoad(previewWidth, previewHeight){
    const { cam } = this.props;
    const { left, top, width, height} = cam; 

    // create a wrapper around native canvas element (with id="c")
    var canvas = new fabric.Canvas(this.canvas);
    previewHeight && canvas.setHeight(previewHeight);
    previewWidth && canvas.setWidth(previewWidth);
    this.camWidth = previewWidth;
    this.camHeight = previewHeight;

    // create a rectangle object
    var rect = new fabric.Rect({
      left, top,
      fill: '#0000ff88',
      width: width ? width : 30,
      height: height ? height : 30
    });

    // "add" rectangle onto canvas
    canvas.add(rect);

    canvas.item(0).setControlsVisibility({ mtr: false });

    this.fcanvas = canvas;
  }

  getPosition(){
    var obj = this.fcanvas.getActiveObject() || this.fcanvas.item(0);
    const {camWidth, camHeight} = this;
    return { left: obj.left, top: obj.top, width: obj.width * obj.scaleX, height: obj.height * obj.scaleY, camWidth, camHeight};
  }

  render(){
    const { cam} = this.props;
    const { preview} = this.state;
    return <div style={{position: 'relative'}} ref={el => this.outter = el}>
      <div style={{position: 'absolute', top:0,bottom:0,left:0,right:0 }}>
        <canvas ref={ref => this.canvas = ref} style={{width:'100%', height:'100%'}} />
      </div>
      {/* <div ref={el => this.preview = el}></div> */}
      {preview && <img ref={ref => this.preview = ref } 
        style={{ width: 870, height: 'auto'}}
        src={'data:image/png;base64, ' + preview} 
        onLoad={()=>{
          console.log(this.preview.width, this.preview.height, this.outter.getBoundingClientRect()); 
          this.onPreviewLoad(870, 870/this.preview.width * this.preview.height)
        }}/>}
      {/* <img src={"/api/cctv/webcam-capture?_=" + timestamp} style={{width: '100%'}} /> */}
    </div>
  }
}

export default DetectionArea;