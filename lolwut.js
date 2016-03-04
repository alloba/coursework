/**
 * Created by alexl_000 on 2/22/2016.
 */

$(document).ready(function(){
    var champComparePane = $('.champComparePane');
    champComparePane.html($('.champInfoPane').html());
    champComparePane.css({'position':'absolute', 'top':'110px', 'left':'58%', 'width':'40%'});
});

function getChamp(name){
    var val;
    $.ajaxSetup({"async":false});
    $.getJSON('champion.json', function(response){
        try{val = response.data[name];}
        catch(err){console.log('no champ found');}
    });
    return val;
}

function search_from_menu(ele){
    if(event.keyCode == 13){
        var givenID = ele.value.charAt(0).toUpperCase() + ele.value.slice(1);
        try {
            console.log(getChamp(givenID).id);
            $('.champInfoPane').fadeOut(400, function(){
                $('.champInfoPane').show(1000);
                gatherInfo(givenID, 'champInfoPane');
            });
        }
        catch (e){
            console.log('champ name not found');
        }
    }
}

function search_from_champ_pane(ele){
    if(event.keyCode == 13) {
        var givenID = ele.value.charAt(0).toUpperCase() + ele.value.slice(1);
        try{
            console.log(getChamp(givenID).id);
            $('.champComparePane').fadeOut(400, function(){
                $('.champComparePane').show(1000);
                $('.champComparePane .search-bar-champ-pane').hide();
                gatherInfo(givenID, 'champComparePane');

            });
        }
        catch(e){
            console.log("champ name not found");
        }
    }
}

function gatherInfo(val, pane_name){
    var display_element = $('.'+pane_name);

    display_element.find('.name').text(getChamp(val).id);
    display_element.find('.champ-image').attr('src', 'Champion_Images/' + val + '.jpg');
    display_element.find('#hp').text(getChamp(val).stats.hp);
    display_element.find('#armor').text(getChamp(val).stats.armor);
    display_element.find('#hpregen').text(getChamp(val).stats.hpregen);
    display_element.find('#attackdamage').text(getChamp(val).stats.attackdamage);
    display_element.find('#mp').text(getChamp(val).stats.mp);
    display_element.find('#spellblock').text(getChamp(val).stats.spellblock);
    display_element.find('#mpregen').text(getChamp(val).stats.mpregen);
    display_element.find('#attackspeedoffset').text(getChamp(val).stats.attackspeedoffset);
    display_element.find('#movespeed').text(getChamp(val).stats.movespeed);
    display_element.find('#attackrange').text(getChamp(val).stats.attackrange);
    display_element.find('#crit').text(getChamp(val).stats.crit);

    display_element.find('#hpperlevel').text(getChamp(val).stats.hpperlevel);
    display_element.find('#spellblockperlevel').text(getChamp(val).stats.spellblockperlevel);
    display_element.find('#critperlevel').text(getChamp(val).stats.critperlevel);
    display_element.find('#mpperlevel').text(getChamp(val).stats.mpperlevel);
    display_element.find('#hpregenperlevel').text(getChamp(val).stats.hpregenperlevel);
    display_element.find('#attackdamageperlevel').text(getChamp(val).stats.attackdamageperlevel);
    display_element.find('#armorperlevel').text(getChamp(val).stats.armorperlevel);
    display_element.find('#mpregenperlevel').text(getChamp(val).stats.mpregenperlevel);
    display_element.find('#attackspeedperlevel').text(getChamp(val).stats.attackspeedperlevel);

}