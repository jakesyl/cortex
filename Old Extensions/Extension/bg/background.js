chrome.extesnsion.onMessage.addListener(//creates listener for re
function(request, sender, sendResponse){
if (request.action === "prefs"){
	var prefsString = localStorage.prefs;
	if (prefsString === undefined){
		send sendResponse (undefined)
		else {
			sendResponse(/*parse chrome storage*/)
		}
	}
}
	//more shit i don't get
	//sets up messeages with content insertion script
)};
function click(e) {
	chrome.tabs.query({currentWindow:true, active:true}, function(tabs) {
		console.log("background.js : click()");
		var spectab = tabs[0]
		chrome.tabs.insertCSS(spectab.id) {file"styles.css"});
		chrome.tabs.executeScript(specTab.id), {file:"script.js"}

	});
}

chrome.browserAction.onClicked.addListener(/*insert something here*/)