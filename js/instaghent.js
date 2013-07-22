if(!Array.prototype.indexOf) {
    Array.prototype.indexOf = function(needle) {
        for(var i = 0; i < this.length; i++) {
            if(this[i] === needle) {
                return i;
            }
        }
        return -1;
    };
}

Array.prototype.remove = function(from, to) {
	try {
	  var rest = this.slice((to || from) + 1 || this.length);
	  this.length = from < 0 ? this.length + from : from;
	  return this.push.apply(this, rest);
	} catch(err) {
		console.log(err)
	}
};


if (!localStorage) localStorage = [];

var upghented = localStorage["upghented"] ? localStorage["upghented"].split(",") : [];
var downghented = localStorage["downghented"] ? localStorage["downghented"].split(",") : [];

var offset = 10;
var photo_array = null;
var lastWidth = 0;


function init() {
	if((navigator.userAgent.match(/iPhone/i)) || (navigator.userAgent.match(/iPod/i)) || (navigator.userAgent.match(/iPad/i))) {
	    $(".photo").click(function(){
	        //we just need to attach a click event listener to provoke iPhone/iPod/iPad's hover event
	        //strange
	    });
	}

	$(".upghent").click(function() {
		photo = $(this);
		if (upghented.indexOf(photo.attr("data-id")) == -1) {
			upghented = upghented.concat(photo.attr("data-id"));
			if (localStorage) localStorage["upghented"]=upghented;
			$("#ghent-meter").html(eval($("#ghent-meter").html())+1)
			$.post("/upghent/"+photo.attr("data-id"))
			if (downghented.indexOf(photo.attr("data-id")) == -1) {
				downghented.remove(downghented.indexOf(photo.attr("data-id")));
				if (localStorage) localStorage["downghented"]=downghented;
			}
		}
	})
	$(".downghent").click(function() {
		photo = $(this);
		if (downghented.indexOf(photo.attr("data-id")) == -1) {
			downghented = downghented.concat(photo.attr("data-id"));
			if (localStorage) localStorage["downghented"]=downghented;
			$.post("/downghent/"+photo.attr("data-id"))
			$("#ghent-meter").html(eval($("#ghent-meter").html())-1)
			if (upghented.indexOf(photo.attr("data-id")) == -1) {
				upghented.remove(upghented.indexOf(photo.attr("data-id")));
				if (localStorage) localStorage["upghented"]=upghented;
			}
		}
	})
}


    // only call this when either the data is loaded, or the windows resizes by a chunk
    var f = function()
    {
        lastWidth = $("div#picstest").innerWidth();
        $("div.picrow").width(lastWidth);
        processPhotos(photo_array);
    };
    
    if (instaghent.sortingMethod == "author") {
		$.getJSON("/by-json/"+instaghent.author, null, function(data, status) {
	        photo_array = data;
	        f();
	})} else if (instaghent.sortingMethod == "tag") {
        $.getJSON("/gf13/"+"0", null, function(data, status) {
            photo_array = data;
            f();
    })} else  {
        $.getJSON("/more/"+instaghent.sortingMethod+"/0", null, function(data, status) {
            photo_array = data;
            $("#pics .picrow.init").remove();
            f();
    })}
    
    $(window).resize(function() { 
        var nowWidth = $("div#picstest").innerWidth();
        
        f();
        // test to see if the window resize is big enough to deserve a reprocess
        if( nowWidth * 1.1 < lastWidth || nowWidth * 0.9 > lastWidth )
        {
            // if so call method
            //f();
        }
    });
	

$(window).scroll(function(){
	if ($(window).scrollTop() == $(document).height() - $(window).height())
	{
		update();
	}
}); 

function update() {
    if (instaghent.sortingMethod == "author") {
        //
    } else if (instaghent.sortingMethod == "tag") {
        $.getJSON("/gf13/"+offset, null, function(data, status) {
            $('<div class="picrow"></div>').appendTo("#pics")
            photo_array = photo_array.concat(data);
            f();
            offset += 10;
    })} else  {
        $.getJSON("/more/"+instaghent.sortingMethod+"/"+offset, null, function(data, status) {
            $('<div class="picrow"></div>').appendTo("#pics")
            photo_array = photo_array.concat(data);
            f();
            offset += 10;
    })}

	
}

function processPhotos(photos)
{
    // divs to contain the images
    var d = $("div.picrow");
    
    // get row width - this is fixed.
    var w = d.eq(0).innerWidth();
    
    // initial height - effectively the maximum height +/- 10%;
    var h = 524;
    // margin width
    var border = 10;
    
    // store relative widths of all images (scaled to match estimate height above)
    var ws = [];
    $.each(photos, function(key, val) {
        var wt = parseInt(612, 10);
        var ht = parseInt(612, 10);
        if( ht != h ) { wt = Math.floor(wt * (h / ht)); }
        ws.push(wt);
    });

    // total number of images appearing in all previous rows
    var baseLine = 0; 
    var rowNum = 0;
    
    while(rowNum++ < d.length)
    {
        var d_row = d.eq(rowNum-1);
        d_row.empty();
        
        // number of images appearing in this row
        var c = 0; 
        // total width of images in this row - including margins
        var tw = 0;
        
        // calculate width of images and number of images to view in this row.
        while( tw * 1.1 < w)
        {
            tw += ws[baseLine + c++] + border * 2;
        }
    
        // Ratio of actual width of row to total width of images to be used.
        var r = w / tw; 
        
        // image number being processed
        var i = 0;
        // reset total width to be total width of processed images
        tw = 0;
        // new height is not original height * ratio
        var ht = Math.floor(h * r);
        while( i < c )
        {
            var photo = photos[baseLine + i];
            // Calculate new width based on ratio
            var wt = Math.floor(ws[baseLine + i] * r);
            // add to total width with margins
            tw += wt + border * 2;
            // Create image, set src, width, height and margin
            (function() {
            	if (photo) {
	                var img = $('<img/>', {title: "@"+photo.author, class: "photo", src: photo.standard, width: wt, height: ht}).css("margin", border + "px");
	                var url = "/by/" + photo.author + "/" + photo.ID;
	                var anc = $("<a/>", {href: url});
	                anc.append(img)
	                d_row.append(anc);
	            }
            })();
            i++;
        }
        
        // if total width is slightly smaller than 
        // actual div width then add 1 to each 
        // photo width till they match
        i = 0;
        while( tw < w )
        {
            var img1 = d_row.find("img:nth-child(" + (i + 1) + ")");
            img1.width(img1.width() + 1);
            i = (i + 1) % c;
            tw++;
        }
        // if total width is slightly bigger than 
        // actual div width then subtract 1 from each 
        // photo width till they match
        i = 0;
        while( tw > w )
        {
            var img2 = d_row.find("img:nth-child(" + (i + 1) + ")");
            img2.width(img2.width() - 1);
            i = (i + 1) % c;
            tw--;
        }
        
        // set row height to actual height + margins
        d_row.height(ht + border * 2);
    
        baseLine += c;
    }
}

init();