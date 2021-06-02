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
      title: 'MOTI ME',
      subtitle: 'Sporočite nam, če ste v svojem okolju zaznali kaj, kar vas moti (okvare, poškodbe, pomanjkljivosti, nepravilnosti …) in menite, da je v pristojnosti MO Maribor, da to reši.',
      type: 'MM'
    }
  }
}

</script>
