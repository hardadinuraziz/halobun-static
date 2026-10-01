function toggleNav(){
  var nl = document.getElementById("navLinks");
  var na = document.getElementById("navActions");
  if(nl) nl.classList.toggle("open");
  if(na) na.classList.toggle("open");
}

function initSlider(id){
  var wrap = document.getElementById(id);
  if(!wrap) return;
  var track = wrap.querySelector(".s-track");
  var slides = wrap.querySelectorAll(".s-slide");
  var dots = wrap.querySelectorAll(".s-dot");
  if(!track || !slides.length) return;
  var cur = 0, timer;
  function go(n){
    cur = (n + slides.length) % slides.length;
    track.style.transform = "translateX(-" + cur * 100 + "%)";
    dots.forEach(function(d, i){ d.classList.toggle("active", i === cur); });
  }
  function next(){ go(cur + 1); }
  function prev(){ go(cur - 1); }
  function auto(){ timer = setInterval(next, 4200); }
  dots.forEach(function(d, i){
    d.addEventListener("click", function(){ clearInterval(timer); go(i); auto(); });
  });
  var nb = wrap.querySelector(".s-btn.next");
  var pb = wrap.querySelector(".s-btn.prev");
  if(nb) nb.addEventListener("click", function(){ clearInterval(timer); next(); auto(); });
  if(pb) pb.addEventListener("click", function(){ clearInterval(timer); prev(); auto(); });
  wrap.addEventListener("mouseenter", function(){ clearInterval(timer); });
  wrap.addEventListener("mouseleave", auto);
  go(0);
  auto();
}

function openModal(id){
  var m = document.getElementById(id);
  if(m) m.classList.add("open");
}

function closeModal(id){
  var m = document.getElementById(id);
  if(m) m.classList.remove("open");
}

// Close modal on backdrop click or Escape key
document.addEventListener("click", function(e){
  if(e.target && e.target.classList.contains("mo")){
    e.target.classList.remove("open");
  }
});

document.addEventListener("keydown", function(e){
  if(e.key === "Escape"){
    document.querySelectorAll(".mo.open").forEach(function(m){ m.classList.remove("open"); });
  }
});

function toast(msg, type){
  var t = document.createElement("div");
  t.style.cssText = "position:fixed;top:80px;right:20px;z-index:9999;background:" +
    (type === "ok" ? "#16A34A" : "#EF4444") +
    ";color:#fff;padding:12px 20px;border-radius:10px;font-size:14px;font-weight:600;box-shadow:0 4px 20px rgba(0,0,0,.15);animation:fadein .25s";
  t.textContent = msg;
  document.body.appendChild(t);
  setTimeout(function(){
    t.style.opacity = "0";
    t.style.transition = "opacity .3s ease";
    setTimeout(function(){ t.remove(); }, 300);
  }, 2700);
}