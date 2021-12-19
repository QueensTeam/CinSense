const gallery = document.querySelector('#gallery');
const loader = document.querySelector('#loader');
const movies = document.querySelector('.photogallery');
let currentPage = 1;
let totalMovies = 0;
let currentUrl = "/getAll/";
let defaultUserState = "offline";


$(document).ready(function () {
  if (document.contains(gallery)) loadMovies(currentPage, currentUrl);
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


window.addEventListener('scroll', () => {
  const {
      scrollTop,
      scrollHeight,
      clientHeight
  } = document.documentElement;
  if (scrollTop + clientHeight >= scrollHeight && currentPage <= 500) {
      currentPage++;
      loadMovies(currentPage, currentUrl);
      console.log(currentPage);
  }
}, {
  passive: true
});

const hasMoreMovies = (page, total) => {
  return total === 0 || ((page - 1) * 20 + 1) < total;
};

const addMovies = (movies) => {
  var noMoviesHeader = document.getElementById("noMoviesHeader");
  mv = JSON.parse(movies);
  mv.forEach(addMovie);
  if (mv.length === 0){
    if(noMoviesHeader.classList.contains("dontshow")){
        noMoviesHeader.classList.remove("dontshow");
       }
  }
};

function searchForMovies(){
  var genre = document.getElementById("genre").value;
  var decade = document.getElementById("decade").value;
  var voteavg = document.getElementById("average").value;
  var votecnt = document.getElementById("votecount").value;
  // var noMoviesHeader = document.getElementById("noMoviesHeader");
  console.log(genre + " " + decade + " " + voteavg + " " + votecnt);
  url = "/getAll/";
  document.getElementById("gallery").innerHTML = "";
  if (genre != "") url+= genre + "a";
  if (decade != "") url+= decade + "a";
  if (voteavg != "") url+= voteavg + "a";
  if (votecnt != "") url += votecnt + "a";
  url += "/"
  console.log(currentPage);
  console.log(url);
  currentUrl = url;
  // if (!url){
  //    if(noMoviesHeader.classList.contains("dontshow")){
  //       noMoviesHeader.classList.remove("dontshow");
  //      }
  // }
  loadMovies(currentPage, url);
}

function addMovie(value){
  if (value.hasOwnProperty('poster_path')) {
    if (value.hasOwnProperty('release_date')) release_year = value.release_date.substring(0, 4);
    else release_year = "-";
    movie = "<img id =\" "+ value.id + "\" src=\"https://image.tmdb.org/t/p/w600_and_h900_bestv2/" + value.poster_path.substring(1) + "\" onClick=\"openMovie(" + value.id + ")\" alt=\"" + value.title + " (" +  release_year+ ")" + "\" title=\"" + value.title + "\" class=\"col-5 col-sm-3 col-md-3 col-lg-2  mov\"/>";
    $("#gallery").append(movie);
  }
}
const loadMovies = async (page, url) => {
  try { 
    
    console.log(url);
    const response = await $.get(url + page);
    console.log(response);
    addMovies(response);
    totalMovies = response.totalMovies;
  } 
  catch (error) {
    console.log(error.message);
  } finally {}
};


const openMovie = async (value) => {
  try {
    response = await $.get("/movie/" + value);
    imdb = await $.get("/imdb/" + value);
    genres = response.genres;
    genre = "";
    var i;
    for (i = 0; i < genres.length; i++) {
      genre += genres[i].name;
      if (i != genres.length - 1) genre += ", ";
    }
    activeMovie = " <div class=\"activeContainer col-11 col-lg-6\"><a href=\"\" onclick=\"closeActiveWindow()\"><i class=\"fas fa-times\"></i></a><span onclick=\"transitionToPage('" + imdb + "')\"><img  src=\"https://image.tmdb.org/t/p/w600_and_h900_bestv2/" + response.poster_path.substring(1) + "\" alt=\"\" title=\" " + response.title + "\" class=\"col-5 col-sm-5 col-lg-5 mov\"/></span><span class=\"movieInfo\"><p id=\"movieYourVote\"><div class=\"star-rating\"><input type=\"radio\" id=\"10-stars\" name=\"rating\" value=\"10\" /><label for=\"10-stars\" class=\"star\">&#9733;</label><input type=\"radio\" id=\"9-stars\" name=\"rating\" value=\"9\" /><label for=\"9-stars\" class=\"star\">&#9733;</label><input type=\"radio\" id=\"8-stars\" name=\"rating\" value=\"8\" /><label for=\"8-stars\" class=\"star\">&#9733;</label><input type=\"radio\" id=\"7-stars\" name=\"rating\" value=\"7\" /><label for=\"7-stars\" class=\"star\">&#9733;</label><input type=\"radio\" id=\"6-star\" name=\"rating\" value=\"6\" /><label for=\"6-star\" class=\"star\">&#9733;</label><input type=\"radio\" id=\"5-stars\" name=\"rating\" value=\"5\" /><label for=\"5-stars\" class=\"star\">&#9733;</label><input type=\"radio\" id=\"4-stars\" name=\"rating\" value=\"4\" /><label for=\"4-stars\" class=\"star\">&#9733;</label><input type=\"radio\" id=\"3-stars\" name=\"rating\" value=\"3\" /><label for=\"3-stars\" class=\"star\">&#9733;</label><input type=\"radio\" id=\"2-stars\" name=\"rating\" value=\"2\" /><label for=\"2-stars\" class=\"star\">&#9733;</label><input type=\"radio\" id=\"1-star\" name=\"rating\" value=\"1\" /><label for=\"1-star\" class=\"star\">&#9733;</label></div></p><div><p id=\"movieTitle\">" + response.title + "</p><p id=\"movieYear\">" + response.release_date.substring(0, 4) + "</p></div><div><p id=\"uncheckedWatchlist\" onclick=\"checkWatchlist()\"><i class=\"far fa-clock\"></i></p><p id=\"checkedWatchlist\" onclick=\"uncheckWatchlist()\" class=\"dontshow\"><i class=\"fas fa-clock\"></i></p><p id=\"uncheckedSeen\" onclick=\"checkSeen()\"><i class=\"far fa-check-circle\"></i></p><p id=\"checkedSeen\" onclick=\"uncheckSeen()\" class=\"dontshow\"><i class=\"fas fa-check-circle\"></i></p></div><p id=\"movieGenre\">" + genre + "</p><p id=\"movieSummary\">" + response.overview + "</p><div id=\"tmdbInfo\"><img src=\"https://play-lh.googleusercontent.com/bBT7rPEvIr2tvzaXcoIdxeeFd8GNUbpWVl94tmiWOwrzwbjMwzDwyhNvAIl5t37u0c8\" width='50px' alt=\"TMDB logo\"/><p id=\"movieVoteAverage\" alt=\"Average movie rating\">" + response.vote_average + "</p><p id=\"movieVoteCount\" alt=\"Movie rating count\">" + response.vote_count +" votes</p></div></span></div>";
    $("#activeMovie").append(activeMovie);
  }
  catch (error) { console.log(error.message); } 
  finally {}
};

function closeActiveWindow(){
  $("#activeMovie").innerHTML=``;
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

const randomovie = async() => {
   try {

     response = await $.get("http://127.0.0.1:5000/randomovie");
     console.log(response);
     var recom = document.getElementById("recommendation");
     recom.innerHTML = ``;
     imdb = await $.get("/imdb/" + response.id);
     if (response.hasOwnProperty('release_date')) release_year = response.release_date.substring(0, 4);
    else release_year = "-";
    $("#recommendation").append( `<div onclick="transitionToPage('` + imdb + `')"> <p class="ltitle">` + response.title + ` (` + release_year + `)</p>
     <img src="https://image.tmdb.org/t/p/w600_and_h900_bestv2` + response.poster_path + `" alt="" title="` + response.title + ` (` + response.release_year + `)" class="col-12  col-lg-5 lpic"/></div>`);
   }
   catch (error) {console.log(error);}
   finally{}
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
  regButton.classList.add("dontshow");
}

function checkWatchlist(){
  var checkButton = document.getElementById("checkedWatchlist");
  var uncheckButton = document.getElementById("uncheckedWatchlist");
  if(checkButton.classList.contains("dontshow")){
    checkButton.classList.remove("dontshow");
  }
  uncheckButton.classList.add("dontshow");
}

function uncheckWatchlist(){
  var checkButton = document.getElementById("checkedWatchlist");
  var uncheckButton = document.getElementById("uncheckedWatchlist");
  if(uncheckButton.classList.contains("dontshow")){
    uncheckButton.classList.remove("dontshow");
  }
  checkButton.classList.add("dontshow");
}
function checkSeen(){
  var checkButton = document.getElementById("checkedSeen");
  var uncheckButton = document.getElementById("uncheckedSeen");
  if(checkButton.classList.contains("dontshow")){
    checkButton.classList.remove("dontshow");
  }
  uncheckButton.classList.add("dontshow");
}

function uncheckSeen(){
  var checkButton = document.getElementById("checkedSeen");
  var uncheckButton = document.getElementById("uncheckedSeen");
  if(uncheckButton.classList.contains("dontshow")){
    uncheckButton.classList.remove("dontshow");
  }
  checkButton.classList.add("dontshow");
}

function showTheFooter(){
  var foot1 = document.getElementById("footerInfo1");
  var foot2 = document.getElementById("footerInfo2");
  var cred = document.getElementById("creatorNames");
  if(foot2.classList.contains("dontshow")){
    foot2.classList.remove("dontshow");
    cred.classList.remove("dontshow");
    foot1.classList.add("dontshow");
  } else if (foot1.classList.contains("dontshow")){
    foot1.classList.remove("dontshow");
    foot2.classList.add("dontshow");
    cred.classList.add("dontshow");
  }
}

function changeUserState(){
  var onlineState = document.getElementById("userStateOnline");
  var offlineState = document.getElementById("userStateOffline");

  var accountOnline = document.getElementById("onlineUser");
  var accountOffline = document.getElementById("offlineUser");
  if(onlineState.classList.contains("dontshow")){
    onlineState.classList.remove("dontshow");
    accountOnline.classList.remove("dontshow");
    offlineState.classList.add("dontshow");
    accountOffline.classList.add("dontshow");
  } else if (offlineState.classList.contains("dontshow")){
    onlineState.classList.add("dontshow");
    accountOnline.classList.add("dontshow");
    offlineState.classList.remove("dontshow");
    accountOffline.classList.remove("dontshow");
  } 
}