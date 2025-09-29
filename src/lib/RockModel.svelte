<script>
  export let name;
  export let link;
  export let title = "";
  export let author_name = "";
  export let author_url = "";
  export let license = "";
  export let license_url = "";

  const uidFromUrl = (url) => {
    if (!url) return null;
    const m1 = url.match(/\/3d-models\/[^\/]+-([a-z0-9]{32})/i);
    if (m1) return m1[1];
    const m2 = url.match(/\/models\/([a-z0-9]{32})(?:[\/?#]|$)/i);
    if (m2) return m2[1];
    return null;
  };
  const uid = uidFromUrl(link);
  const iframeSrc = uid
    ? `https://sketchfab.com/models/${uid}/embed?autostart=1&ui_theme=dark`
    : `${link}?embed=1`;
</script>

<div style="color: var(--accent); padding-bottom: 0.5rem;">
  Click on image to increase resolution. Drag to rotate, scroll to zoom.
</div>
<div class="model-wrap">
  <div class="frame">
    <iframe
      title={`3D model of ${name}`}
      src={iframeSrc}
      allow="autoplay; fullscreen; xr-spatial-tracking"
      loading="lazy"
    ></iframe>
  </div>

  <div class="attrib">
    <div class="title">{title || name}</div>
    <div class="byline">
      {#if author_name && author_url}
        by <a href={author_url} target="_blank">{author_name}</a>
      {:else if author_name}
        by {author_name}
      {/if}
      on <a href={link} target="_blank">Sketchfab</a>
    </div>
    {#if license}
      <div class="license">
        License:
        {#if license_url}
          <a href={license_url} target="_blank">{license}</a>
        {:else}
          {license}
        {/if}
      </div>
    {/if}
  </div>
</div>

<style>
  .model-wrap {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    width: 100%;
    max-width: 800px;
    margin: 0 auto;
  }
  
  .frame {
    position: relative;
    width: 100%;
    aspect-ratio: 16 / 10;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  }
  
  .frame iframe {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    border: none;
  }
  
  .attrib {
    font-size: 0.875rem;
    color: #6b7280;
    line-height: 1.5;
  }
  
  .title {
    font-weight: 600;
    color: #374151;
    margin-bottom: 0.25rem;
  }
  
  .byline {
    margin-bottom: 0.25rem;
  }
  
  .license {
    font-size: 0.8125rem;
  }
  
  a {
    color: #3b82f6;
    text-decoration: none;
  }
  
  a:hover {
    text-decoration: underline;
  }
  
  @media (max-width: 640px) {
    .model-wrap {
      max-width: 100%;
    }
    
    .frame {
      aspect-ratio: 4 / 3;
    }
    
    .attrib {
      font-size: 0.8125rem;
    }
  }
</style>
