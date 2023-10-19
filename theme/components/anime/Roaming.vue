<script setup>
import { onMounted } from 'vue'
import { computed} from 'vue'
import { product, makeArr, choice } from '../../tools'

const props = defineProps({
    top: {
        type: String,
        default: "0",
    },
    left: {
        type: String,
        default:"0"
    },
    w: {
        type: String,
        default: "100%"
    },
    h: {
        type: String,
        default: "100%"
    },
    color: {
        type: String,
        default: '#d993dc'
    },
    rx: {
        type: Number,
        default: 200,
    },
    ry: {
        type: Number,
        default:100
    },
    durMin: {
        type: Number,
        default: 5
    },
    durMax: {//动画持续时长
        type: Number,
        default: 10
    },
    z: {
        type: String,
        default: "30"
    }
})

const style = computed(()=>{
    return {
        "top": props.top,
        "left": props.left,
        "width": props.w,
        "height": props.h,
        "z-index": parseInt(props.z)
    }
})

onMounted(()=>{
    var root = document.querySelector(".roaming")
    root.style.color = props.color

    var h = root.clientHeight
    var w = root.clientWidth

    var items = document.querySelectorAll(".roaming li")

    var posx = makeArr(0, w, items.length - 1)
    var posy = makeArr(0, h, items.length - 1)

    var positions = product(posx, posy)
    items.forEach(function(item){
        var pos = choice(positions)
        item.style.left = pos[0] + "px"
        item.style.top = pos[1] + "px"
        item.style.color = props.color

        var duration = props.durMin + Math.random() * props.durMax;
        item.style.animation = `Roaming ${duration}s ease infinite`

        setInterval(function(){
            var dx = (Math.random() - 0.5) * props.rx
            var dy = (Math.random() - 0.5) * props.ry
            item.style.transform = `translateX(${dx}px)`
            item.style.transform += `translateY(${dy}px)`
            item.style.transition = `transform ${duration}s`
        }, duration * 1000)
    })

})
</script>
<style>


@keyframes Roaming {
  0% {
    opacity: 0;
    color: var(--slidev-back-ground-color);
  }

  50% {
    opacity: 1;
    text-shadow: 0 25px 50px rgba(0, 0, 0, 0.75);
  }

  100% {
    opacity: 0;
    color: var(--slidev-back-ground-color);
  }
}

.roaming {
    position: absolute;
    height: 100%;
    width: 100%;
}

.roaming ul {
    list-style-type: none !important;
}
.roaming li {
    position: absolute;
    transform: none;
}

</style>
<template>
    <div class="roaming" :style="style">
        <slot/>
    </div>
</template>
