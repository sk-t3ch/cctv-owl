<template>
  <v-app>
    <v-app-bar app dark color="primary">
      <v-text-field
        class="mt-7"
        color="accent"
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
      <v-btn icon href="https://github.com/sk-t3ch/cctv-owl">
        <v-icon> mdi-github </v-icon>
      </v-btn>
    </v-app-bar>
    <v-main class="primary">
      <OwlView :pi-url="piUrl" :pi-url-set="piUrlSet" />
    </v-main>
    <v-footer app color="secondary">
      <v-spacer />
      <v-col cols="auto" class="text-none">
        <v-btn
          dark
          href="https://t3chflicks.org"
          text
          class="text-none px-1 ml-0 mr-1 elevation-0"
        >
          T3chFlicks </v-btn
        >- A tech focused education and services company
      </v-col>
    </v-footer>
  </v-app>
</template>

<script>
import OwlView from "./components/OwlView";

export default {
  name: "App",

  components: {
    OwlView,
  },
  methods: {
    doThing() {
      this.piUrlSet = true;
      this.$refs.addressbar.blur();
    },
  },
  mounted() {
    this.$refs.addressbar.focus();
  },
  data() {
    return {
      piUrlSet: false,
      piUrl: null,
    };
  }
};
</script>
