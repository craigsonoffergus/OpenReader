READER = window.READER || {};
READER.feeditemslist = [];

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
	$("#add-form-message").html("");
	$("#add-form-wrapper").removeClass("shown");
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

READER.showNextItems = function(feedkey, showRead) {
	var $dummy = jQuery('<div/>');
	var numToRead = Math.min(10, READER.feeditemslist.length);
	for (var i = 0; i < numToRead; i++) {
		var feeditem = READER.feeditemslist[i];
		$dummy.html(READER.itemTemplate(feeditem));
		$dummy.find('a').attr('target', '_blank');
		$("#feeditemslist").append($dummy.html());
	}
	READER.feeditemslist = READER.feeditemslist.slice(numToRead);
	
	if (!numToRead) {
		READER.updateUnreadCounts();
	}
	
	if (READER.feeditemslist.length) {
		var $loading = $("#loading-feed-items").clone();
		$("#feeditemslist").append($loading);
		$loading.data("feedkey", feedkey);
		$loading.data("showRead", showRead);
		READER.checkToLoadMore();
	}
	$("#loading-content").hide();
	$('#feeditemslist').show();
	$('.feed-item').not(".javascripted").click(function() {
		READER.readItem($(this));
	}).addClass("javascripted");
	
}

READER.loadContent = function(feedkey, showRead) {
	if (READER.IS_LOADING) {
		return;
	}
	READER.IS_LOADING = true;
	READER.updateUnreadCounts();
	$('.feed').removeClass("being-read");
	if (feedkey) {
		$('.feed[data-feedkey="'+feedkey+'"]').addClass("being-read");
	} else {
		$('.all-feeds').addClass("being-read");
	}
	
	if (! READER.feeditemslist.length) {
		$('#feeditemslist').hide();
		$("#loading-content").show();
		$.ajax({
		  url: "/reader/readercontent/",
		  data: {"feed_key": feedkey, "show_read": showRead ? "1" : ""},
		  success:function ( response ) {
				var data = JSON.parse(response);
				$("#feeditemslist").html("");
				if (! data.feeditemslist.length) {
					$("#feeditemslist").append($("#no-feed-items").clone());
					var $showUnread = $("#feeditemslist .show-read-items");
					$showUnread.click(function(e) {
						setTimeout(READER.loadContent(feedkey, true), 5);
						e.preventDefault();
					})
				}
				READER.feeditemslist = data.feeditemslist;
				READER.showNextItems(feedkey, showRead);
				READER.IS_LOADING = false;
		  }
		});
	} else {
		$("#feeditemslist .loading-feed-items").remove();
		READER.showNextItems(feedkey, showRead);
		
		READER.IS_LOADING = false;
	}
}

READER.checkToLoadMore = function() {
	var $loading = $("#feeditemslist .loading-feed-items");
	if (! $loading.length || READER.IS_LOADING) {
		if (! $("#feeditemslist .feed-item").not(".read").length ) {
			READER.updateUnreadCounts();
		}
		return;
	}
	if ($loading.offset().top < $('.content').height() + 40) {
		READER.loadContent($loading.data("feedkey"), $loading.data("showRead"));
	}
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
		if($("#add-form-wrapper").hasClass("shown")) {
			READER.closeAddForm();
		} else {
			$("#add-form-wrapper").fadeIn(170);
			$("#add-form-wrapper").addClass("shown");
			$("#add-form-wrapper input[type='text']").focus();
		}
		e.preventDefault();
	});
	
	$("#add-form").ajaxForm({
		beforeSubmit: function(arr, $form, options) { 
			$("#add-form .add-submit-button").css("display","none");
			$("#add-form .add-form-spinner").css("display","block");
		},
		success: function(responseText, statusText, xhr, $form) {
			var result = JSON.parse(responseText);
			$("#add-form-message").html("");
			if (result.message) {
				$("#add-form-message").html(result.message);
			} else {
				$("#feedslist").html(result.feedslist);
				READER.initializeFeedslist(result.feedkey);
				READER.closeAddForm();
			}
			$("#add-form .add-submit-button").css("display","block");
			$("#add-form .add-form-spinner").css("display","none");
		}
	});
	READER.initializeFeedslist();
	
	$(window).focus(function() {
		READER.updateUnreadCounts();
	});
	setInterval(READER.updateUnreadCounts, 15 * 60 * 1000);
	
	$('.content').scroll(function() {
		$(".feed-item").each(function() {
			if ($(this).offset().top + $(this).height() - $('.content').height() < 0) {
				READER.readItem($(this));
			}
		});
		READER.checkToLoadMore();
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