/**
 * Created by alexl_000 on 2/22/2016.
 */
/**
$(document).ready(function(){

    // jQuery methods go here...
    $('.menu-pane').css({
        position:'absolute',
        top:'0px',
        left:'-20px',
        width:'200px',
        height:'100%',
        background:'red',
        fontSize:'30px'
    }).show();

    $('.top-title').css({
        background:'blue',
        fonsSize:'40px',
        position:'absolute',
        left:'200px',
        height:'100%'
    }).show();

    $('.search-bar').css({

    })
});
 **/
//$(document).ready(function(){
//    $('.menu-pane').sideb
//}

$.getJSON("champion.json", function(data){
    console.log(data[0]);
    var items = [];
    $.each(data, function(i, field){
        items.push(field);
    });
    console.log(items[0]);
});

//var champ_json = JSON.parse("/champion.json")['data'];
//document.getElementsByClassName("champ-information-pane").innerHTML=champ_json;