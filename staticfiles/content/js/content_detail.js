

textBoxArea      = document.querySelectorAll('.textAreaBox')
askAQuestion     = document.querySelectorAll(".askAQuestion")
replyButton      = document.querySelectorAll('.replyButton')
replygroupForm   = document.querySelectorAll('.replygroup')
commentButton    = document.querySelectorAll('.commentButton')
commentReplyList = document.querySelectorAll('.commentReplyList')



for (let i = 0; i < textBoxArea.length; i++) {
    const element = textBoxArea[i];
    element.addEventListener('click',function(){
        element.classList.toggle('asQuestionHeight')
        askAQuestion[i].classList.toggle('displayAsk')
    })
    
}


for (let i = 0; i < replyButton.length; i++) {
    const element = replyButton[i];
    element.addEventListener('click',function(){
        replygroupForm[i].classList.toggle('display')
        
        
    })
    
}


for (let i = 0; i < commentButton.length; i++) {
    const element = commentButton[i];
    
    element.addEventListener('click',function(){
        console.log(i);
        
        commentReplyList[i].classList.toggle('noDisplay')
    })
    
}







