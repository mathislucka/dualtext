<template>
    <div class="shadow p-4 bg-white">
        <div class="w-full mb-4">
            <slot name="header" />
        </div>
        <div class="w-full">
            <slot name="content" />
        </div>
    </div>
</template>

<script>
export default {
    name: 'Card'
}
</script>