<!--象演员表一样向上滚动-->
<script setup>
import { onMounted } from 'vue'
import { computed} from 'vue'
import { product, makeArr, choice } from '../../tools'
import { parseRangeString } from '@slidev/parser/core'

const props = defineProps({
  at: {
    required: true
  },
  left: {
    type: String,
    default: "50%"
  },
  textAlign: {
    type: String,
    default: "center"
  },
  color: {
    type: String,
    default: "rgb(20,20,20)"
  },
  z: {
    type: String,
    default: "10"
  },
  fc: {
    type: String,
    default: ""
  }
})

const show = computed(() => {
    var at = props.at
    if (at === undefined){
        return false
    }

    if (typeof(at) === "number") {
        at = String(at)
    }

    var ranges = parseRangeString(10, at)
    if (ranges.includes($slidev.nav.clicks)){
        setTimeout(rock_roll, 100)
        return true
    }else{
        return false
    }
})

const style = computed(()=>{
    var style_ = {
        "color": props.color,
        "left": props.left,
        "text-align": props.textAlign,
        "z-index": parseInt(props.z)
    }

    if (props.fc !== null){
        style_["background"] = props.fc
    }

    return style_
})

function rock_roll(){
    var cast = document.querySelector(".cast")
    if (cast == null){
        return
    }
    var myHeight = cast.clientHeight
    var slideshow = document.getElementById("slideshow")
    var containerHeight  = slideshow.clientHeight
    cast.style.top = `${containerHeight - 20}px`

    var i = containerHeight - 20
    var timer = setInterval(function(){
        i = i - 1
        cast.style.top = `${i}px`

        var arr = document.querySelectorAll(".cast li")

        for (var item of arr){
            var offsetY = item.offsetTop + cast.offsetTop
            if (offsetY < 0 || offsetY > containerHeight)
                continue

            var op = offsetY / containerHeight

            if (op > 1)
                continue
            else if (op > 0.5)
                op = (1-op)
            else if (op < 0)
                continue


            op *= 2

            item.style.opacity = op
        }
        
        if (i <= -myHeight){
            clearInterval(timer)
        }
    }, 10, i)
}
</script>
<style>

@keyframes Fadeout {
  0% {
    opacity: 1;
  }

  100% {
    opacity: 0;
  }
}

@keyframes Fadein {
  0% {
    opacity: 0;
  }

  100% {
    opacity: 1;
  }
}

.cast {
    position: absolute;
}

.cast ul {
    list-style-type: none !important;
}
</style>
<template>
    <div class="cast" v-if="show" :style="style">
        <slot></slot>
    </div>
</template>
