<template>
  <NewInitiative
    :title="title"
    :subtitle="subtitle"
    :type="type"
  />
</template>

<script>
import NewInitiative from '~/components/NewInitiative'

export default {
  components: { NewInitiative },
  middleware: 'auth',
  data () {
    return {
      title: 'IMAM IDEJO',
      subtitle: 'Sporočite nam, če imate predlog za izboljšavo ali novost v svojem okolju.',
      type: 'II'
    }
  }
}

</script>
