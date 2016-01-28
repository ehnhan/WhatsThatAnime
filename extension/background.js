// Called when the user clicks on the browser action.
chrome.browserAction.onClicked.addListener(function(tab) {
  console.log('Starting');

  chrome.tabs.executeScript({file: "show.js"});
});
