

<script setup>
import { RouterLink } from "vue-router";

const token = localStorage.getItem('token')

if (token) {
  window.location.href = 'explore'
}
</script>

<template>
    <div v-if="token"></div>
    <div class="container" v-else>
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

<style>
  body{
    background: #e5e5e5;
  }

  .container{
    display: flex;
    flex-direction: row;
    gap: 1em;
    height: 25em;
    width: 80%;
    margin: 10em auto;
    font-weight: bold;
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
    background: #fff;
    border-radius: 5px;
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