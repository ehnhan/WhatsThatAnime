var sourceMap = new Map()
getFile(chrome.runtime.getURL("sourcefile.csv"));

// Get the source file
function getFile(url) {
  var request = new XMLHttpRequest();

  request.onreadystatechange = function() {
    if (request.readyState == 4 && request.responseText) {
      console.log(request.responseText);
      parseText(request.responseText);
    }
  };

  request.onerror = function(error) {
    console.log(error);
  }

  request.open("GET", url, true);
  request.send();
}

// Parses a given string and stores the values in a map
function parseText(text) {
  // for each line in the file store it in the map
  var lines = text.split("\n");

  for (var index in lines) {
    var sep = lines[index].split(",");
    var code = sep[0];
    var source = sep[1];

    sourceMap.set(code, source);
  }

  // Once the source file has been stored, we update the page
  updatePage();
}

// Looks for commentfaces on the page and updates them to include the source
function updatePage() {
  var links = document.querySelectorAll("a");

  for (var i  = 0; i < links.length; ++i) {
    var link = links[i].getAttribute('href');

    if (link != null && link[0] == '#') {
      var source = checkLink(link);

      if (source != null) {
        //var name = document.createTextNode(link);
        //document.body.appendChild(name);

        var h = document.createElement("H1"); // Create a <h1> element
        h.innerHTML = "This is from: " + source;

        links[i].parentNode.insertBefore(h, links[i].nextSibling);

        links[i].onclick = test;

        //h.onclick = test;
      }
    }
  }
}

// Check the link with the source map to see if this link is for a commentface
// returns the source if found or null on miss
function checkLink(link) {
  if (sourceMap.has(link)) {
    return sourceMap.get(link);
  } else {
    console.log("no key found");
    return null;
  }
}

function test() {
  document.body.style.backgroundColor="red";

  this.style.visibility = 'hidden'; // Hide
  //element.style.visibility = 'visible'; // Show
}
