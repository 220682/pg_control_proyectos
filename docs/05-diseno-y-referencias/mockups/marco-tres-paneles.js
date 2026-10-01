/* Marco de tres paneles compartido (F0-U1). Copia fiel de los paneles de plan-maestro-tres-paneles.html.
   Cada maqueta define antes: window.MARCO_ACTIVO = '<id del acceso activo>' y, opcional, window.MARCO_PANELES = '00' | '11'
   (izquierdo/derecho ocultos: 1 = oculto). Abre igual desde file://. Sin credenciales ni datos reales. */
(function(){
function esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;');}
var ACTIVO=window.MARCO_ACTIVO||'';
var C={proy:'#22d3ee',plan:'#4f7df3',cost:'#fbbf24',sup:'#c084fc',log:'#34d399',ot:'#38bdf8',adm:'#fb923c',sso:'#fb7185',rec:'#2dd4bf'};
/* id: [etiqueta, color, glifo, activo(1)/inerte(0), acción(1)] */
var R={
 'ot':['(OT) Orden de trabajo','proy','✓',0],'alcance-servicio':['Alcance del servicio','proy','◎',0],'presupuesto':['Presupuesto del proyecto','proy','$',0],
 'dp':['DP (Datos del proyecto)','proy','▤',1],'paquetes-trabajo':['Paquetes de Trabajo','plan','▣',1],'cronograma':['Cronograma','plan','≡',1],'plan-maestro':['Plan Maestro','plan','▦',1],
 'cargos-hh':['Cargos (HH)','proy','☺',0],'equipos-hm':['Equipos (HM)','proy','✚',0],'materiales':['Materiales (c/c)','proy','▥',0],'personal-nuevo':['Personal NUEVO','proy','+',0],
 'planos':['Planos','ot','┼',0],'pets':['Pets','sso','✔',0],
 'consolidado-rdts':['Consolidado RDTs','sup','▤',1],'status-requerimiento':['Status de requerimiento','log','◫',1],'pr':['PR (Reporte del proyecto)','plan','▧',1],'dashboard':['Dashboard','plan','▦',1],'curva-s':['Curva S','plan','∿',1],
 'costos-servicios':['Registro de costos por servicios','log','$',1],'consolidado-servicio':['Consolidado de servicio','proy','✓',0],
 'crear-requerimiento-servicios':['Crear requerimiento de servicios','log','▤',1,1],'crear-rdt':['Crear RDTs','sup','▤',1,1],'rdt':['Subir RDTs','sup','✔',1,1],'crear-paquete':['Crear paquete','plan','+',1,1],
 'ficha-servicio':['Ficha del servicio','proy','i',1],'editar-servicio':['Editar servicio','proy','✎',1,1],'editar-checklist':['Editar checklist','proy','≡',1,1],
 'tareo-moi':['Tareo MOI','adm','◷',0],'consolidado-moi':['Consolidado MOI','adm','▤',0],'status-servicios':['Status de servicios','cost','~',0],'acta-conformidad':['Acta de conformidad','sup','✔',0],
 'consolidado-rq':['Consolidado RQ','log','▤',1],'notif':['Notificaciones','proy','◔',1],
 '3wla':['3WLA','plan','▦',0],'programacion-diaria':['Programación diaria','plan','▤',0],'status-capacitaciones':['Status de capacitaciones','plan','▤',0],'programacion-capacitaciones':['Programación de capacitaciones','plan','▤',0],
 'status-rdts':['Status de RDTs','sup','≡',1],'listado-rdts':['Archivo de RDTs subidos','sup','◷',1],'informe-servicio':['Informe de servicio','sup','▤',0]};
var IZQ=[['Alcance y presupuesto',['ot',['alcance-servicio','Alcance'],['presupuesto','Presupuesto'],'dp','paquetes-trabajo']],
 ['Planificación',['cronograma','plan-maestro']],
 ['Recursos del servicio',['cargos-hh','equipos-hm',['materiales','Materiales (c/c)'],'personal-nuevo']],
 ['Documentación',['planos',['pets','PETS']]],
 ['Reportes',['consolidado-rdts',['status-requerimiento','Requerimiento (RQ)'],'pr','dashboard','curva-s',['costos-servicios','Registro de costos'],'consolidado-servicio']],
 ['Acciones',[['crear-requerimiento-servicios','Generar RQ'],['crear-rdt','Crear RDT'],['rdt','Subir RDT'],'crear-paquete']],
 ['Servicio',['ficha-servicio','editar-servicio','editar-checklist']]];
var DER=[['Planificación','plan',['notif','cronograma','paquetes-trabajo','plan-maestro','3wla','programacion-diaria','pr','dashboard','curva-s','status-capacitaciones','programacion-capacitaciones']],
 ['Costos','cost',['notif','status-servicios']],
 ['Supervisión operativa','sup',['notif','crear-rdt','rdt','status-rdts','listado-rdts','consolidado-rdts','informe-servicio','acta-conformidad']],
 ['Logística','log',['notif','crear-requerimiento-servicios','status-requerimiento','consolidado-rq','costos-servicios']],
 ['Oficina Técnica','ot',['notif']],
 ['Administración','adm',['notif','tareo-moi','consolidado-moi']],
 ['SSOMA','sso',['notif','pets']]];
var RAPIDO=[['tareo-moi'],['pets'],['acta-conformidad'],['status-servicios'],['status-requerimiento','Requerimiento'],['consolidado-rq'],['rdt']];
var RECURSOS=['Personal','Cargos','Equipos','Causas CNC'];
function ico(c,g){return '<span class="ic" style="--c:'+C[c]+'" aria-hidden="true">'+g+'</span>';}
function fila(def,lado){var id=typeof def==='string'?def:def[0],a=R[id],et=(typeof def==='string'?a[0]:def[1]),sel=(id===ACTIVO);
 var mk=(lado==='der'&&a[4])?' <span class="mk">Acción</span>':'';
 if(a[3]){return '<a href="#" class="it'+(sel?' sel':'')+'" data-chip="'+id+'"'+(sel?' aria-current="page"':'')+'>'+ico(a[1],a[2])+esc(et)+mk+'</a>';}
 return '<span class="it inerte" data-chip="'+id+'" title="Sin pantalla todavía">'+ico(a[1],a[2])+esc(et)+mk+'</span>';}
function navIzq(){var h='<nav aria-label="Navegación principal"><a href="#" class="it" style="margin-bottom:0"><span class="ic" style="--c:'+C.proy+'" aria-hidden="true">▦</span>Todos los servicios</a>'
 +'<div class="srv" data-testid="servicio-actual"><p class="k">Servicio actual</p><p class="n">S-0001 (simulado)</p><p class="m">Servicio de prueba</p></div>'
 +'<div class="rec grp-n"><button type="button" class="rec-bt" aria-expanded="false">Recursos de empresa <span class="cv" aria-hidden="true">›</span></button><div class="rec-ls" hidden>'
 +RECURSOS.map(function(n){return '<a href="#" class="it"><span class="ic" style="--c:'+C.rec+'" aria-hidden="true">●</span>'+n+'</a>';}).join('')+'</div></div>';
 IZQ.forEach(function(g){var inf=[],acc=[];g[1].forEach(function(d){var id=typeof d==='string'?d:d[0];(R[id][4]?acc:inf).push(d);});
  var solo=(g[0]==='Acciones');
  h+='<div class="grp-n" data-grupo="'+g[0]+'"><p class="ttl">'+g[0]+'</p>'+inf.map(function(d){return fila(d,'izq');}).join('');
  if(acc.length){h+='<div'+(solo?'':' class="acc-blk"')+'>'+(solo?'':'<p class="sub">Acciones</p>')+acc.map(function(d){return fila(d,'izq');}).join('')+'</div>';}
  h+='</div>';});
 return h+'</nav>';}
var SVG={users:'<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/>',
 bell:'<path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/>',
 out:'<path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><path d="M16 17l5-5-5-5M21 12H9"/>'};
function pieIzq(){return '<div class="ibs"><button type="button" class="ib" title="Usuarios" aria-label="Usuarios"><svg viewBox="0 0 24 24" aria-hidden="true">'+SVG.users+'</svg></button>'
 +'<button type="button" class="ib" title="Notificaciones" aria-label="Notificaciones, 3 pendientes"><svg viewBox="0 0 24 24" aria-hidden="true">'+SVG.bell+'</svg><span class="bd">3</span></button>'
 +'<button type="button" class="ib" title="Configuraciones" aria-label="Configuraciones"><span aria-hidden="true">⚙</span></button>'
 +'<button type="button" class="ib" title="Cerrar sesión" aria-label="Cerrar sesión"><svg viewBox="0 0 24 24" aria-hidden="true">'+SVG.out+'</svg></button></div>'
 +'<div class="vc"><label>Ver como</label><select aria-label="Ver como"><option>Mi rol (Administrador)</option></select></div>'
 +'<a href="#" class="usr" title="Mi entorno"><span class="av" aria-hidden="true">UP</span><span style="min-width:0"><b>Usuario de prueba</b><span>Administrador</span></span></a>';}
function herr(){var h='<div class="sep-d"><p class="ttl" style="padding:0;margin-bottom:8px">Accesos rápidos</p><div class="chips" data-testid="accesos-rapidos">'
 +RAPIDO.map(function(d){var a=R[d[0]],et=d[1]||a[0],mk=a[4]?' <span class="mk">Acción</span>':'';
  return a[3]?'<a href="#" class="chip" data-chip="'+d[0]+'"><span aria-hidden="true">'+a[2]+'</span>'+esc(et)+mk+'</a>':'<span class="chip inerte" data-chip="'+d[0]+'" title="Sin pantalla todavía"><span aria-hidden="true">'+a[2]+'</span>'+esc(et)+'</span>';}).join('')+'</div></div>'
 +'<p class="ttl" style="padding:0;margin-bottom:8px">Grupos del servicio</p><div class="acord">';
 DER.forEach(function(g,k){h+='<div class="ag" data-g="'+k+'"><button type="button" aria-expanded="'+(k===0?'true':'false')+'" style="'+(k===0?'color:'+C[g[1]]:'')+'">'+g[0]+'<span class="cv" aria-hidden="true">&#9662;</span></button><div class="lst"'+(k===0?'':' hidden')+'>'
  +g[2].map(function(id){return fila(id,'der');}).join('')+'</div></div>';});
 return h+'</div>';}
function pintaPaneles(){
 document.querySelectorAll('.nav-izq').forEach(function(e){e.innerHTML=navIzq();});
 document.querySelectorAll('.pie-izq').forEach(function(e){e.innerHTML=pieIzq();});
 document.querySelectorAll('.herr').forEach(function(e){e.innerHTML=herr();});}
document.addEventListener('click',function(e){
 var a=e.target.closest('a[href="#"]');if(a){e.preventDefault();}
 var rb=e.target.closest('.rec-bt');if(rb){var ls=rb.parentNode.querySelector('.rec-ls'),o=ls.hidden;ls.hidden=!o;rb.setAttribute('aria-expanded',o?'true':'false');rb.querySelector('.cv').textContent=o?'⌄':'›';return;}
 var gb=e.target.closest('.ag>button');if(gb){var box=gb.closest('.acord'),mio=gb.parentNode,abierto=gb.getAttribute('aria-expanded')==='true';
  box.querySelectorAll('.ag').forEach(function(x){var b=x.querySelector('button'),on=(x===mio)&&!abierto;b.setAttribute('aria-expanded',on?'true':'false');x.querySelector('.lst').hidden=!on;
   b.style.color=on?C[DER[+x.getAttribute('data-g')][1]]:'';});}
});
pintaPaneles();
/* ocultar/mostrar paneles (solo escritorio) */
var ocu={izq:false,der:false};
function pintaTg(lado){var b=document.querySelector('[data-tg="'+lado+'"]'),p=document.getElementById('pl-'+lado),oc=ocu[lado];p.classList.toggle('oculto',oc);
 var t=(oc?'Mostrar':'Ocultar')+' panel '+(lado==='izq'?'izquierdo':'derecho');b.setAttribute('aria-expanded',oc?'false':'true');b.setAttribute('aria-label',t);b.title=t;
 b.innerHTML=(lado==='izq')?(oc?'&#8250;':'&#8249;'):(oc?'&#8249;':'&#8250;');}
function setPaneles(i,d){ocu.izq=!!i;ocu.der=!!d;pintaTg('izq');pintaTg('der');
 var k=(ocu.izq?'1':'0')+(ocu.der?'1':'0');document.querySelectorAll('[data-pan]').forEach(function(o){o.setAttribute('aria-pressed',o.getAttribute('data-pan')===k?'true':'false');});
 setTimeout(function(){window.dispatchEvent(new Event('resize'));},0);}
document.querySelectorAll('[data-tg]').forEach(function(b){b.addEventListener('click',function(){var l=b.getAttribute('data-tg');setPaneles(l==='izq'?!ocu.izq:ocu.izq,l==='der'?!ocu.der:ocu.der);});});
document.querySelectorAll('[data-pan]').forEach(function(b){b.addEventListener('click',function(){var k=b.getAttribute('data-pan');setPaneles(k.charAt(0)==='1',k.charAt(1)==='1');});});
var ini=window.MARCO_PANELES||'00';setPaneles(ini.charAt(0)==='1',ini.charAt(1)==='1');
/* cajones móviles (sin el icono de ocultar) */
var caj=document.getElementById('cajones'),origen=null;
function abreCajon(lado,btn){cerrarCajon(true);origen=btn;
 var der=(lado==='r');
 caj.innerHTML='<div class="velo" data-cierra="1"></div><aside class="cajon '+lado+'" role="dialog" aria-modal="true" aria-label="'+(der?'Herramientas':'Menú')+'"><div class="ct"><span>'+(der?'Herramientas':'Menú')+'</span><button type="button" data-cierra="1" aria-label="Cerrar">&times;</button></div>'
  +(der?'<div class="herr"></div>':'<div class="scroll-izq nav-izq"></div><div class="pie pie-izq"></div>')+'</aside>';
 pintaPaneles();caj.querySelector('button[data-cierra]').focus();}
function cerrarCajon(sinFoco){caj.innerHTML='';if(!sinFoco&&origen){origen.focus();}if(!sinFoco){origen=null;}}
document.getElementById('m-menu').addEventListener('click',function(){abreCajon('l',this);});
document.getElementById('m-herr').addEventListener('click',function(){abreCajon('r',this);});
caj.addEventListener('click',function(e){if(e.target.closest('[data-cierra]')){cerrarCajon();}});
document.addEventListener('keydown',function(e){if(e.key==='Escape'&&caj.firstChild){cerrarCajon();}});
})();
