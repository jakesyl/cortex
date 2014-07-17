---
title: sudocode.md
---
Purpose:
Highlight urls on a users page that are found useful by an artificial intelligence algorithm in order to pave the way for more advanced ai systems and personal assistance

Attributes:
Portable (chrome)path 

Extension inner workings:
On page load:
.Search for links
.load links into function
.for loop links
.search in history
.search in bookmarks
.identify a title
.identify synonyms
.identify common words in article
.highlight links using replace text in jquery

More Detailed
.Search for links:
Function
.load links into function
.for loop links
.search in history 1 weight/ result
| chrome.history (search function)
.search in bookmarks 4 weight
| chrome.bookmarks (search function)
.identify a title
| extract url, there's gotta be an algo for this, if not make one
.identify synonyms
| this is a maybe, if you do you better be ready to use an in house (local) synonym finder
.identify common words in article
| i.e words from article that match history weight 2
.highlight links using replace text in jquery
	replace thing by that guy from clickable links