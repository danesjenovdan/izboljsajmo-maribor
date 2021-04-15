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

/*
descriptions: [
        'Na kratko opišite, kaj vas moti. Zakaj? Če je mogoče, opišite svojo izkušnje, da nam pomagate bolje razumeti vašo pripombo.',
        'Kako bi lahko to, kar vas moti, popravili?'
      ]
*/
</script>

<style scoped lang="scss">

</style>
