<template>
  <footer>
    <div class="content">
      <nav>
        <RouterLink class="nav-link" to="/">Accueil</RouterLink>
        <span>·</span>
        <a class="nav-link" href="https://github.com/romansainthilaire" target="_blank">GitHub</a>
        <span>·</span>
        <a class="nav-link" href="https://www.linkedin.com/in/roman-saint-hilaire-209341b7/" target="_blank">LinkedIn</a>
      </nav>
      <hr>
      <div class="copyright">&copy; 2025 Djacket</div>
    </div>
  </footer>
</template>

<style scoped>
footer {
  display: flex;
  justify-content: center;
  background-color: rgb(0, 0, 140);
  color: white;
  font-size: 15px;
}

.content {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  max-width: 600px;
  padding: 20px;
}

.nav-link {
  color: white;
  text-decoration: none;
  margin: 0 10px;
}

hr {
  width: 100%;
  border: 0;
  border-top: 1px solid white;
  margin: 20px 0;
}
</style>
