import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Zombie Wave", page_icon="🧟", layout="wide")

HTML = r"""
<!DOCTYPE html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
html,body{margin:0;background:#1b1230}
canvas{display:block;width:100%;max-width:960px;margin:0 auto;touch-action:none;border-radius:10px}
</style></head><body>
<canvas id="c"></canvas>
<script>
const W=960,H=540,G=470,HX=240;
const c=document.getElementById('c'),X=c.getContext('2d');c.width=W;c.height=H;
const SK=[
 {n:'Zombie xanh',c:'#7cc242',d:'#4f8a1f',hat:0,cost:0},
 {n:'Mũ lưỡi trai',c:'#58c4a8',d:'#2f8f78',hat:1,cost:40},
 {n:'Cao bồi',c:'#a3d14b',d:'#6b8f1f',hat:2,cost:80},
 {n:'Vua zombie',c:'#b48be0',d:'#7a4fb0',hat:3,cost:120}];
const MS=[{t:'Ăn 30 con người',g:30},{t:'Chạy tổng cộng 2000 m',g:2000},{t:'Nhặt 50 xu',g:50}];
let S={coins:0,best:0,owned:[1,0,0,0],skin:0,m:[0,0,0],md:[0,0,0]};
try{Object.assign(S,JSON.parse(localStorage.getItem('zw')||'{}'))}catch(e){}
const save=()=>{try{localStorage.setItem('zw',JSON.stringify(S))}catch(e){}};
let st='menu',R=null,btns=[],T=0,SC=0,note='';

/* ---------- nền thành phố ---------- */
const L=[[],[]],TOT=[0,0];
for(let l=0;l<2;l++){let a=0;while(a<1500){const w=60+Math.random()*80,h=(l?110:190)+Math.random()*(l?120:170);L[l].push({x:a,w,h});a+=w+8}TOT[l]=a}
function bg(sp){
 SC+=sp;
 const g=X.createLinearGradient(0,0,0,G);g.addColorStop(0,'#5b3a8c');g.addColorStop(.55,'#f0707a');g.addColorStop(1,'#ffc78a');
 X.fillStyle=g;X.fillRect(0,0,W,H);
 X.fillStyle='#ffe9b0';X.beginPath();X.arc(740,300,70,0,7);X.fill();
 for(let l=0;l<2;l++){
  const f=l?.5:.2,off=(SC*f)%TOT[l];
  X.fillStyle=l?'#3d2b5c':'#6a4a86';
  for(const b of L[l])for(const k of [0,TOT[l]]){
   const bx=b.x-off+k;if(bx>W||bx+b.w<0)continue;
   X.fillRect(bx,G-b.h,b.w,b.h);
   if(l){X.fillStyle='#ffd27a';for(let wy=G-b.h+14;wy<G-20;wy+=26)for(let wx=bx+8;wx<bx+b.w-10;wx+=18)if((wx*7+wy*3|0)%5<2)X.fillRect(wx,wy,7,10);X.fillStyle='#3d2b5c'}
  }}
 X.fillStyle='#4a4f5e';X.fillRect(0,G,W,H-G);
 X.fillStyle='#8b90a0';X.fillRect(0,G,W,8);
 X.fillStyle='#f2c94c';const o=(SC)%80;
 for(let i=-1;i<13;i++)X.fillRect(i*80-o,G+44,44,6);
}

/* ---------- vẽ nhân vật ---------- */
function hat(px,py,k){
 if(k===1){X.fillStyle='#2f6fd6';X.beginPath();X.arc(px+2,py,12,Math.PI,0);X.fill();X.fillRect(px+4,py-2,16,4);X.fillStyle='#fff';X.beginPath();X.arc(px+2,py-6,3,0,7);X.fill()}
 if(k===2){X.fillStyle='#b8894a';X.beginPath();X.ellipse(px+2,py+1,22,5,0,0,7);X.fill();X.fillRect(px-7,py-14,18,14)}
 if(k===3){X.fillStyle='#f4c430';X.beginPath();X.moveTo(px-10,py+2);X.lineTo(px-10,py-12);X.lineTo(px-4,py-5);X.lineTo(px+2,py-14);X.lineTo(px+8,py-5);X.lineTo(px+14,py-12);X.lineTo(px+14,py+2);X.fill()}
}
function Z(px,py,ph,h,sk){
 const k=SK[sk],s=Math.sin(ph)*8;X.lineCap='round';
 X.strokeStyle=k.d;X.lineWidth=5;X.beginPath();X.moveTo(px-3,py-14);X.lineTo(px-3+s,py);X.moveTo(px+3,py-14);X.lineTo(px+3-s,py);X.stroke();
 X.fillStyle='#34495e';X.beginPath();X.ellipse(px,py-24,10,13,0,0,7);X.fill();
 X.strokeStyle=k.c;X.lineWidth=4;X.beginPath();X.moveTo(px+4,py-28);X.lineTo(px+21,py-30+s/2);X.moveTo(px+2,py-25);X.lineTo(px+18,py-23-s/2);X.stroke();
 X.fillStyle=k.c;X.beginPath();X.arc(px+2,py-43,13,0,7);X.fill();
 X.fillStyle='#fff';X.beginPath();X.arc(px+8,py-45,6.5,0,7);X.fill();
 X.fillStyle='#222';X.beginPath();X.arc(px+10,py-45,2.8,0,7);X.fill();
 X.fillStyle='#2a5d12';X.fillRect(px+4,py-37,10,2.5);
 if(h)hat(px,py-54,h);
}
function Hm(o){
 const px=o.x+13,py=G,s=Math.sin(T*.35+o.x)*7;X.lineCap='round';
 X.strokeStyle='#333';X.lineWidth=5;X.beginPath();X.moveTo(px-3,py-18);X.lineTo(px-3+s,py);X.moveTo(px+3,py-18);X.lineTo(px+3-s,py);X.stroke();
 X.fillStyle=o.col;X.fillRect(px-8,py-40,16,24);
 X.strokeStyle=o.sk;X.lineWidth=4;X.beginPath();X.moveTo(px-8,py-36);X.lineTo(px-14,py-52);X.moveTo(px+8,py-36);X.lineTo(px+14,py-52);X.stroke();
 X.fillStyle=o.sk;X.beginPath();X.arc(px,py-48,10,0,7);X.fill();
 X.fillStyle='#222';X.beginPath();X.arc(px-3,py-50,1.8,0,7);X.arc(px+4,py-50,1.8,0,7);X.fill();
 X.beginPath();X.ellipse(px+1,py-43,3,4,0,0,7);X.fill();
}
function Car(o){
 const y=G-o.h;X.fillStyle=o.col;X.beginPath();X.roundRect(o.x,y+14,o.w,o.h-24,8);X.fill();
 X.beginPath();X.roundRect(o.x+22,y,o.w-50,24,8);X.fill();
 X.fillStyle='#bfe6ff';X.fillRect(o.x+30,y+5,18,14);X.fillRect(o.x+54,y+5,18,14);
 X.fillStyle='#222';for(const wx of [24,o.w-24]){X.beginPath();X.arc(o.x+wx,G-9,11,0,7);X.fill()}
 X.fillStyle='#999';for(const wx of [24,o.w-24]){X.beginPath();X.arc(o.x+wx,G-9,4,0,7);X.fill()}
}

/* ---------- giao diện ---------- */
function tx(t,x,y,sz,col,al,ol){
 X.font=`bold ${sz}px Impact,'Trebuchet MS',sans-serif`;X.textAlign=al||'left';
 if(ol){X.lineWidth=sz/6;X.strokeStyle=ol;X.lineJoin='round';X.strokeText(t,x,y)}
 X.fillStyle=col;X.fillText(t,x,y);
}
function B(t,x,y,w,h,col,f,sz){
 btns.push({x,y,w,h,f});
 X.fillStyle='#2b1233';X.beginPath();X.roundRect(x,y+5,w,h,14);X.fill();
 X.fillStyle=col;X.beginPath();X.roundRect(x,y,w,h,14);X.fill();
 tx(t,x+w/2,y+h/2+(sz||26)/3,sz||26,'#fff','center','#2b1233');
}
function panel(x,y,w,h){X.fillStyle='rgba(30,15,50,.78)';X.beginPath();X.roundRect(x,y,w,h,16);X.fill()}

function menu(){
 bg(3);
 for(let i=0;i<8;i++)Z(110+i*34-(i%2)*8,G+(i%2)*6,T*.3+i,i===7?SK[S.skin].hat:0,S.skin);
 tx('ZOMBIE',W/2,120,92,'#8ee03a','center','#1f3b0a');
 tx('WAVE',W/2,205,92,'#ff9a2e','center','#4a1d00');
 B('CHƠI',650,250,250,90,'#f2761c',newRun,46);
 B('NHIỆM VỤ',650,360,250,60,'#d94a8c',()=>st='missions',28);
 B('CỬA HÀNG',650,435,250,60,'#3a8fd9',()=>st='shop',28);
 panel(20,20,250,60);
 tx('Xu: '+S.coins,40,58,26,'#ffd23f','left');
 tx('Kỷ lục: '+S.best,40,76,14,'#fff','left');
}
function missions(){
 bg(1);panel(110,40,740,450);
 tx('NHIỆM VỤ',W/2,100,44,'#ffd23f','center');
 MS.forEach((m,i)=>{
  const y=140+i*95,p=Math.min(1,S.m[i]/m.g);
  tx(m.t+(S.md[i]?'  (+25 xu)':''),150,y+20,24,'#fff','left');
  X.fillStyle='#43305e';X.beginPath();X.roundRect(150,y+34,660,24,12);X.fill();
  X.fillStyle=S.md[i]?'#7cc242':'#f2761c';X.beginPath();X.roundRect(150,y+34,Math.max(24,660*p),24,12);X.fill();
  tx(Math.min(S.m[i],m.g)+' / '+m.g,480,y+53,16,'#fff','center');
 });
 B('QUAY LẠI',380,420,200,56,'#d94a8c',()=>st='menu',24);
}
function shop(){
 bg(1);panel(30,30,900,480);
 tx('CỬA HÀNG',W/2,85,44,'#ffd23f','center');
 tx('Xu: '+S.coins,900,85,24,'#ffd23f','right');
 SK.forEach((k,i)=>{
  const x=55+i*220,y=115;
  X.fillStyle='#43305e';X.beginPath();X.roundRect(x,y,200,290,14);X.fill();
  X.save();X.translate(x+88,y+170);X.scale(2.1,2.1);Z(0,0,T*.25,k.hat,i);X.restore();
  tx(k.n,x+100,y+215,20,'#fff','center');
  const own=S.owned[i],on=S.skin===i;
  B(on?'ĐANG DÙNG':own?'DÙNG':'MUA '+k.cost,x+20,y+232,160,44,on?'#7cc242':own?'#3a8fd9':'#f2761c',()=>{
   if(own)S.skin=i;else if(S.coins>=k.cost){S.coins-=k.cost;S.owned[i]=1;S.skin=i}
   save();},20);
 });
 B('QUAY LẠI',380,430,200,56,'#d94a8c',()=>st='menu',24);
}

/* ---------- vòng chơi ---------- */
function newRun(){
 R={n:3,dist:0,hy:0,vy:0,j:0,hist:new Array(120).fill(0),o:[],gap:350,eat:0,coin:0,shake:0,p:[],sp:6};
 st='play';
}
function jump(){if(R.j<2){R.vy=14.5;R.j++}}
function splat(x,y,col){for(let i=0;i<10;i++)R.p.push({x,y,vx:(Math.random()-.5)*8,vy:-Math.random()*7,l:35,c:col})}
function spawn(){
 const r=Math.random(),x0=W+60,pick=a=>a[Math.random()*a.length|0];
 if(r<.5){const k=1+(Math.random()*4|0);
  for(let i=0;i<k;i++)R.o.push({k:'h',x:x0+i*40,w:26,h:54,col:pick(['#e0523a','#3a7be0','#e0b13a','#9b59b6']),sk:pick(['#f2c9a0','#d9a273','#b87d4b'])})}
 else if(r<.78)R.o.push({k:'car',x:x0,w:110,h:50,col:pick(['#d94a4a','#4a8fd9','#e0c040'])});
 else for(let i=0;i<6;i++)R.o.push({k:'coin',x:x0+i*34,y:G-70-Math.sin(i/5*Math.PI)*70,w:18,h:18});
}
function over(){
 st='over';S.coins+=R.coin;
 const sc=Math.floor(R.dist)+R.eat*10;S.best=Math.max(S.best,sc);
 S.m[0]+=R.eat;S.m[1]+=Math.floor(R.dist);S.m[2]+=R.coin;
 MS.forEach((m,i)=>{if(!S.md[i]&&S.m[i]>=m.g){S.md[i]=1;S.coins+=25}});
 save();
}
function step(){
 T++;if(st!=='play')return;
 R.sp=6+Math.min(R.dist/900,4);R.dist+=R.sp/10;
 R.hy+=R.vy;R.vy-=.75;if(R.hy<=0){R.hy=0;R.vy=0;R.j=0}
 R.hist.unshift(R.hy);R.hist.pop();
 R.gap-=R.sp;if(R.gap<=0){spawn();R.gap=260+Math.random()*320}
 for(const o of R.o){
  o.x-=R.sp;if(o.k==='h')o.x+=1.6;
  if(o.dead)continue;
  if(o.k==='h'&&o.x>HX-130&&o.x<HX+34&&R.hy<60){o.dead=1;R.n++;R.eat++;splat(o.x,G-30,'#7cc242')}
  else if(o.k==='car'&&o.x<HX+34&&o.x+o.w>HX-30&&R.hy<50){o.dead=1;R.n=Math.max(0,R.n-5);R.shake=14;splat(o.x,G-30,'#ddd');if(R.n<=0)over()}
  else if(o.k==='coin'&&o.x<HX+34&&o.x+o.w>HX-100&&Math.abs(o.y-(G-R.hy-30))<55){o.dead=1;R.coin++}
 }
 R.o=R.o.filter(o=>!o.dead&&o.x>-160);
 for(const p of R.p){p.x+=p.vx;p.y+=p.vy;p.vy+=.5;p.l--}
 R.p=R.p.filter(p=>p.l>0);
 if(R.shake>0)R.shake--;
}
function play(){
 X.save();if(R.shake>0)X.translate((Math.random()-.5)*R.shake,(Math.random()-.5)*R.shake);
 bg(st==='play'?R.sp:0);
 for(const o of R.o){
  if(o.k==='h')Hm(o);else if(o.k==='car')Car(o);
  else{X.fillStyle='#ffd23f';X.beginPath();X.arc(o.x+9,o.y,9,0,7);X.fill();X.strokeStyle='#c99a00';X.lineWidth=2;X.stroke()}
 }
 const sh=Math.min(R.n,48);
 for(let i=sh-1;i>=0;i--){
  const col=i/3|0,row=i%3,d=Math.min(i*2,119);
  Z(HX-col*20-row*7,G+row*5-(R.hist[d]||0),T*.35+i*.7,i===0?SK[S.skin].hat:0,S.skin);
 }
 for(const p of R.p){X.globalAlpha=p.l/35;X.fillStyle=p.c;X.beginPath();X.arc(p.x,p.y,4,0,7);X.fill()}
 X.globalAlpha=1;X.restore();
 panel(14,14,430,52);
 tx('Zombie: '+R.n,28,50,26,'#8ee03a','left');
 tx(Math.floor(R.dist)+' m',215,50,26,'#fff','left');
 tx('Xu: '+R.coin,330,50,26,'#ffd23f','left');
 if(R.n<3&&st==='play')tx('Nhảy qua xe! Ăn người để thêm zombie',W/2,110,22,'#fff','center','#000');
}
function overScr(){
 play();X.fillStyle='rgba(15,8,30,.6)';X.fillRect(0,0,W,H);
 panel(280,90,400,340);
 tx('ĐÃ BỊ DIỆT!',W/2,155,46,'#ff6b6b','center');
 tx('Quãng đường: '+Math.floor(R.dist)+' m',W/2,210,24,'#fff','center');
 tx('Đã ăn: '+R.eat+' người',W/2,245,24,'#fff','center');
 tx('Xu nhặt được: '+R.coin,W/2,280,24,'#ffd23f','center');
 tx('Điểm: '+(Math.floor(R.dist)+R.eat*10)+'   Kỷ lục: '+S.best,W/2,315,22,'#8ee03a','center');
 B('CHƠI LẠI',320,340,150,60,'#f2761c',newRun,24);
 B('MENU',490,340,150,60,'#3a8fd9',()=>st='menu',24);
}

/* ---------- điều khiển & vòng lặp ---------- */
c.addEventListener('pointerdown',e=>{
 const r=c.getBoundingClientRect(),x=(e.clientX-r.left)*W/r.width,y=(e.clientY-r.top)*H/r.height;
 if(st==='play'){jump();return}
 for(let i=btns.length-1;i>=0;i--){const b=btns[i];
  if(x>=b.x&&x<=b.x+b.w&&y>=b.y&&y<=b.y+b.h){b.f();return}}
});
addEventListener('keydown',e=>{
 if(e.code==='Space'||e.code==='ArrowUp'){e.preventDefault();if(st==='play')jump();else if(st==='menu'||st==='over')newRun()}
});
let last=performance.now(),acc=0;
function loop(t){
 acc+=Math.min(t-last,100);last=t;
 while(acc>=1000/60){step();acc-=1000/60}
 btns=[];
 ({menu,missions,shop,play,over:overScr})[st]();
 requestAnimationFrame(loop);
}
requestAnimationFrame(loop);
</script></body></html>
"""

components.html(HTML, height=620, scrolling=False)
