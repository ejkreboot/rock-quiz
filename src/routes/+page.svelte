<script>
  import { onMount } from 'svelte';
  import Svelecte from 'svelecte';

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
    const res = await fetch('/rocks-manifest.json');
    manifest = await res.json();
    classes = Object.keys(manifest).sort((a, b) => a.localeCompare(b));
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

  function rebuildFromSelection() {
    if (!ready) return;
    // Use the selected list (or all classes if nothing chosen)
    const chosen = (selectedList.length ? selectedList : classes)
      .filter(lbl => (manifest[lbl]?.length ?? 0) > 0)
      .sort((a,b)=>a.localeCompare(b));
    buildPracticeDeck(chosen);
    current = null;
    revealed = false;
      nextImage();

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

  function reshuffleDeck() {
    // Re-sample new practice set for variety
    buildPracticeDeck();
    current = null;
    revealed = false;
    nextImage();
  }

  function nextImage() {
    if (!drawPile.length) {
      // deck exhausted: reshuffle the same deck (or call buildPracticeDeck() if you prefer fresh picks)
      drawPile = shuffleInPlace(deck.slice());
    }
    const card = drawPile.pop();
    if (!card) return;
    current = card;
    revealed = false;
  }

  function reveal() {
    revealed = true;
    bind:selected
  }

  function svgRenderer(opt, isSelected, _input) {
    return `<div class="inlined">${opt.$selected ? svg_checked : svg_empty}<span>${opt.text}</span></div>`;
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


</style>


<div class="wrap">
    <h1>Rock ID Practice</h1>
    <div class="toolbar">
    <button class="btn" on:click={nextImage}>Next Image</button>
    {#if !revealed}
        <span class="hint">(Click Image For Answer)</span>
    {:else}
        <div class="answer">{current?.label}</div>
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
    <br/>
    <br/>
    <span class="toolbar answer" style="float: left; margin-top: 5px; margin-right: 5px;">Filter rocks: </span>
    <Svelecte style="float: left;"
        options={classes}         
        bind:value={selectedList}
        multiple
        clearable
        keepSelectionInList
        placeholder="Choose rock types…"
        onChange={onSelectionChange}  
    />

</div>
