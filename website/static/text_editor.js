const textarea = document.getElementById('tweet_textarea');
const tweet_preview = document.getElementById('tweet_preview');
const rightDiv = document.querySelector('.right');

textarea.addEventListener('input', function (event) {
    updateTweetPreview();
    scrollRightDivToBottom();
});

function updateTweetPreview() {
    const message = textarea.value;
    tweet_preview.innerText = message;
}

function scrollRightDivToBottom() {
    rightDiv.scrollTop = rightDiv.scrollHeight;
}

function delete_message(messageId) {
    fetch("/delete-message", {
        method: "POST",
        body: JSON.stringify({ messageId: messageId }),
    }).then((_res) => {
        window.location.reload()
    });
}