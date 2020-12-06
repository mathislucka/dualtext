<template>
    <div class="flex">
        <div class="flex items-center w-1/2 mr-4">
            <span class="mr-2 text-xs">Methods:</span>
            <multiselect :items="{'1': 'some tag', '2': 'another', '3': 'this is nice'}" class="w-full" :borders="false" />
        </div>
        <div class="flex items-center w-1/2">
            <span class="mr-2 text-xs">Corpora:</span>
            <multiselect :items="{'1': 'some tag', '2': 'another', '3': 'this is nice', '4': 'lalalalala' }" class="w-full" :borders="false" />
        </div>
    </div>
</template>

<script>
import Multiselect from './Multiselect.vue'
export default {
  name: 'Search',
  components: {
      Multiselect
  },
  props: {
    msg: String
  }
}
</script>