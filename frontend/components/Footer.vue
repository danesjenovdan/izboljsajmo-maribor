<template>
  <b-container fluid>
    <b-row class="footer">
      <NuxtLink to="/pogoji-uporabe">
        Pogoji uporabe
      </NuxtLink>
    </b-row>
  </b-container>
</template>

<script>
export default {
}
</script>

<style scoped lang="scss">
.footer {
  padding: 1rem 2rem;
  background-color: #1a365d;
  box-shadow: 3px 3px 7px #d4d9e1, -3px -3px 7px #ffffff;

  a {
    color: #f8f8f8;

    &:hover {
      text-decoration: none;
      color: #ef7782;
    }
  }
}
</style>
