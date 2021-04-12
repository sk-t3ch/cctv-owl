<template>
  <v-app>
    <v-app-bar
      app
      color="black" 
    >
     <v-toolbar-title class="display-2 font-weight-bold secondary--text mr-4">CCTV OWL</v-toolbar-title>
      <v-text-field
        class="mt-7"
        label="Owl URL"
        dark
        v-model="piUrl"
        rounded
        outlined
        :append-icon="piUrlSet ? 'mdi-pencil' : 'mdi-check'"
        @click:append="piUrlSet = !piUrlSet"
        :readonly="piUrlSet"
        placeholder="`http://raspberrypi.local:5000`"
      >
      </v-text-field>
    </v-app-bar>
    <v-main class="secondary">
      <OwlView :pi-url="piUrl"/>
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
    OwlView,
  },

  data: () => ({
    //
  }),
};
</script>
