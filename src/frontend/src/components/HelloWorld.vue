<template>
  <v-container>
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
                  <v-select :items="['items']" label="Standard"></v-select>
                </v-card-text>
              </v-card>
              <v-card class="ma-2">
                <v-card-title> Certainty </v-card-title>
                <v-card-text>
                  <v-slider hint="Im a hint" max="100" min="0"></v-slider>
                </v-card-text>
              </v-card>
            </v-col>
            <v-spacer />
            <v-col cols="6" class="my-4">
              <v-img
                :src="require('../assets/logo.jpg')"
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
                    :items="['single', 'maximise']"
                    label="Standard"
                  ></v-select>
                </v-card-text>
              </v-card>

              <v-card class="ma-2">
                <v-card-title> Actions </v-card-title>
                <v-card-text>
                  <v-checkbox label="Hoot"></v-checkbox>
                  <v-checkbox label="Alert"></v-checkbox>
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
    return {};
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
  /* border: 1px solid; uncomment to see that they aren't overlapped */
  z-index: -100;
  margin-top: -22px;
  margin-bottom: -22px;
}
.left:after,
.right:after {
  position: absolute;
  content: "";
  background: black;
  height: calc(110%); /* 12px because of 6px border on either side */
  width: calc(130%); /* 12px because of 6px border on either side */
  border-radius: 25%;
  border: 3px solid white;
  z-index: -100;
}
.left:after {
  right: -15%;
}
.right:after {
  left: -15%;
}
</style>