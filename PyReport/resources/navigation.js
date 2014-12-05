
/** Script File for Reporting **/

function RedirectOnLoad(){
	
	function setLocation(newURL, isIFrame){
	    if (isIFrame) {
			$( "#main-menu" ).fadeOut(100);
			
			parent.frames['report-iframe'].contentWindow.location.replace(newURL);
			
			$( '#main-report' ).fadeIn(500);	
			$('iframe').focus();
		}
		else {
			window.location.assign(newURL);
		}
	}

	if (window.location.hash != ''){		
		var hash = window.location.hash;
		var parseHash = hash.replace('#','');
		
		/*var query = $("td span[href*="+ parseHash +"]").attr('href');*/
		var query = "td span[href=\"" + parseHash + "/index.html\"]";
		$(query).parent().parent().attr('class','current');

		var iframeurl = parseHash;
		
		if(iframeurl.indexOf("index") == -1){
			iframeurl = iframeurl + "/index.html";
		}
		
		setLocation(iframeurl, !isIE());
	}
	else{
		$( "#main-menu" ).fadeIn(100);
		$( "#main-report" ).fadeOut(100);
	}	
};

window.onload = function(e){

	RedirectOnLoad();

	$(window).bind( 'hashchange', function() {RedirectOnLoad()});
	
	$("#main-menu tbody tr").click(function () {	 	
		/*
		var arrList = this.parentElement.children;
		var objsArray = Array.prototype.slice.call(arrList);
		objsArray.indexOf(this);
		*/
		
		
		/*var url = $(this).find("span").attr("href");*/
		var url = $(this).find("span").attr("href");
		/*var urlArr = url.split("/");
		var pUrl = urlArr[0];*/
		var pUrl = $(this).find("span").attr("href").replace("/index.html","").replace("\\index.html","");
		
		if (pUrl == '' || pUrl == undefined){}
		else{
			$( "#main-menu" ).fadeOut(300,function(){
					if(!isIE()){
						window.location.hash = pUrl;
					}
					else{
						window.location.assign(url);
					}
				}
				);
		}
     });
	
	$("#returntomenu").click(function () {
		var nURL = "index.html";
		$( "#main-report" ).fadeOut(500,function(){window.location.assign(nURL)});		
    });
	
	$("#nextbutton").click(function () {
		var nURL = $( "#main-menu tbody .current" ).next().find('span').attr('href');
				
		if(nURL != '' && nURL != undefined){
			var redirectURL = window.location.href.replace(window.location.hash,'#' + nURL.replace("/index.html",""));
			$('.current').removeClass();
			$( "#main-report" ).fadeOut(500,function(){window.location.assign(redirectURL)});
		}
    });
	
	$("#backbutton").click(function () {
		var nURL = $( "#main-menu tbody .current" ).prev().find('span').attr('href');
		
		if(nURL != '' && nURL != undefined){
			var redirectURL = window.location.href.replace(window.location.hash,'#' + nURL.replace("/index.html",""));
			$('.current').removeClass();
			$( "#main-report" ).fadeOut(500,function(){window.location.assign(redirectURL)});
		}
    });

		
};