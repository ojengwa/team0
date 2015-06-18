var pdfDocument, canvas, pageNum, pageInterval, numPages;
 
function load(userInput) {
  canvas = document.getElementById("canvas");
  canvas.mozOpaque = true;
  pageNum = 1;
  fileName = userInput;       
  open(fileName);
} 

function open(url) {
  req = new XMLHttpRequest();
  req.open("GET", url);
  req.mozResponseType = req.responseType = "arraybuffer";
  req.expected = (document.URL.indexOf("file:") == 0) ? 0 : 200;
  req.onreadystatechange = function() {
    if (req.readyState == 4 && req.status == req.expected) {
      var data = req.mozResponseArrayBuffer || req.mozResponse || 
        req.responseArrayBuffer || req.response;
      pdfDocument = new PDFDoc(new Stream(data));
      numPages = pdfDocument.numPages;
      document.getElementById("numPages").innerHTML = numPages.toString();
      displayPage(pageNum);
    }
  };
  req.send(null);
} 

function displayPage(num) {
  if (pageNum != num)
    window.clearTimeout(pageInterval);
   
  document.getElementById("pageNumber").innerHTML = num;
   
  var page = pdfDocument.getPage(pageNum = num);
   
  var ctx = canvas.getContext("2d");
  ctx.save();
  ctx.fillStyle = "rgb(255, 255, 255)";
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.restore();
   
  var gfx = new CanvasGraphics(ctx);
   
  // page.compile will collect all fonts for us, once we have loaded them
  // we can trigger the actual page rendering with page.display
  var fonts = [];
  page.compile(gfx, fonts);
  var fontsReady = true;
   
  // Inspect fonts and translate the missing one
  var count = fonts.length;
  for (var i = 0; i < count; i++) {
    var font = fonts[i];
    if (Fonts[font.name]) {
      fontsReady = fontsReady && !Fonts[font.name].loading;
      continue;
    }
    new Font(font.name, font.file, font.properties);
    fontsReady = false;
  }
   
  function delayLoadFont() {
    for (var i = 0; i < count; i++) {
      if (Fonts[font.name].loading) {
        return;
      }
    }
    clearInterval(pageInterval);
    page.display(gfx);
  };
   
  if (fontsReady) {
    delayLoadFont();
  } else {
    pageInterval = setInterval(delayLoadFont, 10);
  }
} 

function prevPage() {
  if(pageNum > 1) {
    displayPage(pageNum - 1);
  }
}
 
function nextPage() {
  if(pageNum < numPages) {
    displayPage(pageNum + 1);
  }
}