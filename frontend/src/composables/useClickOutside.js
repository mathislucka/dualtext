function useClickOutside (templateRef, hasClickedInside) {
    function registerClickEvent () {
        document.body.addEventListener('click', toggleOutsideClick)
    }

    function unregisterClickEvent () {
        document.body.removeEventListener('click', toggleOutsideClick)
    }

    function toggleOutsideClick (e) {
        if (!templateRef.value.contains(e.target)) {
            hasClickedInside.value = false
            unregisterClickEvent()
        }
    }

    return {
        registerClickEvent,
        unregisterClickEvent,
        hasClickedInside
    }
}

export { useClickOutside }