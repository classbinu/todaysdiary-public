//주제 로딩
function topicShow () {
    searching = document.querySelector('#searching');
    topic = document.querySelector('#topic');
    topicButtonBefore = document.querySelector('#topicButtonBefore');
    topicButtonAfter = document.querySelector('#topicButtonAfter');
    topicAd = document.querySelector('#topicAd');
    postList = document.querySelector('#postList');
    
    searching.style.display = "none";
    topic.style.display = "block";
    topicButtonBefore.style.display = "none";
    topicButtonAfter.style.display = "block";
    topicAd.style.display = "block";
    postList.style.display = "block";
}