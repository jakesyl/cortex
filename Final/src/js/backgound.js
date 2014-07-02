chrome.runtime.onMessage.addListener(function(message,sender,sendResponse){
  // message.searchText is the text that was captured in the popup    
  // Search/Highlight code goes here
  //thanks so
function searchText(){//finds a string in the text
  var search = ;//getting this from the document TODO define this later if the document is the search page then
  if(search){//if search === true
    chrome.tabs.query({active:true,currentWindow:true},function(tabs){
      chrome.tabs.executeScript(tabs[0].id,{file:search.js});
      chrome.tabs.sendMessage(tabs[0].id,{method:'search',searchText:search});
    });
  }
}
});

/*
To call this method: 

window.onload = function(){
  document.getElementById('searchButton').onclick = searchText;
};
*/
//http://api.jquery.com/contains-selector/
/*
"if you do a toLowerCase(), you'll want to do something like this: $(':has(some text)', $($('body').html().toLowerCase())) ... it looks ugly as hell, but *should* make for a case-insensitive search"

jakesyl: well, if you're using jquery, you should use its dom traversal functions also, that's part of the beauty of jquery is that it simplifies that interface for you so you can just do things like .parent().children().first().next().next().prev() etc to move around in the dom tree
[23:20] <Velveeta> if you're gonna use references to things like .childNodes and .nextSibling, you might as well skip using jquery and just write it in vanilla js*/
//