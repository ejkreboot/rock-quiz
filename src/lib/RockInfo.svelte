<!-- src/lib/RockInfo.svelte -->
<script>
  // Props
  export let info = {};              // { name, type, subtype, texture, commonColors, diagnostics, confusedWith }
  export let showHeader = false;     // set true if you want a local title (Modal can already show a title)

  // Field order & labels
  const order = [
    "type",
    "subtype",
    "texture",
    "commonColors",
    "diagnostics",
    "confusedWith"
  ];
  const labels = {
    type: "Type",
    subtype: "Subtype",
    texture: "Texture",
    commonColors: "Common colors",
    diagnostics: "Diagnostics",
    confusedWith: "Often confused with"
  };

  // Helpers
  const splitList = (v) =>
    typeof v === "string" ? v.split(",").map((s) => s.trim()).filter(Boolean) : [];

  const typeClass = (t = "") => {
    t = t.toLowerCase();
    if (t.startsWith("igneous")) return "is-igneous";
    if (t.startsWith("sedimentary")) return "is-sedimentary";
    if (t.startsWith("metamorphic")) return "is-metamorphic";
    return "";
  };
</script>

<section class="ri-card" aria-label="Rock information">
  {#if showHeader}
    <h3 class="ri-title">{info?.name ?? "Rock"}</h3>
  {/if}

  <dl class="ri-grid">
    {#each order as key}
      {#if info?.[key]}
        <dt class="ri-label">{labels[key]}</dt>
        <dd class="ri-value">
          {#if key === "type"}
            <span class="chip {typeClass(info.type)}">{info.type}</span>
          {:else}
            <p class="ri-text">{info[key]}</p>
          {/if}
        </dd>
      {/if}
    {/each}
  </dl>

  <slot name="extra" />
</section>

<style>
  /* Theme tokens (tweak in your app if desired) */
  :root {
    --ri-bg: #ffffff;
    --ri-fg: #0b0b0b;
    --ri-border: rgba(0,0,0,0.08);
    --ri-muted: #6b7280;
    --ri-accent: #0ea5e9;
    --ri-radius: 14px;

    --igneous: #ef6c00;
    --sedimentary: #b45309;
    --metamorphic: #7c3aed;
  }

  .ri-card {
    background: var(--ri-bg);
    color: var(--ri-fg);
    border: 1px solid var(--ri-border);
    border-radius: var(--ri-radius);
    box-shadow:
      0 10px 20px rgba(0,0,0,0.12),
      0 6px 12px rgba(0,0,0,0.08);
    padding: 16px 18px;
    text-transform: capitalize;
    font-family: "Quicksand", system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
  }

  .ri-title {
    margin: 0 0 8px 0;
    font-family: "Rubik Distressed", "Quicksand", system-ui, sans-serif;
    font-size: clamp(20px, 2.2vw, 24px);
    line-height: 1.25;
    letter-spacing: .2px;
  }

  .ri-grid {
    display: grid;
    grid-template-columns: 180px minmax(0, 1fr);
    column-gap: 18px;
    row-gap: 12px;
  }

  /* Labels */
  .ri-label {
    text-transform: uppercase;
    margin-left: auto;
    margin-top: 5px;
    align-self: start;
    color: #72abaa;
    font-size: 0.7rem;
    letter-spacing: .25px;
    white-space: nowrap;
  }

  /* Values */
  .ri-value { margin: 0; }
  .ri-text  { margin: 0; line-height: 1.6; }

  /* Chips */
  .chip {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 999px;
    border: 1px solid var(--ri-border);
    background: #f6f7f9;
    font-size: 0.9rem;
    white-space: nowrap;
  }
  .chip-list { display: flex; flex-wrap: wrap; gap: 6px; }

  /* Type-specific chip coloring */
  .chip.is-igneous     { background: color-mix(in srgb, var(--igneous) 16%, white); border-color: color-mix(in srgb, var(--igneous) 40%, white); }
  .chip.is-sedimentary { background: color-mix(in srgb, var(--sedimentary) 14%, white); border-color: color-mix(in srgb, var(--sedimentary) 38%, white); }
  .chip.is-metamorphic { background: color-mix(in srgb, var(--metamorphic) 16%, white); border-color: color-mix(in srgb, var(--metamorphic) 40%, white); color: #2d1b46; }

  /* Ghost chips for 'confused with' */
  .chip-ghost { background: transparent; }

  /* Small screens: stack to single column */
  @media (max-width: 560px) {
    .ri-grid { grid-template-columns: 1fr; }
    .ri-label { margin-left: 0px; font-weight: 600; margin-bottom: -10px; }

  }

  /* Dark mode (optional) */
  @media (prefers-color-scheme: dark) {
    :root {
      --ri-bg: #0f1115;
      --ri-fg: #e5e7eb;
      --ri-border: rgba(255,255,255,0.12);
      --ri-muted: #9aa3b2;
    }
    .ri-card {
      box-shadow:
        0 14px 28px rgba(0,0,0,0.55),
        0 10px 10px rgba(0,0,0,0.35);
    }
    .chip { background: rgba(255,255,255,0.06); }
  }
</style>
