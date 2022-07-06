<template>
  <div class="pagination">
    <span v-if="active > 2" class="page" @click="goToPage(1)">1</span>
    <span v-if="active > 3" class="dots">...</span>
    <span v-if="active - 1 > 0" @click="goToPage(active - 1)">{{ active - 1 }}</span>
    <span class="active">{{ active }}</span>
    <span v-if="active + 1 < maxPage" @click="goToPage(active + 1)">{{ active + 1 }}</span>
    <span v-if="maxPage - active > 2" class="dots">...</span>
    <span v-if="active < maxPage" @click="goToPage(maxPage)">{{ maxPage }}</span>
  </div>
</template>

<script>
export default {
  props: {
    active: {
      type: Number,
      default: 1
    },
    maxPage: {
      type: Number,
      default: 1
    }
  },
  data () {
    return {
    }
  },
  methods: {
    goToPage (p) {
      this.$emit('go-to-page', p)
    }
  }
}
</script>

<style scoped lang="scss">
.pagination {
  padding: 20px 0;
  display: flex;
  justify-content: center;

  span {
    width: 25px;
    height: 25px;
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 3px;
    border-radius: 50%;
    font-size: 14px;
    font-weight: 500;
    transition: color 0.15s ease-in-out, background-color 0.15s ease-in-out, border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;

    &.active {
      background-color: #1a365d;
      color: white;
      box-shadow: 2px 2px 5px #d3d7df, -2px -2px 5px #ffffff;
    }

    &:not(.dots):hover {
      background-color: #ef7782;
      color: black;
      box-shadow: 2px 2px 5px #d3d7df, -2px -2px 5px #ffffff;
      cursor: pointer;
    }
  }
}
</style>
