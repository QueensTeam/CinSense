$(document).ready(function () {

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