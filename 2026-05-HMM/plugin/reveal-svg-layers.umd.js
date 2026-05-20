/* plugin/reveal-svg-layers.umd.js
 *
 * Inline an external SVG and reveal its Inkscape layers as fragments.
 *
 * Two modes:
 *  - Monotonic (original AQV behaviour): data-base / data-include / data-order.
 *      Each non-base layer is shown by one fragment and never hidden on
 *      forward navigation.
 *  - Explicit step-sets: data-steps="L1,L2 ; L1,L3 ; ..."
 *      Each ';'-separated group is one fragment and lists EXACTLY the
 *      (non-base) layers visible at that step. Layers can therefore be
 *      hidden again as the build advances. data-base layers (if any) are
 *      always visible.
 *
 * Container scan happens on Reveal's 'ready' event so it also works when
 * slides are produced by the markdown plugin.
 */
(function (root, factory) {
  if (typeof define === 'function' && define.amd) { define([], function () { return factory(root); }); }
  else if (typeof module === 'object' && module.exports) { module.exports = factory(root); }
  else { root.SvgLayers = factory(root); }
}(typeof self !== 'undefined' ? self : this, function (root) {
  'use strict';

  var options = root.SvgLayersOptions || { selector: '.r-svg-layers', fragmentClass: '' };
  var deck = null;
  var teardownFns = [];
  var STYLE_ID = 'reveal-svg-layers-style';

  function ensureStyle () {
    if (document.getElementById(STYLE_ID)) return;
    var style = document.createElement('style');
    style.id = STYLE_ID;
    style.textContent = '.rsvg-fragment{display:inline-block;width:0;height:0;overflow:hidden}.rsvg-hidden{visibility:hidden}';
    document.head.appendChild(style);
  }

  var uniqId = (function(){ var c=0; return function(prefix){ return (prefix||'rsvg')+'-'+(++c); }; })();
  function toList(v){ return (v||'').split(',').map(function(s){return s.trim();}).filter(Boolean); }
  function qsa(rootEl, sel){ return Array.prototype.slice.call(rootEl.querySelectorAll(sel)); }
  function getLabel(el){ return el.getAttribute('inkscape:label') || el.getAttribute('data-label') || el.id || ''; }
  function findLayers(svg){
    var a = qsa(svg,'g[inkscape\\:groupmode="layer"],g[groupmode="layer"]');
    if (a.length) return a;
    var b = qsa(svg,':scope > g[id]');
    if (b.length) return b;
    return qsa(svg,'g');
  }
  function hideLayer(el){ el.classList.add('rsvg-hidden'); }
  function showLayer(el){ el.classList.remove('rsvg-hidden'); }

  // Our placeholders are injected on Reveal's 'ready', after author
  // fragments were already indexed — and a slide may hold several
  // containers plus author fragments. Re-stamp data-fragment-index on
  // EVERY fragment of the slide in strict DOM order so all of them
  // (multiple SVGs + author fragments) advance one step at a time.
  function normalizeFragmentOrder(container){
    var slide = container.closest ? container.closest('section') : null;
    if (!slide) return;
    qsa(slide, '.fragment').forEach(function(f, idx){
      f.setAttribute('data-fragment-index', String(idx));
    });
    if (deck && typeof deck.sync === 'function') deck.sync();
  }

  // ---- Explicit step-sets mode -------------------------------------------
  function buildStepSets(ctx){
    var container = ctx.container, svg = ctx.svg, fragmentClass = ctx.fragmentClass;
    var allLayers = findLayers(svg);

    var byName = new Map();
    allLayers.forEach(function(g){ byName.set(getLabel(g).toLowerCase(), g); });

    var baseSet = new Set(toList(container.getAttribute('data-base')).map(function(s){return s.toLowerCase();}));
    var extraFrag = container.getAttribute('data-fragment-class') || fragmentClass || '';

    // Parse "a,b ; c ; d,e" -> [Set(a,b), Set(c), Set(d,e)]
    var stepSets = (container.getAttribute('data-steps') || '')
      .split(';')
      .map(function(grp){ return grp.trim(); })
      .filter(function(grp){ return grp.length; })
      .map(function(grp){
        return new Set(grp.split(',').map(function(s){ return s.trim().toLowerCase(); }).filter(Boolean));
      });

    function applyStep(idx){
      allLayers.forEach(function(el){
        var name = getLabel(el).toLowerCase();
        var visible = baseSet.has(name) || (idx >= 0 && stepSets[idx] && stepSets[idx].has(name));
        if (visible) showLayer(el); else hideLayer(el);
      });
    }

    var uid = uniqId('rsvgs');
    var placeholders = stepSets.map(function(_, i){
      var span = document.createElement('span');
      span.className = 'fragment rsvg-fragment' + (extraFrag ? (' ' + extraFrag) : '');
      span.setAttribute('data-rsvg-uid', uid);
      span.setAttribute('data-rsvg-step', String(i));
      container.appendChild(span);
      return span;
    });

    function currentStep(){
      var cur = -1;
      placeholders.forEach(function(ph, i){
        if (ph.classList.contains('visible')) cur = i;
      });
      return cur;
    }
    function sync(){ applyStep(currentStep()); }

    function onFragment(ev){
      var ph = ev.fragment;
      if (ph && ph.getAttribute && ph.getAttribute('data-rsvg-uid') === uid) sync();
    }
    function onSlideChanged(ev){
      if (ev.currentSlide && ev.currentSlide.contains(container)) sync();
    }

    deck.on('fragmentshown', onFragment);
    deck.on('fragmenthidden', onFragment);
    deck.on('slidechanged', onSlideChanged);

    teardownFns.push(function(){
      try{ deck.off('fragmentshown', onFragment); }catch(e){}
      try{ deck.off('fragmenthidden', onFragment); }catch(e){}
      try{ deck.off('slidechanged', onSlideChanged); }catch(e){}
      placeholders.forEach(function(ph){ ph.remove(); });
      allLayers.forEach(showLayer);
    });

    normalizeFragmentOrder(container);
    sync(); // initial (handles deep-linking into a fragment)
  }

  // ---- Original monotonic mode -------------------------------------------
  function buildSteps(ctx){
    var container = ctx.container, svg = ctx.svg, fragmentClass = ctx.fragmentClass;
    var allLayers = findLayers(svg);

    var includeList = toList(container.getAttribute('data-include'));
    var baseList    = toList(container.getAttribute('data-base'));
    var order       = (container.getAttribute('data-order') || 'document').toLowerCase();
    var extraFrag   = container.getAttribute('data-fragment-class') || fragmentClass || '';

    var baseSet = new Set(baseList.map(function(s){return s.toLowerCase();}));
    function byName(g){ return getLabel(g).toLowerCase(); }

    var baseLayers = [], candidates = [];
    allLayers.forEach(function(g){
      (baseSet.has(byName(g)) ? baseLayers : candidates).push(g);
    });

    candidates.forEach(hideLayer);

    var stepLayers = candidates.slice();
    if (includeList.length){
      var mapBy = new Map(candidates.map(function(el){ return [byName(el), el]; }));
      stepLayers = includeList.map(function(n){ return mapBy.get(n.toLowerCase()); }).filter(Boolean);
    } else if (order === 'reverse'){
      stepLayers.reverse();
    }

    baseLayers.forEach(showLayer);

    var uid = uniqId('rsvgc');
    var placeholders = stepLayers.map(function(layerEl, i){
      var span = document.createElement('span');
      span.className = 'fragment rsvg-fragment' + (extraFrag ? (' ' + extraFrag) : '');
      span.setAttribute('data-rsvg-uid', uid);
      span.setAttribute('data-rsvg-index', String(i));
      span.__rsvgLayer = layerEl;
      container.appendChild(span);
      return span;
    });

    function syncFromVisibleFragments(){
      candidates.forEach(hideLayer);
      placeholders.forEach(function(ph){
        if (ph.classList.contains('visible')) showLayer(ph.__rsvgLayer);
      });
      baseLayers.forEach(showLayer);
    }

    function onFragmentShown(ev){
      var ph = ev.fragment;
      if (ph && ph.getAttribute('data-rsvg-uid') === uid) showLayer(ph.__rsvgLayer);
    }
    function onFragmentHidden(ev){
      var ph = ev.fragment;
      if (ph && ph.getAttribute('data-rsvg-uid') === uid) hideLayer(ph.__rsvgLayer);
    }
    function onSlideChanged(ev){
      var current = ev.currentSlide;
      if (current && current.contains(container)) syncFromVisibleFragments();
    }

    deck.on('fragmentshown', onFragmentShown);
    deck.on('fragmenthidden', onFragmentHidden);
    deck.on('slidechanged',  onSlideChanged);

    teardownFns.push(function(){
      try{ deck.off('fragmentshown', onFragmentShown); }catch(e){}
      try{ deck.off('fragmenthidden', onFragmentHidden); }catch(e){}
      try{ deck.off('slidechanged', onSlideChanged); }catch(e){}
      placeholders.forEach(function(ph){ ph.remove(); });
      candidates.forEach(showLayer);
    });

    normalizeFragmentOrder(container);
    syncFromVisibleFragments();
  }

  function inlineExternalSvg(container, srcUrl){
    return fetch(srcUrl).then(function(res){
      if (!res.ok) throw new Error('Failed to load SVG: ' + srcUrl);
      return res.text();
    }).then(function(text){
      var parser = new DOMParser();
      var doc = parser.parseFromString(text, 'image/svg+xml');
      var svg = document.importNode(doc.documentElement, true);
      // Make the inlined SVG scale to its container (keep aspect via viewBox).
      if (svg.getAttribute('viewBox')){
        svg.removeAttribute('width');
        svg.removeAttribute('height');
      }
      svg.setAttribute('style', 'max-width:100%; width:100%; height:auto; display:block;');
      container.appendChild(svg);
      return svg;
    });
  }

  function initContainer(container){
    if (container.__rsvgProcessed) return Promise.resolve();
    container.__rsvgProcessed = true;

    var svg = container.querySelector('svg');
    var src = container.getAttribute('data-src');

    var p = Promise.resolve();
    if (!svg && src) p = inlineExternalSvg(container, src).then(function(s){ svg = s; });

    return p.then(function(){
      if (!svg) return;
      var ctx = { container: container, svg: svg, fragmentClass: options.fragmentClass };
      if (container.hasAttribute('data-steps')) buildStepSets(ctx);
      else buildSteps(ctx);
    }).catch(function(e){
      console.error('[svg-layers] ' + e.message);
    });
  }

  function scanAll(){
    var rootEl = deck.getRevealElement();
    var containers = qsa(rootEl, options.selector || '.r-svg-layers');
    return Promise.all(containers.map(initContainer));
  }

  var plugin = {
    id: 'svg-layers',
    init: function (revealDeck) {
      deck = revealDeck;
      ensureStyle();
      // Scan on 'ready' so markdown-generated slides are already in the DOM.
      deck.on('ready', scanAll);
      // If we somehow registered after 'ready' fired, scan immediately.
      if (deck.isReady && deck.isReady()) scanAll();
      return Promise.resolve();
    },
    destroy: function(){
      teardownFns.forEach(function(fn){ try{ fn(); }catch(e){} });
      teardownFns = [];
    }
  };

  return plugin;
}));
