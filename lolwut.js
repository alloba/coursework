/**
 * Created by alexl_000 on 2/22/2016.
 */

$(document).ready(function(){

});

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
        var givenID = ele.value.charAt(0).toUpperCase() + ele.value.slice(1);
        try {

            console.log(getChamp(givenID).id);
            $('.champ-information-pane').fadeOut(400, function(){
                $(':hidden').show(1000);
                gatherInfo(givenID);
                $('.champ-information-pane').fadeIn(400, function(){});

            });
        }
        catch (e){
            console.log('champ name not found');
        }
    }
}
function gatherInfo(val){
    $('.champ-information-pane .name').text(getChamp(val).id);
    $('.champ-image').attr('src', 'Champion_Images/' + val + '.jpg');
    /*
    STARTING class .starting-stats
    hp id           hp
    armor id        armor
    hpregen         hpregen
    attackdamage    attackdamage
    mana            mp
    spell block     spellblock
    manaregen       mpregen
    attackspd       attackspeedoffset
    movement        movespeed
    attkrange       attackrange
    crit            crit

    PERLEVEL
    hp              hpperlevel
    spellblock      spellblockperlevel
    crit            critperlevel
    mana            mpperlevel
    hpregen         hpregenperlevel
    attkdmg         attackdamageperlevel
    armor           armorperlevel
    manaregen       mpregenperlevel
    attkspd         attackspeedperlevel
     */
    $('#hp').text(getChamp(val).stats.hp);
    $('#armor').text(getChamp(val).stats.armor);
    $('#hpregen').text(getChamp(val).stats.hpregen);
    $('#attackdamage').text(getChamp(val).stats.attackdamage);
    $('#mp').text(getChamp(val).stats.mp);
    $('#spellblock').text(getChamp(val).stats.spellblock);
    $('#mpregen').text(getChamp(val).stats.mpregen);
    $('#attackspeedoffset').text(getChamp(val).stats.attackspeedoffset);
    $('#movespeed').text(getChamp(val).stats.movespeed);
    $('#attackrange').text(getChamp(val).stats.attackrange);
    $('#crit').text(getChamp(val).stats.crit);

    $('#hpperleve').text(getChamp(val).stats.hpperlevel);
    $('#spellblockperlevel').text(getChamp(val).stats.spellblockperlevel);
    $('#critperlevel').text(getChamp(val).stats.critperlevel);
    $('#mpperlevel').text(getChamp(val).stats.mpperlevel);
    $('#hpregenperlevel').text(getChamp(val).stats.hpregenperlevel);
    $('#attackdamageperlevel').text(getChamp(val).stats.attackdamageperlevel);
    $('#armorperlevel').text(getChamp(val).stats.armorperlevel);
    $('#mpregenperlevel').text(getChamp(val).stats.mpregenperlevel);
    $('#attackspeedperlevel').text(getChamp(val).stats.attackspeedperlevel);

}