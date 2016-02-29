/**
 * Created by alexl_000 on 2/22/2016.
 */

//$(document).ready(function(){
//    $.getJSON('champion.json', function(data){
//        console.log(data);
//        var result = eval(data);
//    });
//
//    for(var key in result){
//        console.log(key);
//    }
//});
//
//$.getJSON('champion.json', function(response){
//    console.log(response.data.Aatrox.key);
//    console.log(Object.keys(response.data));
//
//    var champNameList = Object.keys(response.data);
//    //$.each(keys, function(index, value){
//    //    console.log(index + ':' + value);
//    //});
//    console.log(response.data['Aatrox'].key);
//
//    console.log("");
//    return response;
//});


function findchampkey(name){
    $.getJSON('champion.json', function(response){
        //console.log(Object.keys(response.data));
        console.log = response.data[name].key;
    });


}

function getChamp(name){
    var val;
    $.ajaxSetup({"async":false});
    $.getJSON('champion.json', function(response){
        try{val = response.data[name];}
        catch(err){console.log('no champ found');}
    });
    return val;
}

function search(ele){
    if(event.keyCode == 13){
        var value = ele.value.charAt(0).toUpperCase() + ele.value.slice(1);
        try{
            console.log(getChamp(value).id);
            $('.champ-information-pane').fadeOut(800, function(){
                $('.champ-information-pane p').text(getChamp(value).id);
                $('<p>' + getChamp(value).blurb + '<p>').appendTo('.champ-information-pane p');

            });
            $('.champ-information-pane').fadeIn(400, function(){});
        }
        catch (e){
            console.log('champ name not found');
        }
    }
}
