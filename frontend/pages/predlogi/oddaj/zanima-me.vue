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
      title: 'ZANIMA ME',
      subtitle: 'Vprašajte, kar vas zanima.',
      type: 'ZM'
    }
  }
}

</script>
