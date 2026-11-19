/* LaTeX labels inside SVG figures, rendered by KaTeX, as a reveal plugin.

   In the SVG, write a label as ordinary text whose whole content is math:
       <text x="250" y="374" font-size="28" text-anchor="middle">$\pi_a$</text>
   On the slide, mark the image:
       <img src="figures/fig.svg" data-math style="width:80%">

   On 'ready' the plugin waits for KaTeX (loaded by RevealMath.KaTeX), fetches
   each marked SVG, replaces every $...$ <text> by a <foreignObject> holding the
   KaTeX rendering, and puts the inline SVG in place of the <img>.
   The label keeps the text's position, font-size, fill, text-anchor and transform;
   its baseline sits on the text's y. Optional data-dx / data-dy on the <text>
   nudge it (SVG units).

   Usage: <script src="../plugin/reveal-svg-math.js"></script>
          Reveal.initialize({ plugins: [RevealMath.KaTeX, ..., SvgMath] })
*/
(function (global) {
    const MATH = /^\s*\$([\s\S]+)\$\s*$/;
    const XHTML = 'http://www.w3.org/1999/xhtml';
    const SVGNS = 'http://www.w3.org/2000/svg';

    function addStyle() {
        if (document.getElementById('svg-math-style')) return;
        const s = document.createElement('style');
        s.id = 'svg-math-style';
        // label size = the text's font-size (KaTeX alone would scale it by 1.21)
        s.textContent = '.svg-math-label .katex { font-size: 1em; }';
        document.head.appendChild(s);
    }

    function whenKatex(timeout = 15000) {
        return new Promise((resolve, reject) => {
            const t0 = Date.now();
            (function poll() {
                if (global.katex) return resolve(global.katex);
                if (Date.now() - t0 > timeout) return reject(new Error('KaTeX not loaded'));
                setTimeout(poll, 50);
            })();
        });
    }

    const num = v => (v == null ? NaN : parseFloat(String(v).trim().split(/[\s,]+/)[0]));

    function attrOrStyle(el, name) {
        const a = el.getAttribute(name);
        if (a) return a;
        const m = (el.getAttribute('style') || '').match(new RegExp(name + '\\s*:\\s*([^;]+)'));
        return m ? m[1].trim() : null;
    }

    // Render off screen at the label's size, to read its width, height and baseline
    // in CSS px, which are SVG user units inside the foreignObject.
    function renderLabel(katex, tex, fontSize, color) {
        const box = document.createElement('div');
        box.className = 'svg-math-label';
        box.style.cssText = `font-size:${fontSize}px; color:${color}; white-space:nowrap; line-height:normal;`;
        const math = document.createElement('span');
        katex.render(tex, math, { throwOnError: false });
        const mark = document.createElement('span');
        mark.style.cssText = 'display:inline-block; width:0; height:0; vertical-align:baseline;';
        box.append(math, mark);
        return { box, math, mark };
    }

    async function convertTexts(katex, svg) {
        const labels = [];
        svg.querySelectorAll('text').forEach(text => {
            const m = text.textContent.match(MATH);
            if (!m) return;
            const fontSize = num(attrOrStyle(text, 'font-size')) || 16;
            const color = attrOrStyle(text, 'fill') || 'currentColor';
            labels.push({ text, tex: m[1], fontSize, ...renderLabel(katex, m[1], fontSize, color) });
        });
        if (!labels.length) return;

        // measure off screen (works for slides that are not displayed yet)
        const stage = document.createElement('div');
        stage.style.cssText = 'position:absolute; left:-10000px; top:0; visibility:hidden;';
        labels.forEach(l => {
            const wrap = document.createElement('div');
            wrap.style.cssText = 'position:absolute; left:0; top:0;';
            wrap.appendChild(l.box);
            stage.appendChild(wrap);
        });
        document.body.appendChild(stage);
        if (document.fonts && document.fonts.ready) await document.fonts.ready;

        labels.forEach(l => {
            const box = l.box.getBoundingClientRect();
            const w = l.math.getBoundingClientRect().width;
            const baseline = l.mark.getBoundingClientRect().top - box.top;
            const anchor = attrOrStyle(l.text, 'text-anchor') || 'start';
            const x = (num(l.text.getAttribute('x')) || 0) + (num(l.text.dataset.dx) || 0);
            const y = (num(l.text.getAttribute('y')) || 0) + (num(l.text.dataset.dy) || 0);
            const x0 = anchor === 'middle' ? x - w / 2 : anchor === 'end' ? x - w : x;

            const fo = document.createElementNS(SVGNS, 'foreignObject');
            fo.setAttribute('x', x0);
            fo.setAttribute('y', y - baseline);
            fo.setAttribute('width', Math.ceil(w) + 2);
            fo.setAttribute('height', Math.ceil(box.height) + 2);
            if (l.text.getAttribute('transform')) fo.setAttribute('transform', l.text.getAttribute('transform'));
            fo.style.overflow = 'visible';

            const holder = document.createElementNS(XHTML, 'div');
            holder.appendChild(l.box); // moves the rendered label out of the stage
            fo.appendChild(holder);
            l.text.replaceWith(fo);
        });
        stage.remove();
    }

    async function inline(katex, img) {
        const res = await fetch(img.getAttribute('src'));
        if (!res.ok) throw new Error('cannot load ' + img.getAttribute('src'));
        const doc = new DOMParser().parseFromString(await res.text(), 'image/svg+xml');
        const svg = document.importNode(doc.documentElement, true);
        await convertTexts(katex, svg);

        // the inline SVG takes the image's place and sizing
        if (svg.getAttribute('viewBox')) {
            svg.removeAttribute('width');
            svg.removeAttribute('height');
        }
        if (img.className) svg.setAttribute('class', img.className);
        if (img.id) svg.id = img.id;
        svg.setAttribute('style', (img.getAttribute('style') || '') + '; height:auto; overflow:visible;');
        svg.setAttribute('role', 'img');
        if (img.alt) svg.setAttribute('aria-label', img.alt);
        img.replaceWith(svg);
    }

    global.SvgMath = {
        id: 'svg-math',
        init(deck) {
            addStyle();
            deck.on('ready', async () => {
                const imgs = [...deck.getRevealElement().querySelectorAll('img[data-math]')];
                if (!imgs.length) return;
                try {
                    const katex = await whenKatex();
                    await Promise.all(imgs.map(img => inline(katex, img).catch(e => console.error('[svg-math]', e))));
                    deck.layout();
                } catch (e) {
                    console.error('[svg-math]', e);
                }
            });
        },
    };
})(window);
