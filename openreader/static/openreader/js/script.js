READER = window.READER || {};

READER.initializeFeedslist = function() {
	$(".feed .close").click(function() {
		$.ajax({
		  url: "/reader/removefeed/",
		  data: {"key": $(this).parent().data("feedkey")},
		  type:"POST",
		  success:function ( response ) {
			  var data = JSON.parse(response);
			  $("#feedslist").html(data.feedslist);
			  READER.initializeFeedslist();
		  }
		});
	});
	READER.loadContent();
}

READER.closeAddForm = function() {
	$("#add-form-wrapper").fadeOut(170);
	$('#add-form-wrapper input[type="text"]').val('');
}

READER.loadContent = function() {
	$('#feeditemslist').hide();
	$("#loading-content").show();
	
	$.ajax({
	  url: "/reader/readercontent/",
	  success:function ( response ) {
		  var data = JSON.parse(response);
		  $("#feeditemslist").html("");
		  for (var i = 0; i < data.feeditemslist.length; i++) {
			  var feeditem = data.feeditemslist[i];
			  $("#feeditemslist").append(feeditem.content);
		  }
			$("#loading-content").hide();
			$('#feeditemslist').show();
	  }
	});
}

READER.initReader = function() {
	$('body').click(function(e) {
		if ($("#add-area").has($(e.target)).length) {
			return;
		}
		READER.closeAddForm();
	})
	$('#add-form-wrapper .close').click(function(e) {
		READER.closeAddForm();
	})
	$("#add-button").click(function() {
		$("#add-form-wrapper").fadeToggle(170);
	});
	
	$("#add-form").ajaxForm({success: function(responseText, statusText, xhr, $form) {
		var result = JSON.parse(responseText);
		if (result.message) {
			$("#add-form-message").html(result.message);
		} else {
			$("#feedslist").html(result.feedslist);
			READER.initializeFeedslist();
			READER.closeAddForm();
		}
	}});
	READER.initializeFeedslist();
}

$(document).ready(function () {
	
	switch(PAGE_NAME) {
		case "reader":
			READER.initReader();
			break;
	}
});


function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
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
$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
        	var csrftoken = getCookie('csrftoken');
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});