// ── NAVIGATION ──────────────────────────────────
function toggleNav(){
  document.getElementById("navLinks").classList.toggle("open");
  var act=document.getElementById("navActions");if(act)act.classList.toggle("open");
}
document.addEventListener("click",function(e){
  if(!e.target.closest(".nb")){
    var nl=document.getElementById("navLinks");var na=document.getElementById("navActions");
    if(nl)nl.classList.remove("open");if(na)na.classList.remove("open");
  }
});

// ── SLIDER ──────────────────────────────────────
function initSlider(id){
  var wrap=document.getElementById(id);if(!wrap)return;
  var track=wrap.querySelector(".s-track");
  var slides=wrap.querySelectorAll(".s-slide");
  var dots=wrap.querySelectorAll(".s-dot");
  var cur=0,timer,startX=0;
  function go(n){
    cur=(n+slides.length)%slides.length;
    track.style.transform="translateX(-"+cur*100+"%)";
    dots.forEach(function(d,i){d.classList.toggle("active",i===cur)});
  }
  function next(){go(cur+1)}
  function prev(){go(cur-1)}
  function auto(){clearInterval(timer);timer=setInterval(next,4500)}
  dots.forEach(function(d,i){d.addEventListener("click",function(){clearInterval(timer);go(i);auto();});});
  var nb=wrap.querySelector(".s-btn.next");var pb=wrap.querySelector(".s-btn.prev");
  if(nb)nb.addEventListener("click",function(){clearInterval(timer);next();auto();});
  if(pb)pb.addEventListener("click",function(){clearInterval(timer);prev();auto();});
  wrap.addEventListener("mouseenter",function(){clearInterval(timer)});
  wrap.addEventListener("mouseleave",auto);
  track.addEventListener("touchstart",function(e){startX=e.touches[0].clientX},{passive:true});
  track.addEventListener("touchend",function(e){
    var dx=e.changedTouches[0].clientX-startX;
    if(Math.abs(dx)>40){clearInterval(timer);dx>0?prev():next();auto();}
  },{passive:true});
  go(0);auto();
}

// ── MODAL ────────────────────────────────────────
function openModal(id){
  var m=document.getElementById(id);if(m){m.classList.add("open");document.body.style.overflow="hidden";}
}
function closeModal(id){
  var m=document.getElementById(id);if(m){m.classList.remove("open");document.body.style.overflow="";}
}
document.addEventListener("keydown",function(e){if(e.key==="Escape"){document.querySelectorAll(".mo.open").forEach(function(m){m.classList.remove("open");document.body.style.overflow="";})}});
document.addEventListener("click",function(e){if(e.target.classList.contains("mo")){e.target.classList.remove("open");document.body.style.overflow="";}});

// ── TOAST ────────────────────────────────────────
function toast(msg,type){
  type=type||"ok";
  var t=document.createElement("div");
  t.style.cssText="position:fixed;top:80px;right:20px;z-index:9999;padding:13px 20px;border-radius:12px;font-size:14px;font-weight:600;box-shadow:0 4px 20px rgba(0,0,0,.15);animation:fadein .25s;max-width:360px;line-height:1.5;display:flex;align-items:center;gap:10px";
  var styles={ok:"background:#16A34A;color:#fff",er:"background:#EF4444;color:#fff",wa:"background:#FFFBEB;color:#92400E;border:1px solid #FDE68A",in:"background:#EFF6FF;color:#1D4ED8;border:1px solid #BFDBFE"};
  t.style.cssText+=";"+styles[type];
  var icons={ok:"✓",er:"✕",wa:"⚠",in:"ℹ"};
  t.innerHTML="<span style='font-size:16px'>"+icons[type]+"</span><span>"+msg+"</span>";
  document.body.appendChild(t);
  setTimeout(function(){t.style.opacity="0";t.style.transform="translateY(-10px)";t.style.transition="all .3s";setTimeout(function(){t.remove()},300)},3500);
}

// ── FILTER / SEARCH ──────────────────────────────
function filterTable(inputId,tableId){
  var input=document.getElementById(inputId);var table=document.getElementById(tableId);
  if(!input||!table)return;
  input.addEventListener("input",function(){
    var v=this.value.toLowerCase();
    table.querySelectorAll("tbody tr").forEach(function(row){
      row.style.display=row.textContent.toLowerCase().includes(v)?"":"none";
    });
  });
}
function filterCards(inputId,containerClass){
  var input=document.getElementById(inputId);
  if(!input)return;
  input.addEventListener("input",function(){
    var v=this.value.toLowerCase();
    document.querySelectorAll("."+containerClass).forEach(function(card){
      card.style.display=card.textContent.toLowerCase().includes(v)?"":"none";
    });
  });
}

// ── CEK GEJALA MANDIRI (TRIAGE) ─────────────────
function selectGejala(id, el){
  document.querySelectorAll(".gejala-btn").forEach(function(b){b.classList.remove("active")});
  el.classList.add("active");
  document.querySelectorAll(".gejala-res").forEach(function(r){r.classList.remove("show")});
  var target=document.getElementById("res-"+id);
  if(target){target.classList.add("show");}
}

// ── JADWAL SLOT SELECT ─────────────────────────
function selectSlot(el){
  document.querySelectorAll(".slot").forEach(function(s){s.classList.remove("sel")});
  el.classList.add("sel");
  var inp=document.getElementById("jadwal_id");
  if(inp)inp.value=el.getAttribute("data-id");
}

// ── PAYMENT SIMULATION ─────────────────────────
function simulatePayment(method){
  var overlay=document.getElementById("payOverlay");
  if(overlay){overlay.style.display="flex";}
  setTimeout(function(){
    if(overlay)overlay.style.display="none";
    var st=document.getElementById("payStatus");
    if(st){
      st.innerHTML='<div class="alert al-ok" style="font-size:15px;padding:16px"><strong>✓ Pembayaran Berhasil!</strong><br>Booking Anda telah dikonfirmasi via '+method+'. Link Jitsi Meet dan invoice resmi telah dikirim ke WhatsApp Anda.</div>';
      st.style.display="block";
      st.scrollIntoView({behavior:"smooth"});
    }
    toast("Pembayaran via "+method+" sukses!","ok");
  },2200);
}

// ── ADMIN STATUS UPDATE ─────────────────────────
function updateStatus(selectEl){
  var row=selectEl.closest("tr");
  var cell=row?row.querySelector(".status-cell"):null;
  if(!cell)return;
  var map={"pending":"sts-p","confirmed":"sts-c","completed":"sts-d","cancelled":"sts-x","scheduled":"sts-c","selesai":"sts-d"};
  var labels={"pending":"Pending","confirmed":"Confirmed","completed":"Selesai","cancelled":"Dibatalkan","scheduled":"Scheduled","selesai":"Selesai"};
  var v=selectEl.value;
  cell.innerHTML='<span class="sts '+(map[v]||"sts-s")+'">'+(labels[v]||v)+'</span>';
  toast("Status berhasil diperbarui","ok");
}

// ── ADMIN CONFIRM BOOKING ──────────────────────
function confirmBooking(btn, link){
  var row=btn.closest("tr");
  if(row){
    var cell=row.querySelector(".status-cell");
    if(cell)cell.innerHTML='<span class="sts sts-c">Confirmed</span>';
    var act=row.querySelector(".action-cell");
    if(act)act.innerHTML='<a href="'+link+'" target="_blank" class="btn btn-g btn-sm">Buka Jitsi</a>';
  }
  toast("Booking dikonfirmasi! Notifikasi dikirim ke user via WhatsApp.","ok");
}

// ── COPY TO CLIPBOARD ──────────────────────────
function copyText(text){
  if(navigator.clipboard){
    navigator.clipboard.writeText(text).then(function(){toast("Link disalin!","ok")});
  }else{
    toast("Salin: "+text,"in");
  }
}

// ── INIT ───────────────────────────────────────
document.addEventListener("DOMContentLoaded",function(){
  filterTable("searchInput","mainTable");
  filterCards("searchCards","filterable-card");
});
