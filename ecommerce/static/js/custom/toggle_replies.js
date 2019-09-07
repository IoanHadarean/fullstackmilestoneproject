//Get HTML elements
var toggleReplies = document.getElementsByClassName('toggle-replies');

// All comment numbers array
var commentNumbersArray = [];

// Loop through all the toggle-replies p tags
for (let i = 0; i < toggleReplies.length; i++) {

    // Split the toggle-reply classList by '-'
    let toggleCommentClassSplit = toggleReplies[i].classList[2].split('-');

    /*Get the comment number from the class and
    push it to the commentNumbersArray
    */
    let commentNumber = toggleCommentClassSplit[2];
    commentNumbersArray.push(commentNumber);
}

// Loop through the comment numbers in the commentNumbersArray
for (let i = 0; i < commentNumbersArray.length; i++) {

    //Add click event listener for toggle-reply
    toggleReplies[i].addEventListener('click', function() {
        
        // Get the current comment number as an integer
        let currentCommentNumber = parseInt(commentNumbersArray[i], 10);
        
        // Get the replies corresponding to the comment number
        let commentReplies = document.getElementsByClassName('reply-' + currentCommentNumber);
        
        // Get the toggle reply text and reply count
        let toggleReplyText = this.children[0].innerHTML;
        let toggleReplyTextSplit = toggleReplyText.split(" ");
        let replyCount = toggleReplyTextSplit[1];
        
        /*If the first part of the toggle text is 'View',
        show the replies and change the first part of the
        toggle text to 'Hide' + toggle the icon.
        If the first part of the toggle text is 'Hide',
        hide the replies and change the first part of the
        toggle text to 'View' + toggle the icon.
        */
        if (toggleReplyTextSplit[0] == 'View') {
            this.children[1].className = 'ml-2 mt-2 fa fa-angle-up';
            if (toggleReplyText == 'View reply') {
                this.children[0].innerHTML = 'Hide reply';
                for (let j = 0; j < commentReplies.length; j++) {
                    commentReplies[j].style.display = 'block';
                }
            }
            else if (toggleReplyText == 'View ' + replyCount + ' replies') {
                this.children[0].innerHTML = 'Hide ' + replyCount + ' replies';
                for (let j = 0; j < commentReplies.length; j++) {
                    commentReplies[j].style.display = 'block';
                }
            }
        }
        else {
            this.children[1].className = 'ml-2 mt-2 fa fa-angle-down';
            if (toggleReplyText == 'Hide reply') {
                this.children[0].innerHTML = 'View reply';
                for (let j = 0; j < commentReplies.length; j++) {
                    commentReplies[j].style.display = 'none';
                }
            }
            else {
                this.children[0].innerHTML = 'View ' + replyCount + ' replies';
                for (let j = 0; j < commentReplies.length; j++) {
                    commentReplies[j].style.display = 'none';
                }
            }
        }
    });
}
