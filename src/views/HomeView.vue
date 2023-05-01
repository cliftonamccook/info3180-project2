<script setup>
import { ref } from "vue";
import { RouterLink } from "vue-router";

</script>

<template>
<div class="container">
      <div class="home-img">
        <img src="../assets/home.jpg" alt="">
      </div>
      <div class="login-sec">
        <h2>Photogram</h2>
        <p>Share photos of your favourite moments with friends, family and the world.</p>
        <div class="reg-buttons">
          <button class="register-button"><RouterLink class="nav-link" to="/register">Register</RouterLink></button>
          <button class="login-button"><RouterLink class="nav-link" to="/login">Login</RouterLink></button>
        </div>
      </div>
    </div>
</template>

<style scoped>
    body{
    background: #f5efe6;
  }

  .container{
    display: flex;
    flex-direction: row;
    gap: 1em;
    height: 25em;
    width: 80%;
    margin: 10em auto;
    font-weight: bold;
    justify-content: center;
  }

  h2{
    margin: 2em auto 0 auto;
    border-bottom: 0.5px solid #cdcdcd;
    padding-bottom: 0.5em;
    width: 90%;
  }

  p{
    text-align: left;
    width: 90%;
    margin: 1em auto 3em auto;
  }

  .home-img{
    height: 100%;
    width: 40%;
  }

  .home-img img{
    border-radius: 5px;
    width: 100%;
    height: 100%;
  }

  .login-sec{
    height: 100%;
    width: 40%;
    text-align: center;
    background-color: #ffffff;
    border-radius: 5px;
    border: black solid 1px;
  }

  .reg-buttons{
    display: flex;
    flex-direction: row;
  }

  .reg-buttons button{
    border: none;
    border-radius: 5px;
    height: 2.5em;
    width: 45%;
    margin: 0 auto;
    color: #fff;
    font-weight: bold;
    font-size: 1em;
  }

  .register-button{
    background: rgb(92, 221, 122);
  }

  .login-button{
    background: #6fb4e2;
  }


</style>