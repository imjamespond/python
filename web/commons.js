var socket
var handlers = {}

function createSocket(address, name) {
  socket = new WebSocket(address)
  socket.binaryType = "arraybuffer"
  socket.onclose = function(ev){
    console.log(ev)
  }
  socket.onerror = function(ev){
    console.log(ev)
  }
  socket.onmessage = function(ev){
    console.log(ev)
    handle(ev.data)
  }
  socket.onopen = function(ev){
    console.log(ev)
    socket.send(JSON.stringify({'type': 'foobar'}));
  }
  //socket.close(code?: number, reason?: string): void;
  //socket.send(data: any): void;
}

function handle(data){
  var json = JSON.parse(data)
  switch(json['type']){
    case 'ANNOTATED':
      var detectedFaces = document.getElementById("detectedFaces")
      detectedFaces.innerHTML = 
        "<img src='" + json['content'] + "' width='400px'></img>"
      // var img = detectedFaces.getElementsByTagName('img')[0]
      // img.onload = function(){ 
      //   console.log(img.width,img.height); 
      // }
      break
    case 'INFER':
      var result = document.getElementById("result")
      result.innerHTML = JSON.stringify(json['predictions']) 
      break
    default:
      break

  }

}