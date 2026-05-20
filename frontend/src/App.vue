<template>
  <div id="ls-app-root">
    <RouterView />
  </div>
</template>

<style>
html, body, #app, #ls-app-root {
  margin: 0 !important;
  padding: 0 !important;
  width: 100% !important;
  height: 100% !important;
 
  background-color: #0d1117!important; 
  color: #e6edf3 !important;
  overflow-x: hidden;
}


* {
  box-sizing: border-box;
  -webkit-font-smoothing: antialiased;
}
</style>