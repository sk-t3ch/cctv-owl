<template>
  <v-container fill-height fluid>
    <v-row class="text-center">
      <v-col class="mb-4">
        <v-card class="secondary" dark>
          <v-row justify="center">
            <v-col cols="auto">
              <v-card class="ma-2">
                <v-card-title> Labels </v-card-title>
                <v-card-text>
                  <v-select
                    :items="labels"
                    v-model="config['label']"
                  ></v-select>
                </v-card-text>
              </v-card>
              <v-card class="ma-2">
                <v-card-title> Certainty </v-card-title>
                <v-card-text>
                  <v-slider
                    v-model="config['threshold']"
                    thumb-label="always"
                    thumb-color="primary"
                    max="100"
                    min="0"
                  ></v-slider>
                </v-card-text>
              </v-card>
            </v-col>
            <v-spacer />
            <v-col cols="5" class="my-4">
              <v-img
                v-if="piUrlSet && piUrl"
                :src="piUrl + '/video_feed'"
                style="overflow: unset"
              >
                <div class="left"></div>
                <div class="right"></div>
              </v-img>
              <v-img
                v-else
                style="overflow: unset"
                :src="require('../assets/logo.jpg')"
              >
                <div class="left"></div>
                <div class="right"></div>
              </v-img>

            </v-col>
            <v-spacer />
            <v-col cols="auto">
              <v-card class="ma-2">
                <v-card-title> Tracking </v-card-title>
                <v-card-text>
                  <v-select
                    :items="tracking"
                    dark
                    v-model="config['tracking']"
                  ></v-select>
                </v-card-text>
              </v-card>

              <v-card class="ma-2">
                <v-card-title> Actions </v-card-title>
                <v-card-text>
                  <v-checkbox 
                    v-model="config['hoot']"
                    label="Hoot"
                  ></v-checkbox>
                  <v-checkbox
                    v-model="config['alert']"
                    label="Alert"
                  ></v-checkbox>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "OwlView",
  props: ['piUrl'],
  data() {
    return {
      labels: ["person", "bird", "book", "dog", "all"],
      tracking: ["single", "maximise"],
      config: {
        label: "person",
        tracking: "single",
        threshold: 70,
        hoot: false,
        alert: false,
      },
      piUrlSet: true
    };
  },
  watch: {
    config: {
      deep: true,
      handler() {
        console.log("updating config");
        this.updateConfig();
      },
    },
  },
  methods: {
    async updateConfig() {
      const result = await fetch(this.pi_url + "/update_config", {
        method: "POST",
        body: JSON.stringify(this.config),
        headers: {
          "Content-Type": "application/json",
        },
      }).then((resp) => resp.json());
      console.log(result);
    },
  },
};
</script>
<style scoped>
.left,
.right {
  position: relative;
  float: left;
  height: 100%;
  width: 50%;
  z-index: -100;
  margin-top: -5%;
  margin-bottom: -5%;
}
.left:after,
.right:after {
  position: absolute;
  content: "";
  background: black;
  height: calc(110%);
  width: calc(130%);
  border-radius: 25%;
  border: 3px solid white;
}
.left:after {
  right: -15%;
}
.right:after {
  left: -15%;
}
</style>