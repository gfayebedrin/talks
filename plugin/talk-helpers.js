/* Shared markdown helpers for reveal.js talks, as a reveal plugin.
   Pair with theme/talk.css.

   - "Footnote: text" paragraph  → footnote pinned to the bottom of the slide
   - "Paper: Title | Authors, *Journal*, year" line → paper reference block,
     in markdown or inside an HTML block (where the line stays raw text)

   Usage: <script src="../plugin/talk-helpers.js"></script>
          Reveal.initialize({ plugins: [..., TalkHelpers] })
*/
(function (global) {
    const PAPER = /^\s*Paper:\s*/;
    const escape = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    const emphasis = s => s.replace(/\*([^*]+)\*/g, '<em>$1</em>');

    function footnotes(deck) {
        document.querySelectorAll('.reveal .slides section').forEach(slide => {
            if (slide.querySelector('section')) return; // skip parent sections
            slide.querySelectorAll('p').forEach(p => {
                if (p.textContent.trimStart().startsWith('Footnote:')) {
                    const footnote = document.createElement('div');
                    footnote.className = 'slide-footnote';
                    footnote.innerHTML = p.innerHTML.replace(/^Footnote:\s*/, '');
                    p.remove();
                    slide.classList.add('has-footnote');
                    slide.style.height = deck.getConfig().height + 'px';
                    slide.appendChild(footnote);
                }
            });
        });
    }

    function makePaper(html) {
        const [title, authors = ''] = html.replace(PAPER, '').split('|');
        const el = document.createElement('div');
        el.className = 'paper';
        el.innerHTML = `<span class="title">${title.trim()}</span><span class="authors">${authors.trim()}</span>`;
        return el;
    }

    // Side by side in a flex row: share the row. Alone on a slide: cap the width.
    function place(el) {
        const parent = el.parentElement;
        if (getComputedStyle(parent).display === 'flex') {
            el.style.flex = '1 1 0';
            el.style.margin = '0';
        } else if (parent.tagName === 'SECTION') {
            el.style.maxWidth = '60%';
        }
    }

    function papers() {
        const root = document.querySelector('.reveal .slides');

        // In markdown: the line was parsed into a <p>
        root.querySelectorAll('p').forEach(p => {
            if (!PAPER.test(p.textContent)) return;
            const el = makePaper(p.innerHTML);
            p.replaceWith(el);
            place(el);
        });

        // Inside HTML blocks: the line is raw text, possibly among other lines
        const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
        const hits = [];
        while (walker.nextNode()) {
            if (/^\s*Paper:/m.test(walker.currentNode.data)) hits.push(walker.currentNode);
        }
        hits.forEach(node => {
            const parts = node.data.split('\n').map(line =>
                PAPER.test(line) ? makePaper(emphasis(escape(line))) : document.createTextNode(line + '\n'));
            node.replaceWith(...parts);
            parts.forEach(n => n.nodeType === Node.ELEMENT_NODE && place(n));
        });
    }

    global.TalkHelpers = {
        id: 'talk-helpers',
        init(deck) {
            deck.on('ready', () => {
                footnotes(deck);
                papers();
            });
        },
    };
})(window);
