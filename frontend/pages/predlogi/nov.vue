<template>
  <b-container fluid>
    <b-row class="justify-content-center">
      <b-col cols="12" md="10" lg="6" class="position-relative">
        <Initiative :initiative-type="type"/>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import Initiative from '~/components/forms/Initiative'

export default {
  components: { Initiative },
  middleware: 'auth',
  data () {
    return {}
  },
  computed: {
    type () {
      return this.$route.query.tip
    }
  }
}
</script>
