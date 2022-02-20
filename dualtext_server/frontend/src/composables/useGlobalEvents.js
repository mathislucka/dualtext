import { onMounted, onUnmounted } from 'vue'

function useGlobalEvents (eventType, callback) {
    const body = document.getElementsByTagName('BODY')[0]
    onMounted(() => {
        body.addEventListener(eventType, callback)
    })

    onUnmounted(() => {
        body.removeEventListener(eventType, callback)
    })

    return () => {
        body.removeEventListener(eventType, click)
    }
}

export { useGlobalEvents }