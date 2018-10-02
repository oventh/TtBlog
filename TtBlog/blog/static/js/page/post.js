
var postId = '';
var recomment = '';
var csrfmiddlewaretoken = '';

function saveComment() {
    var user = $("#inptCreator").val();
    var content = $("#txtContent").val();
    if(user == '' || content == ''){
        alert("请输入必要的评论内容！");
        return;
    }

    $.post('/api/savecomment/', {
        postId: postId,
        recomment: recomment,
        creator: user,
        content: content,
        csrfmiddlewaretoken: csrfmiddlewaretoken
    }, function (res) {
        if(res.result){
            alert("保存评论已成功！");
            recomment = '';
            $("#inptCreator").val('');
            $("#txtContent").val('');
        } else{
            alert("保存评论失改，原因：" + res.err);
        }
    }, 'JSON');
}

function reply(id){
    recomment = id;
}