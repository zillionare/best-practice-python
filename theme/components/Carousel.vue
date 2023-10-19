<script setup>
import { onMounted } from 'vue'
import { computed} from 'vue'

const props = defineProps({
    n: {
        type: String,
        default: "5"
    },
    circle: {
        type: Boolean,
        default: true
    }
})

function set_nav(){
    const slides = document.querySelectorAll(".slide");

    // loop through slides and set each slides translateX property to index * 100% 
    slides.forEach((slide, indx) => {
    slide.style.transform = `translateX(${indx * 100}%)`;
    });

    // current slide counter
    let curSlide = 0;

    // select next slide button
    const nextSlide = document.querySelector(".btn-next");

    // add event listener and next slide functionality
    nextSlide.addEventListener("click", function () {
        curSlide++
        curSlide = Math.min(props.n, curSlide)
        console.info(curSlide)

        slides.forEach((slide, indx) => {
            slide.style.transform = `translateX(${100 * (indx - curSlide)}%)`;
            if (indx == curSlide){
                slide.style.transform += "scale(1.5)"
            }
            if (props.n == 5 && Math.abs(indx - curSlide) == 1){
                slide.style.transform += "scale(1.2)"
            }
        });
    });

    const prevSlide = document.querySelector(".btn-prev");

    // add event listener and next slide functionality
    prevSlide.addEventListener("click", function () {
        curSlide--
        curSlide = Math.max(0, curSlide)
        console.info(curSlide)

        slides.forEach((slide, indx) => {
            slide.style.transform = `translateX(${100 * (indx - curSlide)}%)`;
            if (indx == curSlide){
                slide.style.transform += "scale(1.5)"
            }
            if (props.n == 5 && Math.abs(indx - curSlide) == 1){
                slide.style.transform += "scale(1.2)"
            }
        });
    });
}
onMounted(()=>{
    var el = document.querySelector(".carousel")
    var w = el.clientWidth 

    var imgWidth = w * 0.8 / props.n

    var images = document.querySelectorAll(".carousel p img")
    //将img和alt包装起来

    var j = 0
    for (var img of images){
        img.style.width = `${imgWidth}px`
        img.style.height = `${imgWidth}px`
        if (props.circle)
            img.style.borderRadius = "50%"

        var fragment = document.createDocumentFragment();
        var div = document.createElement('div')
        div.setAttribute("id", `${j}`)
        div.setAttribute("class", "slide")
        div.appendChild(img)

        var altNode = document.createElement("span")
        altNode.textContent = img.getAttribute("alt")
        div.appendChild(altNode)
        
        fragment.appendChild(div)
        el.appendChild(fragment)
        j += 1
    }

    //bug 创建了重复的div，只能通过移除的方法
    for (var i = images.length - 1; i >= images.length / 2;i--){
        const el = document.getElementById(`${i}`)
        el.remove();
    }

    set_nav()
})
</script>
<template>
<div class="carousel">
    <slot/>
</div>
<button class="btn btn-next"></button>
<button class="btn btn-prev"></button>
</template>
<style>

.carousel {
  width: 100%;
  max-width: 800px;
  display: flex;
  justify-content: space-around;
  transition: all 0.5s;
}

.carousel div > span {
    margin-top: 20px;
    display: block;
}

.slide {
  transition: all 0.5s;
}

.btn {
  position: absolute;
  width: 40px;
  height: 40px;
  padding: 10px;
  border: none;
  border-radius: 50%;
  z-index: 10px;
  cursor: pointer;
  background-color: #fff;
  font-size: 18px;
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
