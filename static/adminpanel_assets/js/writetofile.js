/*
function generate_report(filename, list2d, howmany,type) {
    var text = "";
    if (type=="hourly"){
        for(var i=0; i<howmany; i++){
            for(var j=0; j<24; j++){
                text = text.concat(list2d[i][j].toString());
            }
             text = text.concat(",");
        }
        text = text.concat("\n");
    }


  var element = document.createElement('a');
  element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
  element.setAttribute('download', filename);

  element.style.display = 'none';
  document.body.appendChild(element);

  element.click();

  document.body.removeChild(element);
}

// Start file download.

