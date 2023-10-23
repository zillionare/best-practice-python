<style>
.ellipse{
    position: absolute;
    border-radius: 50%;
    --border-width: 5px;
    border-width: var(--border-width);
    /* box-shadow: 3px 3px rgba(0,0,0,0.2); */
    /* transition-duration: 1s; */
    animation: glow 1s infinite alternate;
}


@keyframes glow {
  from {
    /* box-shadow: 0 0 var(--border-width) calc(-1 * var(--border-width)) hsl(calc(360 * var(--hue1)) 50% 80%); */
    box-shadow: 0 0 var(--border-width) calc(-1 * var(--border-width))  rgba(0,0,0,0.8);
  }
  to {
    /* box-shadow: 0 0 var(--border-width) var(--border-width) hsl(calc(360 * var(--hue1)) 50% 50%); */
    box-shadow: 0 0 var(--border-width) var(--border-width) rgba(0,0,0,0.2);
    filter: blur(1px);
  }
}
</style>

<script setup lang="ts">
import { computed} from 'vue'

const props = defineProps({
    top: {
        type: String,
        default: "50%"
    },
    left: {
        type: String,
        default: "50%"
    },
    color: {
        type: String,
        default: "#ff0000",
    },
    lw: {
        type: String,
        default: "3px"
    },
    s: {
        type: Number,
        default: 200,
    },    
    at: {
        type: String
    }
})

const style = computed(()=>{
    let style = {
        "height": props.s / 2 + "px",
        "width": props.s + "px",
        "top": props.top,
        "left": props.left,
        "border-color": props.color,
        "border-width": props.lw
    }

    if (props.at){
        style["opacity"] = 0.8
    }
    return style
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
    <!-- Ellipse -->
    <div v-if="show" class="ellipse" :style="style"></div>
</template>
