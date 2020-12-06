<template>
    <div class="relative cursor-pointer" ref="rootEl">
        <div
            class="w-full px-4 pt-2 flex border-grey-200"
            :class="{ 'rounded-b-md': !isDropdownOpen && borders, 'rounded-t-md border': borders }"
            @click.stop="toggleDropdown">
            <div class="flex flex-wrap items-center">
                <span
                    class="rounded-xl px-2 leading-none py-1 bg-grey-200 mr-2 text-xs mb-2"
                    v-for="(item, id) in selectedItems"
                    :key="id">
                    {{ item }}
                </span>
            </div>
            <div class="ml-auto flex content-center items-center mb-2">
                <button
                    class="text-blue-500 outline-none focus:outline-none hover:text-blue-700 hover:bg-grey-200 rounded-full p-1 flex-none"
                    @click.stop.prevent="toggleDropdown"><icon :icon="iconType" :width="16" :height="16" /></button>
            </div>
        </div>
        <div
            class="w-full absolute flex flex-col px-4 py-2 bg-white z-10 border-grey-200 shadow"
            :class="{ 'border-l border-r rounded-b-md border-b': borders }"
            v-if="isDropdownOpen">
            <div v-for="(item, id) in items" :key="item" class="hover:bg-blue-100 cursor-pointer" @click.stop="toggleSelection(id)">
                <input type="checkbox" class="mr-2" @click.stop="toggleSelection(id)" :checked="selectedItems[id]">
                <label :for="item">{{ item }}</label>
            </div>
        </div>
    </div>
</template>

<script>
import Icon from './Icon.vue'
export default {
  name: 'Multiselect',
  components: {
      Icon
  },
  props: {
    borders: {
        type: Boolean,
        required: false,
        default: true
    },
    items: {
        type: Object,
        required: false,
        default: () => ({})
    },
    selection: {}
  },
  data () {
      return {
          isDropdownOpen: false,
          selectedItems: {}
      }
  },
  computed: {
      iconType () {
          return this.isDropdownOpen ? 'chevron-down' : 'chevron-right'
      }
  },
  watch: {
      selection () {
          this.selectedItems = this.selection
      }
  },
  methods: {
      closeOnClick (e) {
          console.log(e)
          console.log(this.$refs.rootEl)
          if (!this.$refs.rootEl.contains(e.target)) {
              this.isDropdownOpen = false
              document.body.removeEventListener('click', this.closeOnClick)
          }
      },
      toggleDropdown () {
          if (this.isDropdownOpen) {
              this.isDropdownOpen = false
          } else if (!this.isDropdownOpen) {
              this.isDropdownOpen = true
              document.body.addEventListener('click', this.closeOnClick)
          }
      },
      toggleSelection (id) {
          if (this.selectedItems[id]) {
              delete this.selectedItems[id]
          } else if (!this.selectedItems[id]) {
              this.selectedItems[id] = this.items[id]
          }
      }
  }
}
</script>