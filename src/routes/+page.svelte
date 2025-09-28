<script>
  import { onMount } from 'svelte';
  import Svelecte from 'svelecte';
  import Modal from '$lib/Modal.svelte';
  import RockInfo from '$lib/RockInfo.svelte';
  import rock_defs from '$lib/rock_defs.json';
  let show = false;

  /** @type {Record<string,string[]>} */
  let manifest = {};
  let classes = [];
  let current = null;      // { url, label }
  let revealed = false;
  let selected = []
  let deck = [];           // fixed practice set = up to 5 per class
  let drawPile = [];       // shuffled copy we draw from (no repeats)
  let selectedList = [];            // <- Svelecte's current selection (array)
  let ready = false;       // flips true after manifest loads

  const PER_CLASS = 5;

  onMount(async () => {
    const res = await fetch("/rocks-manifest.json");
    manifest = await res.json();
    classes = Object.keys(manifest).sort((a, b) => a.localeCompare(b));

    // NEW: load credits
    try {
      const c = await fetch("/rocks/credits.json");
      const items = await c.json();
      items.forEach(({ file, url }) => {
        creditsMap.set((file || "").replace(/^\/+/, ""), url);
      });
    } catch (e) {
      console.warn("credits.json not found or invalid:", e);
    }

    ready = true;
    buildPracticeDeck();
    nextImage();
  });

  function onSelectionChange() {
    console.log("changed    ")
    // Force a new array reference so Svelte definitely reacts
    selectedList = Array.isArray(selectedList) ? [...selectedList] : [];
    rebuildFromSelection();
  }


  function sampleUpTo(arr, n) {
    // partial Fisher–Yates: sample n without replacement
    const a = arr.slice();
    const k = Math.min(n, a.length);
    for (let i = 0; i < k; i++) {
      const j = i + Math.floor(Math.random() * (a.length - i));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a.slice(0, k);
  }

  function shuffleInPlace(a) {
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  }

function buildPracticeDeck(labels = classes) {
  const tmp = [];
  for (const label of labels.sort((a,b)=>a.localeCompare(b))) {
    const imgs = manifest[label] ?? [];
    const picks = sampleUpTo(imgs, PER_CLASS);
    for (const url of picks) tmp.push({ url, label });
  }
  deck = tmp;
  console.log(deck);
  drawPile = shuffleInPlace(deck.slice());
}

  function chosenLabels() {
    return (selectedList?.length ? selectedList : classes)
      .filter(lbl => (manifest[lbl]?.length ?? 0) > 0)
      .sort((a,b)=> a.localeCompare(b));
  }

  function reshuffleDeck() {
    buildPracticeDeck(chosenLabels());   // <-- use filter
    current = null;
    revealed = false;
    nextImage();
  }

  function rebuildFromSelection() {
    if (!ready) return;
    buildPracticeDeck(chosenLabels());   // keep these in sync
    current = null;
    revealed = false;
    nextImage();
  }

  function nextImage() {
    if (!drawPile.length) {
      drawPile = shuffleInPlace(deck.slice());
    }
    const card = drawPile.pop();
    if (!card) return;
    current = card;
    revealed = false;

    // NEW: look up credit for this image
    const key = keyFromImageURL(current.url);
    const url = creditsMap.get(key) || null;
    creditURL = url;
    creditHost = url ? new URL(url).hostname.replace(/^www\./, "") : null;
  }

  function reveal() {
    revealed = true;
    bind:selected
  }

  let creditURL = null;     // source link for current image
  let creditHost = null;    // pretty host text (e.g., geologysuperstore.com)
  let creditsMap = new Map();

  const ROCKS_PREFIX = "/rocks/";

  // normalize "/rocks/Andesite/Andesite_001.png?x=y" -> "Andesite/Andesite_001.png"
  function keyFromImageURL(u) {
    const clean = (u || "").split("?")[0].split("#")[0];
    const idx = clean.lastIndexOf(ROCKS_PREFIX);
    const tail = idx !== -1 ? clean.slice(idx + ROCKS_PREFIX.length) : clean.replace(/^\//, "");
    return tail;
  }

  // 18×18, rounded box. Strokes use currentColor so you can style via CSS.
  const svg_empty = `
  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18"
      viewBox="0 0 18 18" aria-hidden="true" focusable="false">
    <rect x="2.25" y="2.25" width="13.5" height="13.5" rx="2.5" ry="2.5"
          fill="none" stroke="currentColor" stroke-width="1.5"/>
  </svg>`;

  const svg_checked = `
  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18"
      viewBox="0 0 18 18" aria-hidden="true" focusable="false">
    <rect x="2.25" y="2.25" width="13.5" height="13.5" rx="2.5" ry="2.5"
          fill="none" stroke="currentColor" stroke-width="1.5"/>
    <path d="M5.2 9.4l2.3 2.3L12.8 6.6"
          fill="none" stroke="currentColor" stroke-width="2"
          stroke-linecap="round" stroke-linejoin="round"/>
  </svg>`;

  function svgRenderer(opt, _isSelected, _input) {
    return `<div class="sv-inlined">
      ${opt.$selected ? svg_checked : svg_empty}
      <span>${opt.text}</span>
    </div>`;
  }

</script>


<svelte:head>
<!-- Google Fonts -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<!-- Rubik Distressed for headings; Quicksand for body -->
<link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600;700&family=Rubik+Distressed&display=swap" rel="stylesheet">
</svelte:head>

<style>
    :root {
        --bg: #fafafa;
        --ink: #222;
        --muted: #6a6a6a;
        --title: #c73d01;    /* requested */
        --accent: #85b7b6;   /* requested */
        --card-bg: #f7f7f7;
        --radius: 14px;
        --shadow: 0 8px 24px rgba(0,0,0,0.12);
    }

    :global {
      /* Align icon + label in each option row */
      .sv-inlined {
        display: inline-flex;
        align-items: center;
        gap: 8px;
      }

      /* Slightly dim the boxes; they inherit text color (currentColor) */
      .sv-inlined svg {
        display: block;
        color: #475569; /* tweak or remove to inherit ambient color */
      }

      /* Optional: stronger color when the option is selected (Svelecte adds .selected) */
      .svelecte .option.selected .sv-inlined svg {
        color: #0ea5e9; /* your accent */
      }
    }
    
    h1 {
        font-family: 'Rubik Distressed', system-ui, sans-serif;
        font-size: clamp(1.8rem, 2.2vw + 1rem, 2.6rem);
        margin: 0 0 1rem 0;
        letter-spacing: 0.5px;
        color: var(--title);
        text-shadow: 0 1px 0 rgba(0,0,0,0.03);
    }
    
    .btn {
        appearance: none;
        border: 1px solid color-mix(in srgb, var(--accent) 45%, #ccc 55%);
        background: white;
        color: var(--ink);
        padding: .55rem .85rem;
        border-radius: 10px;
        font-weight: 600;
        font-size: clamp(0.5rem, 2.5vw, 1rem);
        cursor: pointer;
        transition: transform .04s ease, box-shadow .15s ease, border-color .15s ease, background .15s ease;
    }

    .btn:hover {
        border-color: var(--accent);
        background: color-mix(in srgb, var(--accent) 12%, white 88%);
        box-shadow: 0 6px 18px rgba(0,0,0,.08);
    }

    .btn:focus-visible {
        outline: none;
        box-shadow: 0 0 0 3px color-mix(in srgb, var(--accent) 40%, transparent);
    }

    .hint {
        font-size: clamp(0.5rem, 2.5vw, 1rem);
        color: color-mix(in srgb, var(--accent) 50%, var(--muted) 50%);
    }
    
    .wrap {
        max-width: 900px;
        margin: 2rem auto 3rem;
        padding: 0 1rem;
        color: var(--ink);
        font-family: 'Quicksand', system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
    }
    
    .toolbar {
        display: flex;
        flex-wrap: wrap;
        gap: .75rem 1rem;
        align-items: center;
        margin-bottom: 0.75rem;
    }
    
    .answer {
        font-weight: 700;
        font-size: 1.3rem;
        text-transform: capitalize;
        color: var(--accent);
    }

    .right {
        margin-left: auto;
    }
    
    .btn:active { transform: translateY(1px); }
    
    .card {
        width: 900px;
        height: 620px;
        border-radius: 14px;
        overflow: hidden;
        box-shadow: 0 8px 24px rgba(0,0,0,.12);
        background: #f7f7f7;
        margin: 0 auto;
        cursor: pointer;
    }

    @media (max-width: 960px) {
        .card {
            width: min(900px, 100%);
            aspect-ratio: 900 / 620; /* shrinks proportionally on narrow screens */
            height: auto;
        }
    }

    .rock-frame {
        width: 100%;
        height: 100%;
        display: grid;
        place-items: center;
        background: #f7f7f7;
    }

    .rock-frame img {
        width: min(900px, 100%);
        aspect-ratio: 900 / 620;
        object-fit: contain;     /* always letterboxes, never crops */
        object-position: center;
        display: block;
    }

    .credit {
      width: 900px;
      max-width: 100%;
      margin: 8px auto 0;
      text-align: center;
      font-size: clamp(0.75rem, 1.8vw, 0.95rem);
      color: var(--muted);
    }

    .credit a {
      color: var(--accent);
      text-decoration: underline;
    }


</style>


<div class="wrap">
    <h1>Rock ID Practice</h1>
    <div class="toolbar">
    <button class="btn" on:click={nextImage}>Next Image</button>
    {#if !revealed}
        <span class="hint">(Click Image For Answer)</span>
    {:else}
        <div class="answer">{current?.label}</div>
        <button class="btn" on:click={() => (show = true)}>?</button>
    {/if}
    <button class="btn right" on:click={reshuffleDeck}>Shuffle Deck</button>
    </div>

    {#if current}
    <button
        class="card"
        on:click={reveal}
        aria-label="Show the rock type for this image"
        title="Click to reveal"
    >
        <div class="rock-frame">
        <img src={current.url} alt="Rock sample" loading="eager" />
        </div>
    </button>
    {/if}
            {#if creditURL}
          <div class="credit">
            Image may be subject to copyright. Source:
            <a href={creditURL} target="_blank" rel="noopener noreferrer">{creditHost}</a>
          </div>
        {/if}
    <br/>
    <br/>
    <span class="toolbar answer" style="float: left; margin-top: 5px; margin-right: 5px;">Filter rocks: </span>

    <div style="float: left; width: min(300px, 100%);">
    <Svelecte
        multiple 
        options={classes}         
        bind:value={selectedList}
        renderer={svgRenderer} 
        collapseSelection="always" 
        clearable 
        keepSelectionInList={true} 
        onChange={onSelectionChange}  
        searchProps={{skipSort: true}} >
    </Svelecte>
    </div> 

</div>

<!-- Modal -->
 
<Modal bind:open={show} title="Rock type details">
  <RockInfo info={rock_defs.filter(rock => rock.name === current?.label)[0]} />
  <div slot="footer" class="flex justify-end gap-2">
    <button class="px-3 py-1.5 rounded-md bg-zinc-200" on:click={() => (show = false)}>
      Close
    </button>
  </div>
</Modal>

