READER = window.READER || {};

READER.initializeFeedLink = function($el) {
	$el.click(function(e) {
		READER.loadContent($(this).data("feedkey"));
		e.preventDefault();
	});
}

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
		e.stopPropogation();
		e.preventDefault();
	});
	$("#feedslist .feed").each(function () {
		READER.initializeFeedLink($(this));
	});
	READER.loadContent();
}

READER.closeAddForm = function() {
	$("#add-form-wrapper").fadeOut(170);
	$('#add-form-wrapper input[type="text"]').val('');
}

READER.updateFeedUnreadCount = function($feed, count) {
	$feed.data("unread-count", count);
	if (count) {
		$feed.find(".unread-feed-count").html(" ("+count+")");
		$feed.addClass("has-unread");
	}
}

READER.updateUnreadCounts = function() {
	$.ajax({
		  url: "/reader/unreadcounts/",
		  type:"POST",
		  success:function ( response ) {
			  var data = JSON.parse(response);
			  var itemcounts = data.feeditemcounts;
			  $(".unread-feed-count").html("");
			  $(".feed").removeClass("has-unread");
			  var total = itemcounts.totalunread;
			  READER.updateFeedUnreadCount($("#unread-feed"), total);
			  delete itemcounts.totalunread;
			  document.title = READER.PAGE_TITLE + " (" + total + ")";
			  for (var key in itemcounts) {
				  READER.updateFeedUnreadCount($('.feed[data-feedkey="'+key+'"]'), itemcounts[key]);
			  }
		  }
	});
}

READER.loadContent = function(feedkey) {
	READER.updateUnreadCounts();
	
	$('#feeditemslist').hide();
	$("#loading-content").show();
	
	$.ajax({
	  url: "/reader/readercontent/",
	  data: {"feed_key": feedkey},
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
	
	READER.PAGE_TITLE = document.title;
	READER.initializeFeedLink($("#unread-feed"));
	
	$('body').click(function(e) {
		if ($("#add-area").has($(e.target)).length) {
			return;
		}
		READER.closeAddForm();
	})
	$('#add-form-wrapper .close').click(function(e) {
		READER.closeAddForm();
	})
	$("#add-button").click(function(e) {
		$("#add-form-wrapper").fadeToggle(170);
		e.preventDefault();
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
	
	$(window).focus(function() {
		READER.updateUnreadCounts();
	});
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