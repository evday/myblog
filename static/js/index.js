/**
 * Created by haier on 2017-11-22.
 */

$(".cate_title").mouseover(function () {
    $(this).next().slideDown(300)
}).parent().mouseleave(function () {
    $(this).children("#article").slideUp(300)
});