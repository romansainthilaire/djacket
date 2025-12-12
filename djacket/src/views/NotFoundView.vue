<template>
  <div class="content">
    <img src="@/assets/img/not-found.png" alt="Page non trouvée" >
    <h1>404</h1>
    <p>La page que vous recherchez n'existe pas.</p>
  </div>
</template>

<style scoped>
.content {
  margin-top: 50px;
  margin-bottom: 80px;
  display: flex;
  align-items: center;
  flex-direction: column;
  text-align: center;
}

img {
  width: 300px;
}

h1 {
  margin-top: 20px;
  font-size: 100px;
  color: var(--color-primary);
}

p {
  font-size: 18px;
}

@media (max-width: 600px) {
  .content {
    margin-top: 30px;
    margin-bottom: 50px;
  }

  img {
    width: 200px;
  }

  h1 {
    margin-top: 15px;
    font-size: 70px;
  }

  p {
    font-size: 15px;
  }
}
</style>
