<script setup lang="ts">
import { computed } from 'vue'
import { handleBackground } from '../layoutHelper'

const props = defineProps({
  background: {
    default: '/public/desktop.jpg',
  }
})

const style = computed(() => handleBackground(props.background, false))

</script>
<style>
.title {
        position: absolute;
        top: 15%;
        left: 1.5rem;
        width:100%;
        text-align: left;
    }

.title:after {
    content: " ";
    display: block;
    width: 98%;
    position: absolute;
    left: 1vw;
    border-bottom-width: 1px;
    border-bottom-style: solid;
    border-image: linear-gradient(to right, var(--slidev-theme-primary) 20%, white 100%, var(--slidev-theme-primary) 0%) 1;
}

.subtitle {
    position: absolute;
    font-size: smaller;
    top: 80%;
    right: 2rem;
    color: white;
}

.slogan {
    position: absolute;
    font-size: smaller;
    top: 4rem;
    left: 0.5rem;
    font-style: italic;
    font-family: gothic;
    color: white;
    background-color: var(--slidev-theme-secondary);
    border-radius: 0 20px 20px 0;
    padding: 5px 20px 5px 10px;
    border-left: 5px solid black;
}

.mask {
    background-color:  var(--slidev-theme-three);
    opacity: 80%;
    position: absolute;
    width:100%;
    top: 25%;
    height: 40%;
    left:0;
}

.seq {
    position:absolute;
    left: 0.5rem;
    top: 1.5rem;
    font-size: small;
    color: white;
    background-color: var(--slidev-theme-three);
    border-radius: 0 20px 20px 0;
    padding: 5px 20px 5px 10px;
    border-left: 5px solid black;
}
</style>
<template>
<div
class="slidev-layout cover text-center"
:style="style"
>
    <div class="mask">
    <h1 class="my-auto w-full title">
        {{ $slidev.nav.currentRoute.meta.title }}
    </h1>
    <div class="subtitle">
        {{ $slidev.nav.currentRoute.meta.subtitle }}
    </div>
</div>
<div class="slogan">
    {{ $slidev.nav.currentRoute.meta.slogan }}
</div>
<div class="seq">
    {{ $slidev.nav.currentRoute.meta.seq }}
</div>
</div>
</template>
