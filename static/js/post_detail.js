let blockquote = document.getElementsByTagName('blockquote');
console.log(blockquote);

for (var i = 0; i < blockquote.length; i++) {
    let childrenNodes = blockquote[i].childNodes;
    let childNodesArray = Array.from(childrenNodes);
    for (var j = 0; j < childNodesArray.length; j++) {
        if (childNodesArray[j].textContent == '') {
           let index = childNodesArray.indexOf(childNodesArray[j]);
           console.log(index);
            childNodesArray.splice(index, 1);
            console.log(childNodesArray);
        }
    }
}