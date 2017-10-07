//模态框居中的控制
function centerModals(){
    $('.modal').each(function(i){   //遍历每一个模态框
        var $clone = $(this).clone().css('display', 'block').appendTo('body');
        var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
        top = top > 0 ? top : 0;
        $clone.remove();
        $(this).find('.modal-content').css("margin-top", top-30);  //修正原先已经有的30个像素
    });
}

function setStartDate() {
    var startDate = $("#start-date-input").val();
    if (startDate) {
        $(".search-btn").attr("start-date", startDate);
        $("#start-date-btn").html(startDate);
        $("#end-date").datepicker("destroy");
        $("#end-date-btn").html("离开日期");
        $("#end-date-input").val("");
        $(".search-btn").attr("end-date", "");
        $("#end-date").datepicker({
            language: "zh-CN",
            keyboardNavigation: false,
            startDate: startDate,
            format: "yyyy-mm-dd"
        });
        $("#end-date").on("changeDate", function() {
            $("#end-date-input").val(
                $(this).datepicker("getFormattedDate")
            );
        });
        $(".end-date").show();
    }
    $("#start-date-modal").modal("hide");
}

function setEndDate() {
    var endDate = $("#end-date-input").val();
    if (endDate) {
        $(".search-btn").attr("end-date", endDate);
        $("#end-date-btn").html(endDate);
    }
    $("#end-date-modal").modal("hide");
}

function goToSearchPage(th) {
    var url = "/search?";
    var id=$(th).parent().find('#area-btn').attr('area-id');
    if(undefined==id) id='';
    url += ("area_id=" +id);
    url += "&";
    var areaName = $(th).parent().find('#area-btn').html();
    if ('选择城区' == areaName) areaName="";
    url += ("area_name=" + areaName);
    url += "&";
    var start_date=$(th).parent().find('#start-date-btn').html();
    if('入住日期'==start_date) start_date='';
    url += ("start_date=" + start_date);
    url += "&";
     var end_date=$(th).parent().find('#end-date-btn').html();
    if('离开日期'==end_date) end_date=''
    url += ("end_date=" + end_date);
    location.href = url;
}

$(document).ready(function(){
    $.get("/api/check_login", function(data) {
        if ("0" == data.errcode) {
            $(".top-bar>.user-info>.user-name").html(data.data.name);
            $(".top-bar>.user-info").show();
        } else {
            $(".top-bar>.register-login").show();
        }
    }, "json");
    $.get("/index", function(data){
        if ("0" == data.errcode) {
            $(".swiper-wrapper").html(template("swiper-houses-tmpl", {houses:data.houses}));
            $(".area-list").html(template("area-list-tmpl", {areas:data.areas}));
            var mySwiper = new Swiper ('.swiper-container', {
                loop: true,
                autoplay: true,
                speed:100,
                autoplayDisableOnInteraction: true,
                pagination: '.swiper-pagination',
                paginationClickable: true
            });
        }
    });
    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
    $(window).on('resize', centerModals);               //当窗口大小变化的时候
    $("#start-date").datepicker({
        language: "zh-CN",
        keyboardNavigation: false,
        startDate: "today",
        format: "yyyy-mm-dd"
    });
    $("#start-date").on("changeDate", function() {
        var date = $(this).datepicker("getFormattedDate");
        $("#start-date-input").val(date);
    });
})
$(".area-list a").click(function(e){
    $("#area-btn").html($(this).html());
    $("#area-btn").attr("area-id", $(this).attr("area_id"));
    // alert($(this).attr("area_id"));
    $(".search-btn").attr("area-id", $(this).attr("area-id"));
    $(".search-btn").attr("area-name", $(this).html());
    $("#area-modal").modal("hide");
});


