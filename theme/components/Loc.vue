<script setup lang="ts">
import { computed } from 'vue'
import { parseRangeString } from '@slidev/parser/core'

const props = defineProps({
  img: {
    type: String,
  },
  class: {
    type: String,
  },
  w: {
    default: "100%"
  },
  left: {
    default: "0"
  },
  top: {
    default: "0"
  },
  h: {
    default: "100%"
  },
  position: {
    default: "absolute"
  },
  alpha: {
    default: "1"
  },
  padding: {
    default: "0"
  },
  fc: {
    default: "white"
  },
  at: {
    type: String
  },
  z: {
        type:String,
        default:"90"
    }
})

const style = computed(() => {
    var s = {
        "background-image": 'url(' + props.img +')',
        "background-size": "contain",
        "background-repeat": "no-repeat",
        "position": props.position,
        "top": props.top,
        "left": props.left,
        "width": props.w,
        "height": props.h,
        "opacity": props.alpha,
        "padding": props.padding,
        "display": "flex",
        "flex-flow": "column",
        "justify-content": "center",
        "align-items": "center",
        "background-color": props.fc,
        "z-index": parseInt(props.z)
    }
    console.log(s)
    return s
})

const show = computed(() => {
    var at = props.at
    if (at === undefined){
        return true
    }

    if (typeof(at) === "number") {
        at = String(at)
    }

    var ranges = parseRangeString(10, at)
    return ranges.includes($slidev.nav.clicks)
})

</script>
<template>
    <div v-if="show" :style="style"><slot /></div>
</template>
