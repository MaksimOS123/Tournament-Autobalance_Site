var a = 0

$(document).ready(function() {
    a = $('.streamers').length
});

$(init);

function init(){
    $('.twitch_button').bind('click', Add_Twitch);
    $('.youtube_button').bind('click', Add_Youtube);
    $('#Add_Stream').bind('click', Add);
}

function Add(){
    $("div.just-razdel").append($('<div class="card streamers ' + a + '">' +
            '<div class="card-body">' +
                '<div class="form-row">' +
                    '<div class="form-group col-md-2">' +
                        '<select id="inputPlatform" class="form-control" name="inputPlatform">' +
                            '<option selected disabled>Platform</option>' +
                            '<option value="1">Twitch</option>' +
                            '<option value="2">Youtube</option>' +
                        '</select>' +
                    '</div>' +
                    '<div class="form-group col-md-2">' +
                        '<select id="inputLanguage" class="form-control" name="inputLanguage">' +
                            '<option selected disabled>Language</option>' +
                            '<option value="1">Russian</option>' +
                            '<option value="2">English</option>' +
                            '<option value="3">Russian+English</option>' +
                        '</select>' +
                    '</div>' +
                    '<div class="form-group col-md-7">' +
                        '<label class="sr-only" for="inlineFormInputGroup">Nickname</label>' +
                        '<div class="input-group mb-2">' +
                            '<div class="input-group-prepend">' +
                                '<div class="input-group-text">Nickname/Link</div>' +
                            '</div>' +
                            '<input type="text" class="form-control" id="inlineFormInputGroup" placeholder="Twitch = nickname, Youtube = Link" name="link">' +
                        '</div>' +
                    '</div>' +
                    '<div class="form-group col-md-1 text-right">' +
                        '<button class="btn btn-danger" type="button" onclick="test(' + a + ')"><i class="far fa-trash-alt"></i></button>' +
                    '</div>' +
                '</div>' +
            '</div>' +
        '</div>'));
    a += 1;
}

function Add_Twitch(){
    $("div.just-razdel").append($('<div class="card streamers ' + a + '">' +
            '<div class="card-body">' +
                '<div class="form-row">' +
                    '<div class="form-group col-md-2">' +
                        '<select id="inputPlatform" class="form-control" name="inputPlatform">' +
                            '<option value="1" selected>Twitch</option>' +
                            '<option value="2" disabled>Youtube</option>' +
                        '</select>' +
                    '</div>' +
                    '<div class="form-group col-md-2">' +
                        '<select id="inputLanguage" class="form-control" name="inputLanguage">' +
                            '<option selected disabled>Language</option>' +
                            '<option value="1">Russian</option>' +
                            '<option value="2">English</option>' +
                            '<option value="3">Russian+English</option>' +
                        '</select>' +
                    '</div>' +
                    '<div class="form-group col-md-7">' +
                        '<label class="sr-only" for="inlineFormInputGroup">Nickname</label>' +
                        '<div class="input-group mb-2">' +
                            '<div class="input-group-prepend">' +
                                '<div class="input-group-text">www.twitch.tv/</div>' +
                            '</div>' +
                            '<input type="text" class="form-control" id="inlineFormInputGroup" placeholder="Your twitch nickname. Example: it_ti953" name="link">' +
                        '</div>' +
                    '</div>' +
                    '<div class="form-group col-md-1 text-right">' +
                        '<button class="btn btn-danger" type="button" onclick="test(' + a + ')"><i class="far fa-trash-alt"></i></button>' +
                    '</div>' +
                '</div>' +
            '</div>' +
        '</div>'));
    $('.twitch_button').addClass('disabled');
    $('.twitch_button').attr('disabled', true);
    a += 1;
}

function Add_Youtube(){
    $("div.just-razdel").append($('<div class="card streamers ' + a + '">' +
            '<div class="card-body">' +
                '<div class="form-row">' +
                    '<div class="form-group col-md-2">' +
                        '<select id="inputPlatform" class="form-control" name="inputPlatform">' +
                            '<option value="1" disabled>Twitch</option>' +
                            '<option value="2" selected>Youtube</option>' +
                        '</select>' +
                    '</div>' +
                    '<div class="form-group col-md-2">' +
                        '<select id="inputLanguage" class="form-control" name="inputLanguage">' +
                            '<option selected disabled>Language</option>' +
                            '<option value="1">Russian</option>' +
                            '<option value="2">English</option>' +
                            '<option value="3">Russian+English</option>' +
                        '</select>' +
                    '</div>' +
                    '<div class="form-group col-md-7">' +
                        '<label class="sr-only" for="inlineFormInputGroup">Link</label>' +
                        '<div class="input-group mb-2">' +
                            '<div class="input-group-prepend">' +
                                '<div class="input-group-text">www.youtube.com/channel/</div>' +
                            '</div>' +
                            '<input type="text" class="form-control" id="inlineFormInputGroup" placeholder="Your youtube link. Example: UCDYXPhORtwYy8oO4EEYo8Mw" name="link">' +
                        '</div>' +
                    '</div>' +
                    '<div class="form-group col-md-1 text-right">' +
                        '<button class="btn btn-danger" type="button" onclick="test(' + a +')""><i class="far fa-trash-alt"></i></button>' +
                    '</div>' +
                '</div>' +
            '</div>' +
        '</div>'));
    $('.youtube_button').addClass('disabled');
    $('.youtube_button').attr('disabled', true);
    a += 1;
}