<template>
  <v-app>
    <v-app-bar
      app
      dark
    >
     <v-toolbar-title class="font-weight-bold mr-4">CCTV OWL {{ $vuetify.breakpoint.name }}</v-toolbar-title>
      <v-text-field
        class="mt-7"
        label="Enter your CCTV OWL URL"
        ref="addressbar"
        dark
        dense
        v-model="piUrl"
        rounded
        outlined
        :append-icon="piUrlSet ? 'mdi-pencil' : 'mdi-check'"
        @click:append="piUrlSet = !piUrlSet"
        @click="piUrlSet = false"
        @keyup.enter="doThing"
        :readonly="piUrlSet"
        placeholder="http://raspberrypi.local:5000"
      >
      </v-text-field>
    </v-app-bar>
    <v-main class="secondary">
      <OwlView :pi-url="piUrl" :pi-url-set="piUrlSet"/>
    </v-main>
    <v-footer app color="black" class="font-weight-bold secondary--text"
      >T3chFlicks</v-footer
    >
  </v-app>
</template>

<script>
import OwlView from "./components/OwlView";

export default {
  name: "App",

  components: {
    OwlView
  },
  methods: {
    doThing(){
      this.piUrlSet = true;
      this.$refs.addressbar.blur()
    }
  },
  mounted() {
    this.$refs.addressbar.focus()
  },
  data() {
    return {
    piUrlSet: false,
    piUrl: null
    //
  }
  },
};
</script>
