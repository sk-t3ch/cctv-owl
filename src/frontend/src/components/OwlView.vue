<template>
  <v-container>
    <v-row class="my-2">
      <v-col cols="12">
        <v-card class="elevation-12 px-4" color="black">
          <v-row justify="center">
            <v-col
              cols="12"
              xs="12"
              sm="12"
              md="4"
              lg="3"
              xl="2"
              align-self="center"
            >
              <v-card class="ma-2 elevation-12" color="secondary">
                <v-card-title> Labels </v-card-title>
                <v-card-text>
                  <v-select
                    color="primary"
                    :items="labels"
                    item-color="accent"
                    v-model="config['label']"
                  ></v-select>
                </v-card-text>
              </v-card>
              <v-card class="ma-2 elevation-12" color="secondary">
                <v-card-title> Certainty </v-card-title>
                <v-card-text>
                  <v-slider
                    v-model="config['threshold']"
                    thumb-label="always"
                    thumb-color="primary"
                    color="accent"
                    max="100"
                    min="0"
                  ></v-slider>
                </v-card-text>
              </v-card>
            </v-col>
            <v-col cols="12" xs="12" sm="12" md="4" lg="6" xl="8" class="my-4 px-0">
              <v-img
                v-if="piUrlSet && piUrl"
                :src="piUrl + '/video_feed'"
                style="overflow: unset"
                class="videoFeed"
                :aspect-ratio="16 / 9"
              >
                <template v-slot:placeholder>
                  <v-row
                    class="fill-height ma-0"
                    align="center"
                    justify="center"
                  >
                    <v-progress-circular
                      indeterminate
                      color="grey lighten-5"
                    ></v-progress-circular>
                  </v-row>
                </template>
              </v-img>
              <div v-else>
                <v-card class="elevation-12" color="primary">
                  <v-responsive :aspect-ratio="16/9">
                    <tiny-owl />
                  </v-responsive>
                </v-card>
              </div>
            </v-col>
            <v-col
              cols="12"
              xs="12"
              sm="12"
              md="4"
              lg="3"
              xl="2"
              align-self="center"
            >
              <v-card class="ma-2 elevation-12" color="secondary">
                <v-card-title> Tracking </v-card-title>
                <v-card-text>
                  <v-select
                    color="secondary"
                    :items="tracking"
                    item-color="accent"
                    dark
                    v-model="config['tracking']"
                  ></v-select>
                </v-card-text>
              </v-card>

              <v-card class="ma-2 elevation-12" color="secondary">
                <v-card-title> Actions </v-card-title>
                <v-card-text>
                  <v-switch
                    inset
                    color="accent"
                    v-model="config['hoot']"
                    label="Hoot"
                  ></v-switch>
                  <v-switch
                    inset
                    color="accent"
                    v-model="config['alert']"
                    label="Alert"
                  ></v-switch>
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
import TinyOwl from "@/components/tinyOwl.vue";
export default {
  name: "OwlView",
  props: ["piUrl", "piUrlSet"],
  components: {
    TinyOwl,
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
      },
    };
  },
  watch: {
    config: {
      deep: true,
      handler() {
        this.updateConfig();
      },
    },
  },
  methods: {
    async updateConfig() {
      const result = await fetch(this.piUrl + "/update_config", {
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

</style>