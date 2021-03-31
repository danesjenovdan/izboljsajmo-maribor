<template>
  <NewInitiative
    :title="title"
    :subtitle="subtitle"
    :type="type"
    :descriptions="descriptions"
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
      type: 'ZM',
      descriptions: [
        'Kaj vas zanima? Vaše vprašanje naj bo jasno in nedvoumno; če je potrebno in če je mogoče, na kratko opišite okoliščine, na katere se nanaša vaše vprašanje. Tako vam bomo lažje podali kvaliteten in konkreten odgovor.'
      ]
    }
  }
}
</script>

<style scoped lang="scss">

</style>
