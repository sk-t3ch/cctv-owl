<template>
  <v-container>
    <v-row class="my-2">
      <v-col cols="12">
        <v-card dark>
        <v-row justify="center"> 
          <v-col cols="12" xs="12" sm="12" md="4" lg="3" xl="2" align-self="center">
            <v-card class="ma-2 elevation-12">
              <v-card-title> Labels </v-card-title>
              <v-card-text>
                <v-select
                  :items="labels"
                  v-model="config['label']"
                ></v-select>
              </v-card-text>
            </v-card>
            <v-card class="ma-2  elevation-12">
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
          <v-col cols="12"  xs="12" sm="12" md="4" lg="6" xl="8" class="my-4">
            <v-img
              v-if="piUrlSet && piUrl"
              :src="piUrl + '/video_feed'"
              style="overflow: unset"
              class="videoFeed"
            >
              <div class="left"></div>
              <div class="right"></div>
            </v-img>
            <div v-else>
              <v-card class="mx-4" min-height="40vh">
                <tiny-owl />
              </v-card>
            </div>
          </v-col>
          <v-col cols="12"  xs="12" sm="12" md="4" lg="3" xl="2" align-self="center">
            <v-card class="ma-2 elevation-12">
              <v-card-title> Tracking </v-card-title>
              <v-card-text>
                <v-select
                  :items="tracking"
                  dark
                  v-model="config['tracking']"
                ></v-select>
              </v-card-text>
            </v-card>

            <v-card class="ma-2 elevation-12">
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
import TinyOwl from '@/components/tinyOwl.vue'
export default {
  name: "OwlView",
  props: ['piUrl', 'piUrlSet'],
  components: {
    TinyOwl
  },
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
      }
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
  height: calc(105%);
  width: calc(110%);
  border-radius: 25%;
  border: 3px solid white;
}
.left:after {
  right: -15%;
}
.right:after {
  left: -15%;
}

.videoFeed {
  /* width: 60%; */
}
</style>