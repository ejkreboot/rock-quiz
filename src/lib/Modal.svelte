<!-- src/lib/Modal.svelte -->
<script>
  import { createEventDispatcher, onMount, onDestroy, tick } from "svelte";
  import { browser } from "$app/environment";

  export let open = false;
  export let title = null;
  export let closeOnEsc = true;
  export let closeOnBackdrop = true;
  export let labelledBy = null;
  export let maxWidth = "800px"; // control dialog width
  
  // New props for dynamic component rendering
  export let component = null;
  export let props = {};

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
        {#if component}
          <svelte:component this={component} {...props} />
        {:else}
          <slot />
        {/if}
      </section>

      <footer class="modal-footer">
        <slot name="footer" />
      </footer>
    </div>
  </div>
{/if}
