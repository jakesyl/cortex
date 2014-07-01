chrome.runtime.onMessage.addListener(function(message,sender,sendResponse){
  // message.searchText is the text that was captured in the popup    
  // Search/Highlight code goes here
function searchText(){
  var search = document.getElementById('searchText').value;
  if(search){
    chrome.tabs.query({active:true,currentWindow:true},function(tabs){
      chrome.tabs.executeScript(tabs[0].id,{file:search.js});
      chrome.tabs.sendMessage(tabs[0].id,{method:'search',searchText:search});
    });
  }
}
});