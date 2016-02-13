var clickX = new Array();
var clickY = new Array();
var clickDrag = new Array();
var paint;

var colorBlack = "#444444";
var colorRed = "#E42F19";
var colorGreen = "#7ED321";
var colorBlue = "#4990E2";
var curColor = colorBlack;
var clickColor = new Array();

var lineThin = 2;
var lineMedium = 4;
var lineLarge = 6;
var curSize = lineMedium;
var clickSize = new Array();

//Setting up canvas

var canvasDiv = document.getElementById('message-canvas');
canvas = document.createElement('canvas');
canvas.setAttribute('width', '1270px');
canvas.setAttribute('height', '690px');
canvas.setAttribute('id', 'canvas');
canvasDiv.appendChild(canvas);
if(typeof G_vmlCanvasManager != 'undefined') {
	canvas = G_vmlCanvasManager.initElement(canvas);
}
context = canvas.getContext("2d");


//Mouse events

$('#canvas').mousedown(function(e) {
  var mouseX = e.pageX - this.offsetLeft;
  var mouseY = e.pageY - this.offsetTop;
		
  paint = true;
  addClick(e.pageX - this.offsetLeft, e.pageY - this.offsetTop);
  redraw();
});

$('#canvas').mousemove(function(e) {
  if(paint){
    addClick(e.pageX - this.offsetLeft, e.pageY - this.offsetTop, true);
    redraw();
  }
});

$('#canvas').mouseup(function(e) {
  paint = false;
});

$('#canvas').mouseleave(function(e) {
  paint = false;
});


//Drawing logic

function addClick(x, y, dragging) {
  clickX.push(x);
  clickY.push(y);
  clickDrag.push(dragging);
  clickColor.push(curColor);
  clickSize.push(curSize);
}

function redraw() {
  context.clearRect(0, 0, context.canvas.width, context.canvas.height); // Clears the canvas
  
  context.lineJoin = "round";
			
  for (var i=0; i < clickX.length; i++) {		
    context.beginPath();
    if (clickDrag[i] && i) {
      context.moveTo(clickX[i-1], clickY[i-1]);
     } else {
       context.moveTo(clickX[i]-1, clickY[i]);
     }
     context.lineTo(clickX[i], clickY[i]);
     context.closePath();
     context.strokeStyle = clickColor[i];
     context.lineWidth = clickSize[i];
     context.stroke();
  }
}


//Buttons
function refreshDrawing() {
	location.reload();
}

function changeColor(color) {
	this.curColor = color;
}

function changeStroke(stroke) {
	this.curSize = stroke;
}

function attachBase64Image() {
	document.getElementById("canvasBase64").value = canvas.toDataURL();
}
