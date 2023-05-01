<script setup>
    const props = defineProps(['posts'])
</script>

<template>
<div class="grid-container">
        <div class="grid-item" v-for="post in posts" :key="post.id" >
            <img v-bind:src="post.photo" alt="..."/>
        </div>
</div>
</template>

<style scoped>
.grid-container {
    display: grid;
    grid-template-columns: auto auto auto;
    margin: auto;
    justify-content: center;
    align-items: center;
    column-gap: 15px;
    row-gap: 15px;
    width: 70%;
}

.grid-container img {
    width: 15vw;
}
</style>