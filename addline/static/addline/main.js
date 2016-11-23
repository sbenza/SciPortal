$(function() {

    // Submit expLine on submit event
    $('#expLine-form').on('submit', function(event){
        event.preventDefault();
        console.log("form submitted!");  // sanity check
        create_expLine();
    });
    // AJAX for posting
    function create_expLine() {
        console.log("create expLine is working!"); // sanity check
        $.ajax({
            url : "addExpLine/", // the endpoint
            type : "POST", // http method
            data : {
                name : $('#exp-Name').val(),
                description : $('#exp-Description').val()
                }, // data sent with the post request
            // handle a successful response
            success : function(json) {
                console.log("success expLine is working!"); // sanity check
                $('#exp-Name').val('');
                $('#exp-Description').val('');// remove the value from the input
                console.log(json); // log the returned json to the console
                $("#expLineList").prepend("<li><a href='/addline/"+json.expLineId+"/'>"+json.expName+"</a></li>");
                console.log("success"); // another sanity check
            },
            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    }

    // Submit awkf on submit event
    $('#awkf-form').on('submit', function(event){
        event.preventDefault();
        console.log("form submitted!");  // sanity check
        create_wkf();
    });
    // AJAX for posting
    function create_wkf() {
        console.log("create wkf is working!"); // sanity check
        $.ajax({
            url : "", // the endpoint
            type : "POST", // http method
            data : {
                name : $('#wkf-Name').val(),
                description : $('#wkf-Description').val()
                }, // data sent with the post request
            // handle a successful response
            success : function(json) {
                console.log("success wkf is working!"); // sanity check
                $('#wkf-Name').val('');// remove the value from the input
                $('#wkf-Description').val('');// remove the value from the input
                console.log(json); // log the returned json to the console
                $("#wkfList").prepend("<li><a href='/addline/"+json.expLineId+"/addAbstractWkf/"+json.wkfId+"/'>"+json.wkfName+"</a></li>");
                console.log("success"); // another sanity check
            },
            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    }


    // Submit ela on submit event
    $('#ELA-form').on('submit', function(event){
        event.preventDefault();
        console.log("form submitted!");  // sanity check
        addELA();
    });
    // AJAX for posting
    function addELA() {
        console.log("create ELA is working!"); // sanity check
        var checkbox_value = '';    //Checked dependency to string
        $(":checkbox").each(function () {
        var ischecked = $(this).is(":checked");
        if (ischecked) {
            checkbox_value += $(this).val() + " ";
        }
        });
        
        $.ajax({
            url : "addELAct/", // the endpoint
            type : "POST", // http method
            data : {
                id : $('#expid').val(),
                name : $('#name').val(),
                operation :$('#operation').val(),
                variant : $('#variant').val(),
                optional : $('#optional').val(),
                dependency : checkbox_value
                }, // data sent with the post request
            // handle a successful response
            success : function(json) {
                console.log($('#name').val());
                console.log("success expLine is working!"); // sanity check
                
                $('#name').val(''); // remove the value from the input
                console.log(json); // log the returned json to the console
                console.log("success"); // another sanity check
                
                window.location.reload(true);
            },
            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    }
    //adding new activity to the derived workflow AND the expline activity
    $('#addAA-form').on('submit', function(event){
        event.preventDefault();
        console.log("form submitted!");  // sanity check
        addAA();
    });
    // AJAX for posting
    function addAA() {
        console.log("create AA is working!"); // sanity check
        
        $.ajax({
            url : "", // the endpoint
            type : "POST", // http method
            data : {
                name : $('#aact-name').val(),
                description : $('#aact-description').val(),
                func : 'addAA'
                
                }, // data sent with the post request
            // handle a successful response
            success : function(json) {
                console.log("success addAA is working!",$('#Name').val(),$('#Description').val()); // sanity check
                window.location.reload(true);
            },
            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    }
    //adding the selected activities to the derived workflow
    $('#aact-form').on('submit', function(event){
        event.preventDefault();
        console.log("form submitted!");  // sanity check
        selectAA();
    });
    // AJAX for posting
    function selectAA() {
        console.log("create AA is working!"); // sanity check
        var checkbox_value = '';    //Checked dependency to string
        $(":checkbox").each(function () {
        var ischecked = $(this).is(":checked");
        if (ischecked) {
            checkbox_value += $(this).val() + " ";
        }
        });
        
        $.ajax({
            url : "", // the endpoint
            type : "POST", // http method
            data : {
                elaid : $('#elaid').val(),
                workflowid : $('#workflowid').val(),
                activities : checkbox_value,
                func : 'selectAA'
                
                }, // data sent with the post request
            // handle a successful response
            success : function(json) {
                console.log("success addAA is working!"); // sanity check
                if (json.text !== ''){
                window.confirm(json.text)}
                
                window.location.reload(true);
                
            },
            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    }
    // validate expLine on submit event
    $('#expLine-check').on('submit', function(event){
        event.preventDefault();
        console.log("checking expLine");  // sanity check

        checkExp();

    });
    function checkExp(){
        $.ajax({
            url : "addELAct/", // the endpoint
            type : "PUT", // http method
            success : function(json) {

                console.log("expLine checked"); // another sanity check
                console.log(json); // log the returned json to the console
                $("#connected").children().remove()
                $("#connected").prepend("<li><h3> "+json.text+"</h3></li>"); 
                $("#cardinality").children().remove()
                $("#cardinality").prepend("<li><h3> "+json.cardinality_text+"</h3></li>");

            },
            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    }
    // validate expLine on submit event
    $('#wkf-check').on('submit', function(event){
        event.preventDefault();
        console.log("checking wkf");  // sanity check

        checkWkf();

    });
    function checkWkf(){
        $.ajax({
            url : "", // the endpoint
            type : "POST", // http method
            data : {
                func : 'checkWkf',
            },
            success : function(json) {

                console.log("expLine checked"); // another sanity check
                console.log(json.text); // log the returned json to the console
                $("#connected").children().remove()
                $("#connected").prepend("<li><h3> "+json.text+"</h3></li>"); 
                $("#cardinality").children().remove()
                $("#cardinality").prepend("<li><h3> "+json.cardinality_text+"</h3></li>");


            },
            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    }
    
    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});



