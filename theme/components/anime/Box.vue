<style scoped>
.wrapper {
    position: absolute;
}

.box:hover {
    opacity: 100% !important;
}

.box{
    position: relative;
    --border-width: 5px;
    --hue1: 1;
    --hue2: 0.8;
    --hue3: 0.6;
    height: 100%;
    width: 100%;
    /* box-shadow: 3px 3px rgba(0,0,0,0.3); */
    /* opacity: 0%; */
    border-radius: calc(2 * var(--border-width));

    &::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        border-radius: 4px;
        background: linear-gradient(120deg, hsl(calc(360 * var(--hue1)) 100% 50%), hsl(calc(360 * var(--hue2)) 100% 50%), hsl(calc(360 * var(--hue3)) 100% 50%));
        background-size: 300% 300%;
        animation: frame-enter 1s forwards ease-in-out reverse, gradient-animation 2s ease-in-out infinite;
    }
}

@keyframes gradient-animation {
  0% {
    background-position: 15% 0%;
  }
  50% {
    background-position: 85% 100%;
  }
  100% {
    background-position: 15% 0%;
  }
}

@keyframes frame-enter {
  0% {
    clip-path: polygon(0% 100%, 3px 100%, 3px 3px, calc(100% - 3px) 3px, calc(100% - 3px) calc(100% - 3px), 3px calc(100% - 3px), 3px 100%, 100% 100%, 100% 0%, 0% 0%);
  }
  25% {
    clip-path: polygon(0% 100%, 3px 100%, 3px 3px, calc(100% - 3px) 3px, calc(100% - 3px) calc(100% - 3px), calc(100% - 3px) calc(100% - 3px), calc(100% - 3px) 100%, 100% 100%, 100% 0%, 0% 0%);
  }
  50% {
    clip-path: polygon(0% 100%, 3px 100%, 3px 3px, calc(100% - 3px) 3px, calc(100% - 3px) 3px, calc(100% - 3px) 3px, calc(100% - 3px) 3px, calc(100% - 3px) 3px, 100% 0%, 0% 0%);
  }
  75% {
    -webkit-clip-path: polygon(0% 100%, 3px 100%, 3px 3px, 3px 3px, 3px 3px, 3px 3px, 3px 3px, 3px 3px, 3px 0%, 0% 0%);
  }
  100% {
    -webkit-clip-path: polygon(0% 100%, 3px 100%, 3px 100%, 3px 100%, 3px 100%, 3px 100%, 3px 100%, 3px 100%, 3px 100%, 0% 100%);
  }
}

</style>

<script setup lang="ts">
import { computed, onMounted} from 'vue'
import { parseRangeString } from '@slidev/parser/core'

const props = defineProps({
    position: {
        type: String,
        default: "absolute"
    },
    top: {
        type: String,
        default: "50%"
    },
    left: {
        type: String,
        default: "50%"
    },
    hue1: {
        type: Number,
        default: 1,
    },
    hue2: {
        type: Number,
        default: 1,
    },
    hue3: {
        type: Number,
        default: 1,
    },
    lw: {
        type: String,
        default: "3px"
    },
    w: {
        type: String,
        default: "200px",
    },
    h: {
        type: String,
        default: "2.5rem"
    },
    at: {
        type: String
    }
})

const style = computed(()=>{
    let style = {
        "height": props.h,
        "width": props.w,
        "position": props.position,
        "top": props.top,
        "left": props.left,
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

onMounted(()=>{
        var el = document.querySelector(".box")
        if (el){
            el.style.setProperty("--hue1", props.hue1)
            el.style.setProperty("--hue2", props.hue2)
            el.style.setProperty("--hue3", props.hue3)
        }
})

</script>
<template>
    <!-- Box -->
    <div v-if="show" class="wrapper" :style="style">
        <div class="box">&nbsp</div>
    </div>
</template>
