<!-- src/lib/Modal.svelte -->
<script>
  import { createEventDispatcher, onMount, onDestroy, tick } from "svelte";
  import { browser } from "$app/environment";

  export let open = false;
  export let title = null;
  export let closeOnEsc = true;
  export let closeOnBackdrop = true;
  export let labelledBy = null;
  export let maxWidth = "640px"; // control dialog width

  const dispatch = createEventDispatcher();
  let dialogEl;
  let opener = null;
  let mounted = false;

  const uid = `modal-${Math.random().toString(36).slice(2)}`;
  let headingId;
  $: headingId = labelledBy ?? (title ? `${uid}-title` : null);

  function lockScroll() { if (browser) document.documentElement.style.overflow = "hidden"; }
  function unlockScroll() { if (browser) document.documentElement.style.overflow = ""; }

  const focusable =
    'a[href], button:not([disabled]), textarea, input, select, details, summary, [tabindex]:not([tabindex="-1"])';

  async function trapFocus() {
    if (!browser) return;
    await tick();
    const nodes = dialogEl ? Array.from(dialogEl.querySelectorAll(focusable)) : [];
    (nodes[0] ?? dialogEl)?.focus();
  }

  function handleKeydown(e) {
    if (!open) return;
    if (e.key === "Escape" && closeOnEsc) { e.stopPropagation(); close(); return; }
    if (e.key === "Tab" && browser) {
      const nodes = Array.from(dialogEl?.querySelectorAll(focusable) ?? []);
      if (nodes.length === 0) { e.preventDefault(); dialogEl?.focus(); return; }
      const first = nodes[0], last = nodes[nodes.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  }

  function backdropClick(e) {
    if (!closeOnBackdrop) return;
    if (e.target === e.currentTarget) close();
  }

  function openModal() {
    if (!browser) return;
    opener = document.activeElement ?? null;
    lockScroll();
    dispatch("open");
    trapFocus();
  }

  function close() {
    open = false;
    unlockScroll();
    dispatch("close");
    if (browser) requestAnimationFrame(() => opener?.focus());
  }

  onMount(() => {
    mounted = true;
    const onWinKey = (e) => handleKeydown(e);
    if (browser) window.addEventListener("keydown", onWinKey, true);
    return () => { if (browser) window.removeEventListener("keydown", onWinKey, true); };
  });

  onDestroy(unlockScroll);

  $: if (mounted && open) openModal();
  $: if (mounted && !open) unlockScroll();
</script>

{#if open}
  <div class="modal-backdrop" on:click={backdropClick} aria-hidden="true">
    <div
      bind:this={dialogEl}
      class="modal-dialog"
      role="dialog"
      aria-modal="true"
      aria-labelledby={headingId}
      tabindex="0"
      on:keydown={handleKeydown}
      style={`--modal-max-width:${maxWidth}`}
    >
      <header class="modal-header">
        <div class="modal-header-left">
          {#if title}
            <h2 id={headingId} class="modal-title">{title}</h2>
          {:else}
            <slot name="header" />
          {/if}
        </div>
      </header>

      <section class="modal-body">
        <slot />
      </section>

      <footer class="modal-footer">
        <slot name="footer" />
      </footer>
    </div>
  </div>
{/if}

<style>
  /* ---------- Theming (override from app if you like) ---------- */
  :root {
    --modal-accent: #0ea5e9;          /* highlight color */
    --modal-bg: #ffffff;              /* surface color */
    --modal-fg: #0b0b0b;              /* text color */
    --modal-border: rgba(0,0,0,0.08);
    --modal-shadow-1: 0 10px 20px rgba(0,0,0,0.12);
    --modal-shadow-2: 0 6px 12px rgba(0,0,0,0.08);
    --modal-radius: 14px;
  }

  /* ---------- Backdrop / centering ---------- */
  .modal-backdrop {
    position: fixed;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 16px;
    background: rgba(0, 0, 0, 0.45);
    z-index: 1000;
    backdrop-filter: blur(2px);
    animation: modal-fade 140ms ease-out;
  }

  /* ---------- Dialog card ---------- */
  .modal-dialog {
    width: 100%;
    max-width: var(--modal-max-width, 640px);
    max-height: 85vh;
    overflow: auto;
    border-radius: var(--modal-radius);
    background: var(--modal-bg);
    color: var(--modal-fg);
    border: 1px solid var(--modal-border);
    box-shadow: var(--modal-shadow-1), var(--modal-shadow-2);
    outline: none;
    animation: modal-pop 180ms cubic-bezier(.2,.8,.2,1);
    font-family: "Quicksand", system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
  }

  /* ---------- Header ---------- */
  .modal-header {
    position: sticky;
    top: 0;
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 14px 18px;
    background:
      linear-gradient(0deg, rgba(255,255,255,0.85), rgba(255,255,255,0.85));
    border-bottom: 1px solid var(--modal-border);
    backdrop-filter: blur(2px);
  }
  .modal-title {
    margin: 0;
    flex: 1;
    min-width: 0;
    font-family: "Rubik Distressed", "Quicksand", system-ui, sans-serif;
    color: #bd2100;
    font-size: clamp(20px, 2.2vw, 24px);
    line-height: 1.25;
    letter-spacing: 0.2px;
  }

  /* ---------- Close button ---------- */
  .modal-close {
    border: 0;
    background: transparent;
    inline-size: 34px;
    block-size: 34px;
    display: grid;
    place-items: center;
    border-radius: 999px;
    cursor: pointer;
    color: inherit;
  }
  .modal-close:hover { background: rgba(2, 132, 199, 0.08); }
  .modal-close:focus-visible {
    outline: 2px solid var(--modal-accent);
    outline-offset: 2px;
  }

  /* ---------- Body & footer ---------- */
  .modal-body  { padding: 18px; line-height: 1.6; }
  .modal-footer{
    padding: 12px 18px;
    border-top: 1px solid var(--modal-border);
    display: flex;
    gap: 8px;
    justify-content: flex-end;
  }

  /* Buttons you place in the footer (optional helper) */
  .modal-btn {
    border: 1px solid var(--modal-border);
    background: #f6f7f9;
    color: inherit;
    padding: 8px 12px;
    border-radius: 10px;
    cursor: pointer;
  }
  .modal-btn.primary {
    background: var(--modal-accent);
    border-color: transparent;
    color: #fff;
  }
  .modal-btn:hover { filter: brightness(0.98); }
  .modal-btn:focus-visible {
    outline: 2px solid var(--modal-accent);
    outline-offset: 2px;
  }

  /* ---------- Pretty <pre> for JSON ---------- */
  .modal-body pre {
    margin: 0;
    padding: 12px 14px;
    background: #0f172a10;         /* subtle slate tint */
    border: 1px solid var(--modal-border);
    border-radius: 10px;
    overflow: auto;
    font: 500 14px/1.5 ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
    tab-size: 2;
    white-space: pre;               /* keep formatting from JSON.stringify */
  }

  /* ---------- Dark mode ---------- */
  @media (prefers-color-scheme: dark) {
    :root {
      --modal-bg: #0f1115;
      --modal-fg: #e5e7eb;
      --modal-border: rgba(255,255,255,0.12);
      --modal-shadow-1: 0 14px 28px rgba(0,0,0,0.55);
      --modal-shadow-2: 0 10px 10px rgba(0,0,0,0.35);
    }
    .modal-close:hover { background: rgba(255,255,255,0.06); }
    .modal-header { background: linear-gradient(0deg, rgba(15,17,21,0.9), rgba(15,17,21,0.9)); }
    .modal-body pre { background: #ffffff0f; }
  }

  /* ---------- Motion ---------- */
  @keyframes modal-fade { from { opacity: 0; } to { opacity: 1; } }
  @keyframes modal-pop  {
    from { transform: translateY(6px) scale(0.98); opacity: 0.96; }
    to   { transform: translateY(0)   scale(1);     opacity: 1; }
  }
  @media (prefers-reduced-motion: reduce) {
    .modal-backdrop, .modal-dialog { animation: none !important; }
  }
</style>
