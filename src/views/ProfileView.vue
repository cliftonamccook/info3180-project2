<template>
  <div class="about container">
    <h2>About</h2>
    <p>This is an about page.</p>
  </div>
</template>
<script>
const token = localStorage.getItem('token')
if (!token) {
  window.location.href = '/'
}
</script>
<style>
</style>
