<template>
  <div>
    <h1>Pozabljeno geslo</h1>
    <RestorePassword />
  </div>
</template>

<script>
import RestorePassword from '~/components/forms/RestorePassword'

export default {
  components: { RestorePassword },
  layout: 'login'
}
</script>

<style scoped lang="scss">

</style>
