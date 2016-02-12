var sourceMap = new Map();
var sitesObj;
var loadingJson = true;

var streaming_sites = ["crunchyroll", "funimation", "hulu", "netflix", "viewster", "daisuki", "animenetwork"];

var info_sites = ["myanimelist", "wikipedia"];

getFile(chrome.runtime.getURL("sites.json"));

// Get the source file
function getFile(url) {
  var request = new XMLHttpRequest();

  request.onreadystatechange = function() {
    if (request.readyState == 4 && request.responseText) {
      if (loadingJson) {
        parseJson(request.responseText);
      } else {
        parseText(request.responseText);
      }
    }
  };

  request.onerror = function(error) {
    console.log(error);
  }

  request.open("GET", url, true);
  request.send();
}

// Parses the sites json
function parseJson(json_data) {
  sitesObj = JSON.parse(json_data);

  // Once the json file has been stored, we retrieve the source file
  loadingJson = false;
  getFile(chrome.runtime.getURL("sourcefile.tsv"));
}

// Parses a given string and stores the values in a map
function parseText(text) {
  // for each line in the file store it in the map
  var lines = text.split("\n");

  for (var index in lines) {
    var sep = lines[index].split("\t");

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

  for (var i = 0; i < links.length; ++i) {
    var link = links[i].getAttribute('href');

    // check if each link is a commentface
    if (link != null && link[0] == '#') {
      var source = checkLink(link);

      if (source != null) {
        // create an element to display the source
        var div = document.createElement("div");
        div.className = "tooltip-content";

        div.innerHTML = source;

        // add the sites that are available
        var sites = getSites(source);
        if (sites != null) {
          var sitesDiv = createSitesDiv(sites);
          div.appendChild(sitesDiv);
        }

        // appends the element to the parent of the image and
        // updates the class so that it displays the source when hovered
        var parent = links[i].parentNode;
        parent.className += " tooltip-wrap";
        parent.appendChild(div);
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
    return null;
  }
}

// Get the sites object for a given show
function getSites(show_name) {
  for (index in sitesObj.shows) {
    if (sitesObj.shows[index].name == show_name) {
      return sitesObj.shows[index].sites;
    }
  }

  return null;
}

// Create a div containing lists of info and streaming sites
function createSitesDiv(sites) {
  var div = document.createElement("div");

  // check for info sites
  if (sites.info) {
    div.appendChild(createList("Info:", info_sites, sites.info));
  }

  // check for streaming sites
  if (sites.streams) {
    div.appendChild(createList("Streams:", streaming_sites, sites.streams));
  }

  return div;
}

// Create a list of the given type of sites
// innerText: text that should appear in the list
// site: array of sites to check
// json_obj: object of the show and corresponding links
function createList(innerText, sites, json_obj) {
  var div = document.createElement("div");
  div.innerHTML = innerText;

  var list = document.createElement("ul");

  for (index in sites) {
    var site = sites[index];
    if (json_obj[site]) {
      // Create a list item element to add to the list
      var li = document.createElement('li');
      var a = document.createElement('a');

      a.setAttribute('href', json_obj[site]);
      a.innerHTML = site;

      li.appendChild(a);
      list.appendChild(li);
    }
  }

  div.appendChild(list);

  return div;
}
