/**
 * Created by haier on 2017-11-24.
 */
//ajax 实现点赞功能

$(".diggit").on("click", function () {
    if($.cookie("username")){
        $.ajax({
        url: "/blog/poll/",
        type: "POST",
        headers: {"X-CSRFToken": $.cookie('csrftoken')},
        data: {
             article_id:$(".datasave").text()
        },
        success: function (data) {
            var dat = JSON.parse(data);
            if (dat.state) {
                var val = parseInt($("#digg_count").html()) + 1;//parseInt 把字符串转化为Int类型
                $("#digg_count").html(val)
            }
            else if (dat.is_repeat) {
                $(".diggnum_error").html("不能重复点赞").css("color", "red")
            }
        }

    })
    }
    else{
        location.href="/login/?next="+$.cookie("next_path")
    }
});

