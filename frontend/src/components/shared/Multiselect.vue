<template>
    <div class="relative cursor-pointer" ref="rootEl">
        <div
            class="w-full px-4 pt-2 flex border-grey-200"
            :class="{ 'rounded-b-md': !isDropdownOpen && borders, 'rounded-t-md border': borders }"
            @click.stop="toggleDropdown">
            <div class="flex items-center flex-wrap">
                <span
                    class="rounded-xl px-2 leading-none py-1 bg-grey-200 mr-2 text-xs mb-2 whitespace-nowrap"
                    v-for="(item, id) in selectedItems"
                    :key="id"
                    :ref="'tag' + id"
                    :class="{ 'visually-hidden': wrappedItems[id] }">
                    {{ item }}
                </span>
                <span v-show="Object.keys(wrappedItems).length > 0" class="mb-2 text-grey-600">...</span>
            </div>
            <div class="ml-auto flex content-center items-center mb-2">
                <button
                    class="btn-icon rounded-full p-1 flex-none"
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
import { ref } from 'vue'
import { useClickOutside } from './../../composables/useClickOutside.js'

export default {
  name: 'Multiselect',
  components: {
      Icon,
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
    selection: {
        type: Object,
        required: false,
        default: () => ({})
    }
  },
  data () {
      return {
          selectedItems: { ...this.selection },
          wrappedItems: {}
      }
  },
  computed: {
      iconType () {
          return this.isDropdownOpen ? 'chevron-down' : 'chevron-right'
      }
  },
  watch: {
      selection () {
          console.log('setting selection', this.selection)
          this.selectedItems = { ...this.selection }
      },
      selectedItems: {

        handler () {
            this.wrappedItems = {}
            this.$nextTick(() => {
                this.hideWrappedElements()
            })
        },
        deep: true
      }
  },
  methods: {
      hideWrappedElements () {
        const elements = []
        Object.keys(this.selectedItems).forEach(id => {
            elements.push({ el: this.$refs['tag' + id], id })
        })
        let previousTop = null
        elements.forEach(item => {
            const { top } = item.el.getBoundingClientRect()
            if (previousTop && top > previousTop) {
                this.wrappedItems[item.id] = true
            } else {
                previousTop = top
            }
        })
      },
      toggleDropdown () {
          if (!this.isDropdownOpen) {
              this.isDropdownOpen = true
              this.registerClickEvent()
          } else if (this.isDropdownOpen) {
              this.isDropdownOpen = false
              this.unregisterClickEvent()
          }
      },
      toggleSelection (id) {
          if (this.selectedItems[id]) {
              delete this.selectedItems[id]
          } else if (!this.selectedItems[id]) {
              this.selectedItems[id] = this.items[id]
          }
          this.$emit('selection-changed', { ...this.selectedItems })
      }
  },
  mounted () {
      this.$nextTick(() => {
          this.hideWrappedElements()
      })
  },
  setup () {
    const rootEl = ref(null)
    const isDropdownOpen = ref(false)
    const { registerClickEvent, unregisterClickEvent } = useClickOutside(rootEl, isDropdownOpen)

    return {
        isDropdownOpen,
        rootEl,
        registerClickEvent,
        unregisterClickEvent
    }
  }
}
</script>