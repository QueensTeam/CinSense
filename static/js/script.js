$(document).ready(function () {

    $.get("/getAll", {}).done(function(data) {
      var movies = JSON.parse(data);
      console.log(movies);
      movies.forEach(addMovie);
    });

  $('.first-button').on('click', function () {

    $('.animated-icon1').toggleClass('open');
  });
  $('.second-button').on('click', function () {

    $('.animated-icon2').toggleClass('open');
  });
  $('.third-button').on('click', function () {

    $('.animated-icon3').toggleClass('open');
  });
});

function searchForMovies(){
  var genre = document.getElementById("genre").value;
  var decade = document.getElementById("decade").value;
  var voteavg = document.getElementById("average").value;
  var votecnt = document.getElementById("votecount").value;
  console.log(decade + " " + voteavg + " " + votecnt);
  url = "/genre/" + genre;
  $.get(url, {}).done(function(data) {
    var movies = JSON.parse(data);
    document.getElementById("gallery").innerHTML = ""
    console.log(movies);
    movies.forEach(addMovie);
  });
}


function addMovie(value){
	alt = value.title + " (" + value.release_year + ")";
  title = value.title;
	$("#gallery").append("<img src=\"https://image.tmdb.org/t/p/w600_and_h900_bestv2/" + value.poster + "\" alt=\"" + alt + "\" title=\"" + title + "\" class=\"col-12 col-lg-2  mov\"/>");
}

window.transitionToPage = function(href) {
    document.querySelector('body').style.opacity = 0
    setTimeout(function() { 
        window.location.href = href
    }, 0)
}

document.addEventListener('DOMContentLoaded', function(event) {
    document.querySelector('body').style.opacity = 1
})



 function randomovie(){
		var ltit = document.getElementsByClassName("ltitle");
		var lpi = document.getElementsByClassName("lpic");
		var lem = document.getElementById("lemon");
		var lem2 = document.getElementById("lemon2");
	   for (var i=0; i < ltit.length; i++){
	      if(ltit[i].classList.contains('closed')) {
	         ltit[i].classList.remove('closed');
	         // k++;
	      }
	      if(ltit[i].classList.contains('openli')) {
	         ltit[i].classList.remove('openli');
	         // k++;
	      }
	      if(lpi[i].classList.contains('openph'))
	      	lpi[i].classList.remove('openph');
	    }
	   var ran;
	   ran = Math.floor(Math.random() * ltit.length);
	   lem.classList.add("closed");
	lem2.classList.add("oplem");
   for(var i=0; i < ltit.length; i++){
      	if (i != ran)
         	ltit[i].classList.add('closed');
    	if (i == ran){
    		lpi[i].classList.add('openph');
    		ltit[i].classList.add('openli');
    	}
   }
	// document.getElementById("randomovie").innerHTML = "&starf;"
}
document.getElementById("randomovie").ondblclick = function reset(){
}

function openLogin(){
  var logButton = document.getElementById("loginButton");
  var logForm = document.getElementById("loginForm");
  var regForm = document.getElementById("registerForm");
  var regButton = document.getElementById("registerButton");
  if(logForm.classList.contains("dontshow")){
    logForm.classList.remove("dontshow");
  }
  regForm.classList.add("dontshow");
  logButton.classList.add("dontshow");
  // logForm.classList.add("show");
  regButton.classList.add("dontshow");

}
function openRegister(){
  var logButton = document.getElementById("loginButton");
  var regForm = document.getElementById("registerForm");
  var regButton = document.getElementById("registerButton");
  var logForm = document.getElementById("loginForm");
  if(regForm.classList.contains("dontshow")){
    regForm.classList.remove("dontshow");
  }
  logButton.classList.add("dontshow");
  logForm.classList.add("dontshow");
  // regForm.classList.add("show");
  regButton.classList.add("dontshow");
}