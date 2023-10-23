<style>
    footer {
        color: #bebebe;
        z-index: 999;
    }
</style>
<script>
import {isPresenter} from '@slidev/client/logic/nav.ts'
import { computed } from 'vue'

document.onkeydown = checkKey;

function checkKey(e) {
    e = e || window.event;
    // console.info("key pressed: " + e.keyCode)

    var search = new URLSearchParams(location.search) 
    var clicks = parseInt(search.get("clicks"))
    // console.info("clicks now is: " + clicks)

    if (e.keyCode == '37') {
        // left right and space
       if (clicks == NaN || clicks <= 1){
            return
       }

       clicks = clicks - 1
    }
    else if (e.keyCode == '39' || e.keyCode == '32'){
        if (clicks == NaN){
            clicks = 1
        }else {
            clicks = clicks + 1
        }
    }

    // scroll to SEC?
    document.querySelectorAll('div.note h1').forEach(function (item) {
        if (item.innerText.toUpperCase().startsWith('SEC' + clicks)) {
            item.scrollIntoView()
        }
    });

}

// const clicks = computed(()=>{
//     var search = new URLSearchParams(location.search) 
//     return search.get("clicks")
// })
</script>
<template>
  <footer class="absolute bottom-0 left-5"><br/><small><SlideCurrentNo/>/<SlidesTotal/></small></footer>
  <footer
    v-if="$slidev.nav.currentLayout !== 'cover'"
    class="absolute bottom-0 right-0 p-2 flex items-center"
  >
    <span class="c-green-4">@quantfans_99(宽粉)</span>
  </footer>
</template>
