<style>
    footer {
        color: #bebebe;
        z-index: 999;
    }
</style>
<template>
  <footer class="absolute bottom-0 left-5"><br/><small><SlideCurrentNo/>/<SlidesTotal/></small></footer>
  <footer
    v-if="$slidev.nav.currentLayout !== 'cover'"
    class="absolute bottom-0 right-0 p-2 flex items-center"
  >
    <span>@量化风云 @quantfans_99 (宽粉)</span>
  </footer>
</template>
