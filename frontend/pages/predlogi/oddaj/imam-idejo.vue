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
      title: 'IMAM IDEJO',
      subtitle: 'Sporočite nam, če imate predlog za izboljšavo ali novost v svojem okolju.',
      type: 'II',
      descriptions: [
        'Na kratko opišite svojo pobudo oziroma predlog? Zakaj ta predlog? Katere izzive /probleme, pomankljivosti, slabosti v skupnosti/ mestu bi z uresničitvijo  vaše pobude rešili?',
        'Kakšen je vaš idejni predlog rešitve, izzivov/problemov, uvedbe izboljšav, izkoriščanja priložnosti? Kaj konkretno predlagate?  Kakšne priložnosti naslavlja?  Kaj bi se z izvedbo vašega predloga izboljšalo? Ali predlog spodbuja povezovanje /sodelovanje ljudi? Krepi njihove sposobnosti za lažje samostojno reševanje izzivov v skupnosti/mestu?',
        'Kako in kje bi realizirali vašo pobudo-idejo? Katere aktivnosti (koraki /postopki, dela, opravila) so potrebni za izvedbo rešitve? Ali se lahko vaša pobuda realizira v nevladnem sektorju (v okviru društev, civilnih pobud ..), kot socialno podjetniški/zadružni/ podjetniški podjem, razvojni projekt v mestu ali kot gospodarski projekt/pobuda? Koga bi pritegnili k sodelovanju?',
        'Ali lahko ocenite vrednost realizacije projekta / ideje (v EUR)?'
      ]
    }
  }
}
</script>

<style scoped lang="scss">

</style>
