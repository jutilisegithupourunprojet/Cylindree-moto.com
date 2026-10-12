# -*- coding: utf-8 -*-
"""
Outils interactifs : "Trouve ma moto" (quiz) et "Est-ce que je touche le sol ?".

Ce module ne contient que du texte statique (CSS et JavaScript) ; les pages et le
fichier de donnees sont construits dans 20_site.py. Tout est calcule dans le
navigateur : aucune donnee saisie ne quitte l'appareil.

Regle de la hauteur de selle, commune aux deux outils (a garder identique dans
les deux scripts) :
  entrejambe estime = 45 % de la taille (ou valeur saisie)
  portee            = entrejambe + 30 mm (semelle des bottes, affaissement)
  ecart             = portee - hauteur de selle constructeur
  >= 0 : pieds a plat | >= -40 : presque a plat | >= -90 : pointes | sinon : trop haute
"""

CSS_OUTILS = r"""
/* ---- outils : quiz et hauteur de selle ---- */
.outil{padding-block:2rem 3rem}
.outil h1{margin-bottom:.4rem}
.liste-simple{max-width:68ch;color:var(--doux);padding-left:1.2rem;display:grid;gap:.4rem}
.liste-simple a{color:var(--accent)}
.outil h2{margin-top:2.2rem}
.outil-note{font-size:.84rem;color:var(--doux);max-width:70ch;margin-top:1.6rem}
.tm{background:var(--carte);border:1px solid var(--trait);border-radius:10px;
  box-shadow:var(--ombre);padding:clamp(1rem,3vw,1.8rem);margin-top:1.4rem;max-width:860px}
.tm-prog{display:flex;align-items:center;gap:.8rem;margin-bottom:1.2rem;
  font-size:.8rem;text-transform:uppercase;letter-spacing:.1em;color:var(--doux)}
.tm-barre{flex:1;height:6px;background:var(--creux);border-radius:3px;overflow:hidden}
.tm-barre i{display:block;height:100%;background:var(--accent);border-radius:3px;
  transition:width .4s cubic-bezier(.2,.8,.2,1)}
.tm fieldset{border:0;margin:0;padding:0;min-width:0}
.tm legend{font-family:var(--police-titre);font-weight:600;font-size:clamp(1.4rem,3.6vw,1.9rem);
  line-height:1.15;padding:0;margin-bottom:.3rem;text-wrap:balance}
.tm legend:focus{outline:none}
.tm-aide{margin:0 0 1rem;color:var(--doux);font-size:.95rem}
.tm-opts{display:grid;gap:.6rem;grid-template-columns:repeat(auto-fit,minmax(min(100%,230px),1fr))}
.q-opt{position:relative;display:block;cursor:pointer}
.q-opt input{position:absolute;opacity:0;inset:0;width:100%;height:100%;margin:0;cursor:pointer}
.q-opt span{display:flex;flex-direction:column;gap:.15rem;height:100%;min-height:3.4rem;
  padding:.8rem 1rem;border:1.5px solid var(--trait-fort);border-radius:8px;
  background:var(--fond);transition:border-color .2s,background-color .2s,transform .2s}
.q-opt b{font-weight:650}
.q-opt small{color:var(--doux);font-size:.84rem}
.q-opt:hover span{border-color:var(--accent)}
.q-opt input:checked + span{border-color:var(--accent);background:var(--accent-clair)}
.q-opt input:focus-visible + span{outline:2px solid var(--accent);outline-offset:2px}
.tm-champs{display:grid;gap:1rem;grid-template-columns:repeat(auto-fit,minmax(min(100%,220px),1fr));
  align-items:end;margin-bottom:1rem}
.tm-champs .champ input{font-size:1.1rem;padding:.65rem .75rem}
.tm-case{display:flex;align-items:center;gap:.6rem;font-size:.95rem;cursor:pointer;padding:.4rem 0;min-height:44px}
.tm-case input{width:1.2rem;height:1.2rem;accent-color:var(--accent)}
.tm-nav{display:flex;flex-wrap:wrap;gap:.7rem;margin-top:1.3rem;align-items:center}
.q-btn{font:inherit;font-weight:650;cursor:pointer;border-radius:8px;padding:.7rem 1.3rem;
  min-height:44px;border:1.5px solid var(--accent);background:var(--accent);color:#fff;
  text-decoration:none;display:inline-flex;align-items:center;transition:background-color .2s,transform .2s}
.q-btn:hover{background:var(--cta-survol);transform:translateY(-1px)}
.q-btn:disabled{opacity:.45;cursor:not-allowed;transform:none}
.q-btn.second{background:transparent;color:var(--texte);border-color:var(--trait-fort)}
.q-btn.second:hover{border-color:var(--accent);color:var(--accent);background:transparent}
.tm-res h2{font-family:var(--police-titre);font-size:clamp(1.5rem,4vw,2rem);margin:0 0 .3rem}
.tm-notes{margin:.2rem 0 1rem;padding:0;list-style:none;display:grid;gap:.3rem;font-size:.9rem;color:var(--doux)}
.tm-notes li::before{content:"\2192";color:var(--accent);margin-right:.5rem}
.r-liste{display:grid;gap:1rem;margin:1rem 0 0;padding:0;list-style:none}
.r-carte{display:grid;grid-template-columns:minmax(0,170px) 1fr;gap:1rem;background:var(--fond);
  border:1px solid var(--trait);border-radius:10px;overflow:hidden;position:relative}
.r-carte:first-child{border-color:var(--accent);box-shadow:var(--ombre)}
.r-rang{position:absolute;top:.5rem;left:.5rem;z-index:1;font-family:var(--police-titre);
  background:var(--accent);color:#fff;border-radius:6px;padding:.05rem .55rem;font-weight:600}
.r-img{background:var(--creux);display:flex;align-items:center;justify-content:center;min-height:130px}
.r-img img{width:100%;height:100%;object-fit:cover}
.r-corps{padding:.9rem 1rem .9rem 0;display:flex;flex-direction:column;gap:.35rem;min-width:0}
.r-marque{font-size:.72rem;text-transform:uppercase;letter-spacing:.1em;color:var(--pale)}
.r-nom{font-family:var(--police-titre);font-size:1.35rem;font-weight:600;line-height:1.15;margin:0}
.r-nom a{text-decoration:none}
.r-nom a:hover{color:var(--accent)}
.r-specs{font-size:.88rem;color:var(--doux);margin:0}
.r-pourquoi{margin:.2rem 0 0;padding:0;list-style:none;display:flex;flex-wrap:wrap;gap:.35rem}
.r-pourquoi li{font-size:.78rem;padding:.15rem .55rem;border-radius:99px;background:var(--accent-clair);
  color:var(--texte)}
.r-pourquoi li.neutre{background:var(--creux);color:var(--doux)}
.r-autres{margin-top:1.6rem}
.r-autres h3{font-size:1rem;margin:0 0 .5rem;color:var(--doux);font-weight:600}
.r-autres ul{margin:0;padding:0;list-style:none;display:grid;gap:.4rem;
  grid-template-columns:repeat(auto-fill,minmax(min(100%,250px),1fr))}
.r-autres a{display:flex;justify-content:space-between;gap:.6rem;padding:.55rem .8rem;
  border:1px solid var(--trait);border-radius:8px;text-decoration:none;font-size:.9rem;
  background:var(--fond);min-height:44px;align-items:center}
.r-autres a:hover{border-color:var(--accent)}
.r-autres span{color:var(--pale);font-size:.8rem;white-space:nowrap}
.r-vide{padding:1rem;border:1px dashed var(--trait-fort);border-radius:8px;color:var(--doux)}
@media (max-width:560px){
  .r-carte{grid-template-columns:1fr}
  .r-img{min-height:150px;max-height:190px}
  .r-corps{padding:0 1rem 1rem}
}

.tm-affiner h2{font-family:var(--police-titre);font-size:clamp(1.5rem,4vw,2rem);margin:0 0 .3rem}
.tm-aff-groupe{margin:0 0 1.4rem}
.tm-aff-groupe legend{font-weight:650;font-size:1.05rem;margin-bottom:.5rem;padding:0}
.tm-opts.compact{grid-template-columns:repeat(auto-fit,minmax(min(100%,190px),1fr))}
.tm-opts.compact .q-opt span{min-height:3rem;padding:.6rem .85rem}
.tm-pref{margin:.1rem 0 .6rem;font-size:.9rem;color:var(--doux)}
.tm-compte{margin:.4rem 0 0;font-weight:650;color:var(--accent)}

/* hauteur de selle */
.sl{background:var(--carte);border:1px solid var(--trait);border-radius:10px;box-shadow:var(--ombre);
  padding:clamp(1rem,3vw,1.8rem);margin-top:1.4rem}
.sl-tete{display:grid;gap:1.2rem 2rem;grid-template-columns:minmax(0,1.2fr) minmax(0,1fr);align-items:end}
.sl-taille{display:flex;flex-direction:column;gap:.5rem}
.sl-taille label{font-size:.74rem;text-transform:uppercase;letter-spacing:.09em;color:var(--pale)}
.sl-val{font-family:var(--police-titre);font-size:clamp(2.2rem,6vw,3.2rem);font-weight:600;line-height:1;
  font-variant-numeric:tabular-nums}
.sl-val small{font-size:1rem;color:var(--doux);font-weight:500;margin-left:.3rem}
.sl input[type=range]{width:100%;accent-color:var(--accent);height:32px;margin:0}
.sl-opts{display:grid;gap:.8rem;grid-template-columns:1fr 1fr;align-items:end}
.sl-resume{margin:1.2rem 0 .4rem;font-size:1.02rem}
.sl-resume b{color:var(--accent)}
.sl-histo{display:flex;align-items:flex-end;gap:2px;height:110px;margin:1rem 0 .2rem;
  border-bottom:1px solid var(--trait-fort)}
.sl-histo i{flex:1;min-width:2px;border-radius:2px 2px 0 0;background:var(--trait-fort);
  transition:background-color .25s,height .3s}
.sl-histo i.z0{background:var(--vert)}
.sl-histo i.z1{background:#6aa07f}
.sl-histo i.z2{background:#d99a2b}
.sl-histo i.z3{background:var(--rouge)}
.sl-axe{display:flex;justify-content:space-between;font-size:.74rem;color:var(--pale);
  font-variant-numeric:tabular-nums;margin-bottom:.8rem}
.sl-legende{display:flex;flex-wrap:wrap;gap:.4rem 1.1rem;font-size:.82rem;color:var(--doux);margin:.2rem 0 1rem}
.sl-legende span::before{content:"";display:inline-block;width:.7rem;height:.7rem;border-radius:2px;
  margin-right:.4rem;vertical-align:-1px;background:var(--c)}
.sl-groupe{border-top:1px solid var(--trait);padding-top:.4rem}
.sl-groupe summary{cursor:pointer;display:flex;justify-content:space-between;align-items:center;
  gap:1rem;padding:.7rem 0;font-weight:650;min-height:44px;list-style:none}
.sl-groupe summary::-webkit-details-marker{display:none}
.sl-groupe summary::after{content:"+";font-size:1.3rem;color:var(--pale);margin-left:auto}
.sl-groupe[open] summary::after{content:"\2212"}
.sl-nb{font-family:var(--police-titre);font-weight:600;color:var(--accent);font-size:1.15rem}
.sl-pastille{width:.8rem;height:.8rem;border-radius:3px;background:var(--c);flex:none}
.sl-titre{display:flex;align-items:center;gap:.6rem}
.sl-grille{display:grid;gap:.4rem;margin:0 0 1rem;padding:0;list-style:none;
  grid-template-columns:repeat(auto-fill,minmax(min(100%,235px),1fr))}
.sl-grille a{display:flex;justify-content:space-between;gap:.6rem;align-items:center;
  padding:.5rem .8rem;border:1px solid var(--trait);border-radius:8px;text-decoration:none;
  background:var(--fond);font-size:.9rem;min-height:44px}
.sl-grille a:hover{border-color:var(--accent)}
.sl-grille em{font-style:normal;color:var(--doux);font-size:.8rem;white-space:nowrap;
  font-variant-numeric:tabular-nums}
.sl-vide{color:var(--pale);font-size:.9rem;margin:0 0 1rem}
@media (max-width:640px){.sl-tete{grid-template-columns:1fr}}

/* maillage des marques dans le pied de page */
.pied-marques{display:flex;flex-wrap:wrap;gap:.2rem 1.1rem;margin:.9rem 0 .4rem}
.pied-marques a{font-size:.88rem;color:var(--doux);text-decoration:none;padding-block:.4rem}
.pied-marques a:hover{color:var(--accent);text-decoration:underline}
.liste-detail{color:var(--doux);font-size:.88rem}

/* acces aux outils depuis l'accueil */
.outils-duo{display:grid;gap:1rem;grid-template-columns:repeat(auto-fit,minmax(min(100%,320px),1fr));
  margin-top:1.1rem}
.outil-carte{display:flex;flex-direction:column;gap:.4rem;padding:1.3rem 1.4rem;text-decoration:none;
  background:var(--petrole);color:#f3efe7;border-radius:10px;border:1px solid transparent;
  transition:transform .25s cubic-bezier(.2,.8,.2,1),border-color .25s}
.outil-carte:hover{transform:translateY(-2px);border-color:#ff7a33}
.outil-carte b{font-family:var(--police-titre);font-size:1.5rem;font-weight:600;line-height:1.1}
.outil-carte span{color:#cfe0de;font-size:.95rem}
.outil-carte em{font-style:normal;color:#ff9a5c;font-weight:650;margin-top:.3rem}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]) .outil-carte{background:#12302f}
}
@media (max-width:560px){
  .nav-principale{gap:0 1.1rem;justify-content:flex-start}
  .nav-principale a{padding-block:.6rem}
}
@media (prefers-reduced-motion:reduce){
  .tm-barre i,.sl-histo i,.q-opt span{transition:none}
}
"""


# ---------------------------------------------------------------- quiz
JS_TROUVE = r"""
(function(){
  var conteneur=document.getElementById('tm');
  if(!conteneur) return;

  var SRC=conteneur.getAttribute('data-src');
  var ETAPES=[
    {id:'permis',q:'Quel permis as-tu ?',aide:'Le permis A2 limite la puissance à 35 kW (47,6 ch).',
     opts:[['a2','Permis A2','35 kW maximum'],['a','Permis A','Pas de limite de puissance']]},
    {id:'usage',q:'Tu roules surtout où ?',aide:'Choisis ton usage principal.',
     opts:[['ville','En ville','Trajets quotidiens, petites distances'],
           ['balade','Sur route, en balade','Week-ends, départementales'],
           ['voyage','En voyage','Longues distances, parfois à deux'],
           ['chemin','Sur chemins','Pistes et sorties mixtes'],
           ['sport','En sportive','Pilotage vif, sorties dynamiques']]},
    {id:'taille',q:'Quelle est ta taille ?',custom:true,
     aide:'On l’utilise pour la hauteur de selle. Tu peux passer cette question.'},
    {id:'budget',q:'Ton budget pour une moto neuve ?',
     aide:'Prix catalogue indicatif en France. Les motos sans prix relevé restent proposées, signalées.',
     opts:[['6000','Jusqu’à 6 000 €'],['9000','Jusqu’à 9 000 €'],
           ['13000','Jusqu’à 13 000 €'],['0','Pas de limite']]},
    {id:'exp',q:'Ton niveau à moto ?',aide:'Il sert à pondérer le poids et la puissance.',
     opts:[['deb','Débutant','Moins de 2 ans de pratique'],['int','Intermédiaire','2 à 5 ans'],
           ['conf','Confirmé','Plus de 5 ans']]}
  ];
  var CAT_USAGE={
    ville:{1:['scooter','roadster'],.5:['custom','trail']},
    balade:{1:['roadster','custom','cafe racer'],.5:['trail','routiere','sportive']},
    voyage:{1:['routiere','trail'],.5:['custom','roadster']},
    chemin:{1:['trail','tout-terrain','supermotard'],.5:['enduro']},
    sport:{1:['sportive'],.5:['supermotard','roadster']}
  };
  var LIB_USAGE={ville:'la ville',balade:'la balade',voyage:'le voyage',chemin:'les chemins',sport:'la sportive'};
  var D=[],rep={},idx=0;

  function norm(s){return (s||'').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'');}
  function fmt(n){return String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g,' ');}
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){
    return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}

  /* hauteur de selle : meme regle que la page "touche le sol" */
  function ecart(m){
    if(!rep.taille||!m.s) return null;
    var entre=rep.entre?rep.entre*10:rep.taille*10*0.45;
    return entre+30-m.s;
  }
  function zone(ec){return ec>=0?0:ec>=-40?1:ec>=-90?2:3;}

  function poidsUsage(m){
    var c=norm(m.c),t=CAT_USAGE[rep.usage]||{},w=0;
    [1,.5].forEach(function(p){
      (t[p]||[]).forEach(function(k){if(c.indexOf(k)>-1) w=Math.max(w,p);});
    });
    return w;
  }

  /* percentiles poids/puissance et couple/poids, calcules au chargement */
  var PCT={};
  function pctDe(vals){
    var s=vals.slice().sort(function(a,b){return a-b;});
    return function(v){
      if(s.length<2) return .5;
      var i=0;while(i<s.length&&s[i]<v) i++;
      return Math.min(1,i/(s.length-1));
    };
  }
  function preparer(){
    var pp=[],pc=[];
    D.forEach(function(m){
      if(m.kg){m.pw=m.ch/m.kg;pp.push(m.pw);}
      if(m.kg&&m.cp){m.pc=m.cp/m.kg;pc.push(m.pc);}
    });
    PCT.pw=pctDe(pp);PCT.pc=pctDe(pc);
  }
  var ECOLES_OPT=['japonaise','italienne','allemande','britannique','chinoise'];
  var LIB_AR={mono:'monocylindre',twin:'bicylindre',vtwin:'V-twin',boxer:'flat-twin','3':'3 cylindres','4':'4 cylindres',v4:'V4'};
  function dansOrigine(m){
    if(!rep.orig) return true;
    if(rep.orig==='autre') return ECOLES_OPT.indexOf(m.e)<0;
    return m.e===rep.orig;
  }
  function ajouter(raisons,txt,neutre){
    for(var i=0;i<raisons.length;i++) if(raisons[i][0]===txt) return;
    raisons.push([txt,neutre?1:0]);
  }

  function classer(o){
    var out=[];
    D.forEach(function(m){
      if(rep.permis==='a2'&&m.a2!=='oui') return;
      var w=poidsUsage(m);
      if(w===0) return;
      if(o.orig&&!dansOrigine(m)) return;
      if(o.auto&&rep.auto==='souvent'&&(m.ch<30||(m.cc&&m.cc<300))) return;
      if(o.leger&&rep.leger==='oui'&&m.kg&&m.kg>200) return;
      var ec=ecart(m),sc=45*w,raisons=[];
      if(ec!==null){
        var z=zone(ec);
        if(o.sel&&z>0) return;
        if(z>1) return;
        sc+=z===0?15:10;
        raisons.push([z===0?'Pieds à plat pour toi':'Presque à plat pour toi',0]);
      }
      if(o.bud&&m.pz){
        if(m.pz>o.bud) return;
        sc+=15;
        raisons.push(['Dans ton budget',0]);
      }else if(o.bud&&!m.pz){
        raisons.push(['Prix non relevé',1]);
      }
      if(rep.permis==='a2') sc+=20*Math.min(m.ch,47.6)/47.6;
      if(rep.exp==='deb'){
        if(m.kg){sc+=m.kg<=170?12:m.kg<=200?8:m.kg<=230?3:0;
          if(m.kg<=200) ajouter(raisons,'Légère : '+fmt(m.kg)+' kg');}
        if(rep.permis==='a'){sc+=m.ch<=75?8:m.ch>120?-12:0;}
      }else if(rep.exp==='conf'){
        sc+=Math.min(m.ch,150)/150*8;
      }else if(rep.exp==='int'&&rep.permis==='a'){
        sc+=Math.min(m.ch,90)/90*8;
      }
      /* questions "Affiner" */
      if(rep.orig&&dansOrigine(m)) ajouter(raisons,rep.orig==='autre'?'Autre origine : '+(m.e||'')
        :'École '+rep.orig);
      if(rep.auto==='parfois'&&m.ch<20) sc-=15;
      if((rep.auto==='souvent'||rep.auto==='parfois')&&m.ch>=30){sc+=6;ajouter(raisons,'À l\u2019aise sur autoroute');}
      if(rep.leger==='oui'&&m.kg){
        sc+=m.kg<=160?15:m.kg<=185?11:m.kg<=210?6:0;
        if(m.kg<=185) ajouter(raisons,'Légère : '+fmt(m.kg)+' kg');
      }
      if(rep.car){
        var pw=m.pw!==undefined?PCT.pw(m.pw):null,pcc=m.pc!==undefined?PCT.pc(m.pc):null,ar=m.ar,
            lib=ar&&LIB_AR[ar]?' ('+LIB_AR[ar]+')':'';
        if(rep.car==='vif'){
          if(pw!==null) sc+=25*pw;
          if(ar==='3'||ar==='4'||ar==='v4') sc+=6;
          if((pw!==null&&pw>=.6)||ar==='3'||ar==='4'||ar==='v4') ajouter(raisons,'Moteur vif'+lib);
        }else if(rep.car==='docile'){
          if(pw!==null) sc+=25*(1-pw);
          if(ar==='mono'||ar==='twin'||ar==='boxer') sc+=6;
          if((pw!==null&&pw<=.45)||ar==='mono'||ar==='twin') ajouter(raisons,'Moteur docile'+lib);
        }else if(rep.car==='couple'){
          if(pcc!==null) sc+=25*pcc;
          if(ar==='vtwin'||ar==='boxer') sc+=6;
          if((pcc!==null&&pcc>=.6)||ar==='vtwin'||ar==='boxer') ajouter(raisons,'Du couple'+(m.cp?' : '+m.cp+' Nm':''));
        }
      }
      sc+=((m.pz?1:0)+(m.s?1:0)+(m.kg?1:0)+(m.co?1:0))*1.5;
      if(w===1) raisons.unshift(['Pensée pour '+LIB_USAGE[rep.usage],0]);
      if(m.a2==='oui'&&rep.permis==='a2') ajouter(raisons,'Compatible A2');
      out.push({m:m,sc:sc,r:raisons,ec:ec});
    });
    out.sort(function(a,b){return b.sc-a.sc||a.m.n.localeCompare(b.m.n);});
    return out;
  }

  function calculer(){
    var notes=[],budget=parseInt(rep.budget,10)||0,strict=!!(rep.taille&&rep.plat);
    var niveaux=[
      {sel:strict,orig:true,auto:true,leger:true,bud:budget},
      {sel:strict,orig:true,auto:false,leger:false,bud:budget},
      {sel:false,orig:true,auto:false,leger:false,bud:budget},
      {sel:false,orig:false,auto:false,leger:false,bud:budget},
      {sel:false,orig:false,auto:false,leger:false,bud:0}
    ];
    var liste=[],n=0;
    for(var i=0;i<niveaux.length;i++){
      liste=classer(niveaux[i]);n=i;
      if(liste.length>=3) break;
    }
    if(n>=1&&(rep.auto==='souvent'||rep.leger==='oui')) notes.push('Peu de motos répondent à tous tes critères (autoroute, légèreté) : ils comptent dans le classement mais n\u2019écartent plus de moto.');
    if(n>=2&&strict) notes.push('Peu de motos te laissent les pieds à plat : on a élargi aux motos où tu poses presque les pieds à plat.');
    if(n>=3&&rep.orig) notes.push('Peu de motos de cette origine correspondent : on a élargi à toutes les origines.');
    if(n>=4&&budget) notes.push('Peu de motos entrent dans ce budget parmi nos fiches : on a levé la limite de prix.');
    return {liste:liste,notes:notes};
  }

  function specs(m){
    var b=[];
    b.push(fmt(m.ch)+' ch');
    if(m.kg) b.push(fmt(m.kg)+' kg');
    if(m.s) b.push('selle '+fmt(m.s)+' mm');
    if(m.co) b.push(String(m.co).replace('.',',')+' L/100 km');
    b.push(m.pz?fmt(m.pz)+' €':'prix non relevé');
    return b.join(' · ');
  }

  function carte(x,rang){
    var m=x.m;
    var img=m.i?'<img src="'+esc(m.i)+'" alt="" loading="lazy" decoding="async">':'';
    var pq=x.r.slice(0,4).map(function(r){return '<li'+(r[1]?' class="neutre"':'')+'>'+esc(r[0])+'</li>';}).join('');
    return '<li class="r-carte"><span class="r-rang">'+rang+'</span>'
      +'<div class="r-img">'+img+'</div><div class="r-corps">'
      +'<span class="r-marque">'+esc(m.m)+' · '+esc(m.c||'Moto')+'</span>'
      +'<h3 class="r-nom"><a href="'+esc(m.u)+'">'+esc(m.n)+'</a></h3>'
      +'<p class="r-specs">'+esc(specs(m))+'</p>'
      +(pq?'<ul class="r-pourquoi">'+pq+'</ul>':'')+'</div></li>';
  }

  var AFFINER=[
    {id:'orig',q:'Une préférence d\u2019origine ?',
     opts:[['','Peu importe'],['japonaise','Japonaise','Honda, Yamaha, Kawasaki, Suzuki'],
           ['italienne','Italienne','Ducati, Aprilia, Moto Guzzi…'],['allemande','Allemande','BMW'],
           ['britannique','Britannique','Triumph'],['chinoise','Chinoise','CFMoto, Voge, Zontes…'],
           ['autre','Autre','KTM, Royal Enfield, Harley-Davidson…']]},
    {id:'car',q:'Quel caractère moteur ?',
     opts:[['','Peu importe'],['docile','Docile et souple','Facile à vivre, sans à-coups'],
           ['vif','Vif et sportif','Monte vite dans les tours'],
           ['couple','Plein de couple','De la poussée dès les bas régimes']]},
    {id:'auto',q:'Tu prends l\u2019autoroute ?',
     opts:[['','Peu importe'],['jamais','Jamais'],['parfois','De temps en temps'],['souvent','Souvent','Il faut de la puissance en réserve']]},
    {id:'leger',q:'Une moto légère à manœuvrer ?',
     opts:[['','Peu importe'],['oui','Oui, c\u2019est essentiel','Moins de 200 kg quand le poids est connu']]}
  ];
  var LIB_PREF={
    orig:{japonaise:'Origine japonaise',italienne:'Origine italienne',allemande:'Origine allemande',
          britannique:'Origine britannique',chinoise:'Origine chinoise',autre:'Autre origine'},
    car:{docile:'Moteur docile',vif:'Moteur vif',couple:'Du couple'},
    auto:{jamais:'Pas d\u2019autoroute',parfois:'Autoroute parfois',souvent:'Autoroute souvent'},
    leger:{oui:'Légère'}
  };
  function prefsActives(){
    var a=[];
    AFFINER.forEach(function(q){if(rep[q.id]&&LIB_PREF[q.id][rep[q.id]]) a.push(LIB_PREF[q.id][rep[q.id]]);});
    return a;
  }

  function rendreAffiner(){
    var avant={};AFFINER.forEach(function(q){avant[q.id]=rep[q.id]||'';});
    var h='<div class="tm-affiner"><h2 id="tm-leg" tabindex="-1">Affiner mes résultats</h2>'
      +'<p class="tm-aide">Quatre questions facultatives. « Peu importe » ne change rien au classement.</p>';
    AFFINER.forEach(function(q){
      h+='<fieldset class="tm-aff-groupe"><legend>'+esc(q.q)+'</legend><div class="tm-opts compact" role="radiogroup">';
      q.opts.forEach(function(o){
        var on=(rep[q.id]||'')===o[0];
        h+='<label class="q-opt"><input type="radio" name="aff-'+q.id+'" value="'+o[0]+'"'+(on?' checked':'')
          +'><span><b>'+esc(o[1])+'</b>'+(o[2]?'<small>'+esc(o[2])+'</small>':'')+'</span></label>';
      });
      h+='</div></fieldset>';
    });
    h+='<p class="tm-compte" id="aff-compte" role="status" aria-live="polite"></p>';
    h+='<div class="tm-nav"><button type="button" class="q-btn" id="aff-ok">Voir mes motos</button>'
      +'<button type="button" class="q-btn second" id="aff-annuler">Annuler</button></div></div>';
    conteneur.innerHTML=h;
    function lireChoix(){
      AFFINER.forEach(function(q){
        var c=conteneur.querySelector('input[name="aff-'+q.id+'"]:checked');
        rep[q.id]=c?c.value:'';
      });
    }
    /* nombre de motos qui respectent TOUS les criteres, sans assouplissement */
    function majCompte(){
      lireChoix();
      var n=classer({sel:!!(rep.taille&&rep.plat),orig:true,auto:true,leger:true,bud:parseInt(rep.budget,10)||0}).length;
      document.getElementById('aff-compte').textContent=n===0
        ?'Aucune moto ne respecte tous ces critères : le classement les assouplira.'
        :n+' moto'+(n>1?'s':'')+' respectent tous ces critères.';
    }
    conteneur.querySelectorAll('input[type=radio]').forEach(function(r){r.addEventListener('change',majCompte);});
    majCompte();
    document.getElementById('aff-ok').addEventListener('click',function(){
      lireChoix();
      rendreResultats();
    });
    document.getElementById('aff-annuler').addEventListener('click',function(){
      AFFINER.forEach(function(q){rep[q.id]=avant[q.id];});
      rendreResultats();
    });
    document.getElementById('tm-leg').focus({preventScroll:false});
  }

  function rendreResultats(){
    var r=calculer(),l=r.liste,h='',pa=prefsActives();
    h+='<div class="tm-res"><h2>'+(l.length?'Tes '+Math.min(3,l.length)+' motos':'Aucune moto trouvée')+'</h2>';
    if(pa.length) h+='<p class="tm-pref">Préférences : '+pa.map(esc).join(' · ')+'</p>';
    if(r.notes.length) h+='<ul class="tm-notes">'+r.notes.map(function(n){return '<li>'+esc(n)+'</li>';}).join('')+'</ul>';
    if(!l.length){
      h+='<p class="r-vide">Aucune fiche ne correspond à ces réponses. Essaie un autre usage ou un budget plus large, '
        +'ou ouvre le <a href="/comparateur.html">comparateur</a>.</p>';
    }else{
      h+='<ol class="r-liste">'+l.slice(0,3).map(function(x,i){return carte(x,i+1);}).join('')+'</ol>';
      if(l.length>3){
        h+='<div class="r-autres"><h3>Autres pistes</h3><ul>'+l.slice(3,9).map(function(x){
          return '<li><a href="'+esc(x.m.u)+'">'+esc(x.m.n)+'<span>'+fmt(x.m.ch)+' ch'
            +(x.m.pz?' · '+fmt(x.m.pz)+' €':'')+'</span></a></li>';}).join('')+'</ul></div>';
      }
    }
    h+='<div class="tm-nav"><button type="button" class="q-btn" id="tm-affiner">'
      +(pa.length?'Modifier mes préférences':'Affiner mes résultats')+'</button>'
      +'<button type="button" class="q-btn second" id="tm-modifier">Modifier mes réponses</button>'
      +'<button type="button" class="q-btn second" id="tm-refaire">Recommencer</button>'
      +'<a class="q-btn second" href="/touche-le-sol.html">Vérifier la hauteur de selle</a>'
      +'<a class="q-btn second" href="/comparateur.html">Ouvrir le comparateur</a></div>'
      +'<p class="outil-note">Classement calculé sur '+D.length+' motos encore produites, d’après les '
      +'caractéristiques de nos fiches. Vérifie prix et disponibilité chez le constructeur.</p></div>';
    conteneur.innerHTML=h;
    document.getElementById('tm-refaire').addEventListener('click',function(){
      rep={};idx=0;history.replaceState(null,'',location.pathname);rendreEtape(true);
    });
    document.getElementById('tm-affiner').addEventListener('click',rendreAffiner);
    document.getElementById('tm-modifier').addEventListener('click',function(){idx=0;rendreEtape(true);});
    var t=conteneur.querySelector('h2');t.setAttribute('tabindex','-1');t.focus({preventScroll:false});
    sauver();
    if(window.gtag) gtag('event','quiz_resultat',{usage:rep.usage,permis:rep.permis,affine:pa.length});
  }

  function sauver(){
    var p=new URLSearchParams();
    ['permis','usage','taille','entre','budget','exp','orig','car','auto','leger'].forEach(function(k){if(rep[k]) p.set(k,rep[k]);});
    if(rep.plat) p.set('plat','1');
    history.replaceState(null,'','?'+p.toString());
  }

  function barre(){
    return '<div class="tm-prog"><span>Question '+(idx+1)+' sur '+ETAPES.length+'</span>'
      +'<span class="tm-barre" aria-hidden="true"><i style="width:'+((idx+1)/ETAPES.length*100)+'%"></i></span></div>';
  }

  function rendreEtape(focus){
    var e=ETAPES[idx],h=barre()+'<fieldset><legend id="tm-leg" tabindex="-1">'+esc(e.q)+'</legend>'
      +'<p class="tm-aide">'+esc(e.aide)+'</p>';
    if(e.custom){
      h+='<div class="tm-champs"><div class="champ"><label for="tm-taille">Taille en cm</label>'
        +'<input id="tm-taille" type="number" inputmode="numeric" min="140" max="210" step="1" placeholder="175" value="'+(rep.taille||'')+'"></div>'
        +'<div class="champ"><label for="tm-entre">Entrejambe en cm (facultatif)</label>'
        +'<input id="tm-entre" type="number" inputmode="numeric" min="60" max="105" step="1" placeholder="Estimé" value="'+(rep.entre||'')+'"></div></div>'
        +'<label class="tm-case"><input type="checkbox" id="tm-plat"'+(rep.plat?' checked':'')+'>Je veux poser les deux pieds à plat</label>';
    }else{
      h+='<div class="tm-opts" role="radiogroup" aria-labelledby="tm-leg">';
      e.opts.forEach(function(o){
        h+='<label class="q-opt"><input type="radio" name="'+e.id+'" value="'+o[0]+'"'
          +(rep[e.id]===o[0]?' checked':'')+'><span><b>'+esc(o[1])+'</b>'
          +(o[2]?'<small>'+esc(o[2])+'</small>':'')+'</span></label>';
      });
      h+='</div>';
    }
    h+='</fieldset><div class="tm-nav">'
      +(idx>0?'<button type="button" class="q-btn second" id="tm-retour">Retour</button>':'')
      +'<button type="button" class="q-btn" id="tm-suite"'+(!e.custom&&!rep[e.id]?' disabled':'')+'>'
      +(idx===ETAPES.length-1?'Voir mes motos':(e.custom&&!rep.taille?'Passer':'Suivant'))+'</button></div>';
    conteneur.innerHTML=h;

    var suite=document.getElementById('tm-suite');
    function avancer(){
      if(e.custom){
        var t=parseInt(document.getElementById('tm-taille').value,10),
            en=parseInt(document.getElementById('tm-entre').value,10);
        rep.taille=(t>=140&&t<=210)?t:'';
        rep.entre=(en>=60&&en<=105)?en:'';
        rep.plat=rep.taille&&document.getElementById('tm-plat').checked?1:'';
      }
      if(idx<ETAPES.length-1){idx++;rendreEtape(true);}else{rendreResultats();}
    }
    suite.addEventListener('click',avancer);
    var retour=document.getElementById('tm-retour');
    if(retour) retour.addEventListener('click',function(){idx--;rendreEtape(true);});
    if(e.custom){
      var ti=document.getElementById('tm-taille');
      ti.addEventListener('input',function(){
        var v=parseInt(ti.value,10);suite.textContent=(idx===ETAPES.length-1)?'Voir mes motos':(v>=140&&v<=210?'Suivant':'Passer');
      });
    }else{
      conteneur.querySelectorAll('input[type=radio]').forEach(function(r){
        r.addEventListener('change',function(){rep[e.id]=r.value;suite.disabled=false;});
        r.addEventListener('click',function(ev){
          /* clic souris ou tactile : on passe a la suite ; le clavier garde le bouton */
          if(ev.detail>0){rep[e.id]=r.value;setTimeout(avancer,160);}
        });
      });
    }
    if(focus){var lg=document.getElementById('tm-leg');if(lg) lg.focus({preventScroll:false});}
  }

  function depuisUrl(){
    var p=new URLSearchParams(location.search);
    if(!p.get('permis')||!p.get('usage')||!p.get('exp')||!p.get('budget')) return false;
    rep={permis:p.get('permis'),usage:p.get('usage'),budget:p.get('budget'),exp:p.get('exp'),
         taille:parseInt(p.get('taille'),10)||'',entre:parseInt(p.get('entre'),10)||'',plat:p.get('plat')?1:''};
    AFFINER.forEach(function(q){
      var v=p.get(q.id)||'';
      rep[q.id]=q.opts.some(function(o){return o[0]===v;})?v:'';
    });
    return !!CAT_USAGE[rep.usage];
  }

  conteneur.innerHTML='<p class="tm-aide">Chargement des fiches…</p>';
  fetch(SRC).then(function(r){return r.json();}).then(function(d){
    D=d;preparer();
    if(depuisUrl()) rendreResultats(); else rendreEtape(false);
  }).catch(function(){
    conteneur.innerHTML='<p class="r-vide">Impossible de charger les fiches. Réessaie, ou ouvre le '
      +'<a href="/comparateur.html">comparateur</a>.</p>';
  });
})();
"""


# ---------------------------------------------------------------- selle
JS_SELLE = r"""
(function(){
  var conteneur=document.getElementById('sl');
  if(!conteneur) return;
  var SRC=conteneur.getAttribute('data-src');
  var ZONES=[
    {nom:'Pieds à plat',c:'var(--vert)',aide:'Tu poses toute la semelle des deux pieds.'},
    {nom:'Presque à plat',c:'#6aa07f',aide:'Les talons se lèvent à peine.'},
    {nom:'Sur la pointe des pieds',c:'#d99a2b',aide:'Praticable avec de l’habitude ; moins rassurant en manœuvre.'},
    {nom:'Trop haute',c:'var(--rouge)',aide:'Difficile à l’arrêt, surtout chargée ou en pente.'}
  ];
  var D=[];

  function esc(s){return String(s).replace(/[&<>"]/g,function(c){
    return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
  function fmt(n){return String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g,' ');}
  function zone(ec){return ec>=0?0:ec>=-40?1:ec>=-90?2:3;}

  conteneur.innerHTML=
    '<div class="sl-tete"><div class="sl-taille"><label for="sl-taille">Ta taille</label>'
    +'<div class="sl-val"><span id="sl-aff">175</span><small>cm</small></div>'
    +'<input id="sl-taille" type="range" min="145" max="200" step="1" value="175" aria-describedby="sl-resume"></div>'
    +'<div class="sl-opts"><div class="champ"><label for="sl-entre">Entrejambe en cm</label>'
    +'<input id="sl-entre" type="number" inputmode="numeric" min="60" max="105" placeholder="Estimé"></div>'
    +'<label class="tm-case"><input type="checkbox" id="sl-a2">Seulement les A2</label></div></div>'
    +'<p class="sl-resume" id="sl-resume" role="status"></p>'
    +'<div class="sl-histo" id="sl-histo" aria-hidden="true"></div>'
    +'<div class="sl-axe" aria-hidden="true"><span>650 mm</span><span>Hauteur de selle</span><span>900 mm</span></div>'
    +'<div class="sl-legende" id="sl-leg"></div><div id="sl-groupes"></div>';

  var taille=document.getElementById('sl-taille'),aff=document.getElementById('sl-aff'),
      entre=document.getElementById('sl-entre'),a2=document.getElementById('sl-a2'),
      resume=document.getElementById('sl-resume'),histo=document.getElementById('sl-histo'),
      groupes=document.getElementById('sl-groupes'),leg=document.getElementById('sl-leg');
  leg.innerHTML=ZONES.map(function(z){return '<span style="--c:'+z.c+'">'+esc(z.nom)+'</span>';}).join('');

  var ouverts={0:true,1:true};
  groupes.addEventListener('toggle',function(ev){
    var d=ev.target;if(d.dataset&&d.dataset.z!==undefined) ouverts[d.dataset.z]=d.open;
  },true);

  function portee(){
    var en=parseInt(entre.value,10);
    var inseam=(en>=60&&en<=105)?en*10:parseInt(taille.value,10)*10*0.45;
    return inseam+30;
  }

  function maj(){
    aff.textContent=taille.value;
    var p=portee(),liste=D.filter(function(m){return !a2.checked||m.a2==='oui';}),
        par=[[],[],[],[]];
    liste.forEach(function(m){par[zone(p-m.s)].push(m);});
    par.forEach(function(g){g.sort(function(a,b){return a.s-b.s||a.n.localeCompare(b.n);});});

    var aplat=par[0].length+par[1].length;
    resume.innerHTML='Portée estimée : <b>'+fmt(p)+' mm</b>. Sur '+liste.length+' motos, '
      +'<b>'+par[0].length+'</b> te laissent les pieds à plat et <b>'+aplat+'</b> au moins presque à plat.';

    /* histogramme par tranche de 10 mm */
    var bins=[],min=650,max=900,i;
    for(i=min;i<max;i+=10) bins.push(0);
    liste.forEach(function(m){var b=Math.floor((Math.min(max-1,Math.max(min,m.s))-min)/10);bins[b]++;});
    var top=Math.max.apply(null,bins)||1;
    histo.innerHTML=bins.map(function(n,j){
      var s=min+j*10+5,z=zone(p-s);
      return '<i class="z'+z+'" style="height:'+(n?Math.max(6,n/top*100):2)+'%"></i>';
    }).join('');

    groupes.innerHTML=par.map(function(g,z){
      var zn=ZONES[z],open=ouverts[z]===undefined?false:ouverts[z];
      var corps=g.length?'<ul class="sl-grille">'+g.map(function(m){
        return '<li><a href="'+esc(m.u)+'"><span>'+esc(m.n)+'</span><em>'+fmt(m.s)+' mm'
          +(m.a2==='oui'?' · A2':'')+'</em></a></li>';}).join('')+'</ul>'
        :'<p class="sl-vide">Aucune moto de notre base dans cette zone.</p>';
      return '<details class="sl-groupe" data-z="'+z+'"'+(open?' open':'')+'><summary>'
        +'<span class="sl-titre"><span class="sl-pastille" style="--c:'+zn.c+'"></span>'+esc(zn.nom)+'</span>'
        +'<span class="sl-nb">'+g.length+'</span></summary>'
        +'<p class="sl-vide">'+esc(zn.aide)+'</p>'+corps+'</details>';
    }).join('');
  }

  taille.addEventListener('input',maj);
  entre.addEventListener('input',maj);
  a2.addEventListener('change',maj);

  fetch(SRC).then(function(r){return r.json();}).then(function(d){
    D=d.filter(function(m){return m.s>0;});
    maj();
  }).catch(function(){
    groupes.innerHTML='<p class="r-vide">Impossible de charger les fiches. Réessaie, ou ouvre le '
      +'<a href="/comparateur.html">comparateur</a>.</p>';
  });
})();
"""
