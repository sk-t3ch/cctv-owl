<template>
  <v-container fill-height>
    <v-row class="text-center">
      <v-col class="mb-4">
        <v-card class="brown" dark>
          <v-card-text class="display-2 font-weight-bold">
            CCTV OWL
          </v-card-text>
          <v-row justify="center">
            <v-col cols="auto">
              <v-card class="ma-2">
                <v-card-title> Labels </v-card-title>
                <v-card-text>
                  <v-select :items="labels" v-model="config['label']" label="Standard"></v-select>
                </v-card-text>
              </v-card>
              <v-card class="ma-2">
                <v-card-title> Certainty </v-card-title>
                <v-card-text>
                  <v-slider v-model="config['threshold']" thumb-label="always" max="100" min="0"></v-slider>
                </v-card-text>
              </v-card>
            </v-col>
            <v-spacer />
            <v-col cols="5" class="my-4">
              <v-img
                :src="video_feed_url"
                style="overflow: unset"
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
                    label="Standard"
                    v-model="config['tracking']"
                  ></v-select>
                </v-card-text>
              </v-card>

              <v-card class="ma-2">
                <v-card-title> Actions </v-card-title>
                <v-card-text>
                  <v-checkbox v-model="config['hoot']" label="Hoot"></v-checkbox>
                  <v-checkbox v-model="config['alert']" label="Alert"></v-checkbox>
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
  name: "HelloWorld",
  data() {
    return {
      labels: [
        'person',
        'bird',
        'book',
        'dog',
        'all'
      ],
      tracking: [
        'single',
        'maximise'
      ],
      config: {
        label: 'person',
        tracking: 'single',
        threshold: 70,
        hoot: false,
        alert: false
      },
      video_feed_url: `http://raspberrypi.local:5000/video_feed`,
      update_config_url: `http://raspberrypi.local:5000/update_config`
    };
  },
  watch: {
    config: {
      deep: true,
      handler() {
        console.log("updating config")
        this.updateConfig()
      }
    }
  },
  methods: {
    async updateConfig(){
      const result = await fetch(this.update_config_url, {
        method: 'POST',
        body: JSON.stringify(this.config),
        headers: {
          'Content-Type': 'application/json'
        }
      }).then(resp => resp.json())
      console.log(result)
    }
  }
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