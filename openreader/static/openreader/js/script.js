READER = window.READER || {};

READER.initializeFeedLink = function($el) {
	$el.click(function(e) {
		READER.loadContent($(this).data("feedkey"));
		e.preventDefault();
	});
}

READER.initializeFeedslist = function(feedkey) {
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
		if ($(this).data("feedkey") == feedkey) {
			$(this).addClass("being-read");
		}
	});
	READER.loadContent(feedkey);
}

READER.closeAddForm = function() {
	$("#add-form-wrapper").fadeOut(170);
	$('#add-form-wrapper input[type="text"]').val('').blur();
}

READER.updateFeedUnreadCount = function($feed, count) {
	$feed.data("unread-count", count);
	$feed.find(".unread-feed-count").html("");
	$feed.removeClass("has-unread");
	if (count) {
		$feed.find(".unread-feed-count").html(" ("+count+")");
		$feed.addClass("has-unread");
	}
}

READER.setPageTitle = function(count) {
	document.title = READER.PAGE_TITLE + (count ? " (" + count + ")" : "");
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
			  READER.setPageTitle(total);
			  for (var key in itemcounts) {
				  READER.updateFeedUnreadCount($('.feed[data-feedkey="'+key+'"]'), itemcounts[key]);
			  }
		  }
	});
}

READER.loadContent = function(feedkey) {
	READER.updateUnreadCounts();
	$('.feed').removeClass("being-read");
	if (feedkey) {
		$('.feed[data-feedkey="'+feedkey+'"]').addClass("being-read");
	} else {
		$('.all-feeds').addClass("being-read");
	}
	
	$('#feeditemslist').hide();
	$("#loading-content").show();
	
	var $dummy = jQuery('<div/>');
	
	$.ajax({
	  url: "/reader/readercontent/",
	  data: {"feed_key": feedkey},
	  success:function ( response ) {
			var data = JSON.parse(response);
			$("#feeditemslist").html("");
			for (var i = 0; i < data.feeditemslist.length; i++) {
				var feeditem = data.feeditemslist[i];
				$dummy.html(READER.itemTemplate(feeditem));
				$dummy.find('a').attr('target', '_blank');
				$("#feeditemslist").append($dummy.html());
			}
			if (! data.feeditemslist.length) {
				$("#feeditemslist").append($("#no-feed-items").clone());
			}
			$("#loading-content").hide();
			$('#feeditemslist').show();
			$('.feed-item').click(function() {
				READER.readItem($(this));
			});
	  }
	});
}

READER.readItem = function($item) {
	if ($item.hasClass("read")) {
		return;
	}
	var total = Math.max($("#unread-feed").data("unread-count") - 1,0);
	READER.updateFeedUnreadCount($("#unread-feed"), total);
	READER.setPageTitle(total);
	var $feed = $('.feed[data-feedkey="'+$item.data("feedkey")+'"]');
	var feedTotal = Math.max($feed.data("unread-count") - 1, 0);
	READER.updateFeedUnreadCount($feed, feedTotal);
	$item.addClass("read");
	
	$.ajax({
		  url: "/reader/readitem/",
		  data: {"item_key": $item.data("feeditemkey")},
		  type: "POST"
	});
}

READER.initReader = function() {
	
	READER.PAGE_TITLE = document.title;
	READER.initializeFeedLink($("#unread-feed"));
	READER.itemTemplate = _.template($("#item-template").html());
	
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
		// TODO: focus field on show. blur on hide. 
		e.preventDefault();
	});
	
	$("#add-form").ajaxForm({success: function(responseText, statusText, xhr, $form) {
		var result = JSON.parse(responseText);
		if (result.message) {
			$("#add-form-message").html(result.message);
		} else {
			$("#feedslist").html(result.feedslist);
			READER.initializeFeedslist(result.feedkey);
			READER.closeAddForm();
		}
	}});
	READER.initializeFeedslist();
	
	$(window).focus(function() {
		READER.updateUnreadCounts();
	});
	setInterval(READER.updateUnreadCounts, 30 * 60 * 1000);
	
	$('.content').scroll(function() {
		$(".feed-item").each(function() {
			if ($(this).offset().top + $(this).height() - $('.content').height() < 0) {
				READER.readItem($(this));
			}
		});
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