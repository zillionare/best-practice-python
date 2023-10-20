<script setup>
import { onMounted } from 'vue'
import { computed} from 'vue'

const props = defineProps({
    n: {//必须是奇数
        type: String,
        default: "3",
        required: false
    },
    imgwidth: {
        //必须是px单位
        type: String,
        required: true
    },
    imgheight: {
        type: String,
        required: false
    },
    w: {
        type: String,
        required: false
    },
    circle: {
        type: Boolean,
        default: true
    },
    slides: {
        type: Array,
        required: true
    },
    top: {
        // 容器
        type: String,
        required: false
    },
    left: {
        // 容器
        type: String,
        required: false
    }
})

const all_slides = computed(()=>{
    return props.slides
})


const imgStyle = computed(()=>{
    return {
        width: props.imgwidth,
        height: props.imgheight || props.imgwidth
    }
})

const style = computed(()=>{
    return {
        top: props.top,
        left: props.left,
        width: props.w
    }
})

function calcAndScale(target, cursor){
    var scale = 1
    if (props.n < 5 && target == cursor){
            scale = 1.2
    }else if (props.n > 5){
        if (target == cursor){
            scale = 1.5
        }else if (Math.abs(target-cursor) == 1){
            scale = 1.2
        }
    }

    // console.info(`scale ${target} to ${scale}`)

    //query image and scale
    let img = document.getElementById(`carousel-${target}`)
    if (img == null)
        return

    if (scale == 1.2)
        img.style.border = "3px solid rgba(200,200,200,0.8)"
    else{
        img.style.border = ""
    }
    // img.style.transform = `scale(${scale}) translateY(${(1-scale)*100}%)`
}
function set_nav(){
    const slides = document.querySelectorAll(".slide");
    let total_slides = slides.length / 2

    // current slide counter
    // let curSlide = parseInt(props.n / 2)
    let curSlide = 1

    // loop through slides and set each slides translateX property to index * 100% 
    slides.forEach((slide, indx) => {
        slide.style.transform = `translateX(${indx * 120}%)`;
        calcAndScale(indx, curSlide)
    });

    // select next slide button
    const nextSlide = document.querySelector(".btn-next");

    // add event listener and next slide functionality
    nextSlide.addEventListener("click", function () {
        if (curSlide === total_slides) {
            curSlide = 0
        } else {
            curSlide++;
        }

        console.info(`cur slide is ${curSlide}, ${total_slides - parseInt(props.n / 2)}`)

        slides.forEach((slide, indx) => {
            slide.style.transform = `translateX(${(indx - curSlide + parseInt(props.n / 2)) * 120}%)`;
            calcAndScale(indx, curSlide)
        });
    });

    const prevSlide = document.querySelector(".btn-prev");

    // add event listener and next slide functionality
    prevSlide.addEventListener("click", function () {
        if (curSlide === 0) {
            curSlide = total_slides;
        } else {
            curSlide--;
        }

        slides.forEach((slide, indx) => {
            slide.style.transform = `translateX(${(indx - curSlide + parseInt(props.n / 2)) * 120}%)`;
            calcAndScale(indx, curSlide, slides)
        });
    });
}

const hasCircle = computed(()=>{
    if (props.circle)
        return "circle"
    else
        return ""
})

onMounted(()=>{
    set_nav()
})
</script>
<template>
<div class="carousel" :style="style">
    <div v-for="(item, index) in all_slides" class="slide">
    <div class="img-wrapper"><img :id="'carousel-' + index" :src="item.img" class="img" :class="hasCircle" :style="imgStyle"></div>
    <div class="img-caption">{{ item.caption }}</div>
    </div>
</div>
<button class="btn btn-next"></button>
<button class="btn btn-prev"></button>
</template>
<style>

.carousel {
    position: relative;
    width: 100%;
    max-width: 800px;
    transition: all 1s;
}

.slide {
  transition: all 1s;
  position: absolute;
}


.circle {
    border-radius: 50%;
}

.btn {
  position: absolute;
  width: 100px;
  height: 100px;
  padding: 10px;
  border: none;
  border-radius: 50%;
  z-index: 10px;
  cursor: pointer;
  background-color:grey;
  font-size: 18px;
  opacity: 0.02;
}
.btn:active {
  transform: scale(1.1);
}
.btn-prev {
  top: 45%;
  left: 2%;
}

.btn-next {
  top: 45%;
  right: 2%;
}

</style>
